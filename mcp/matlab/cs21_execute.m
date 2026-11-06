function cs21_execute(jobFile)
job = jsondecode(fileread(jobFile));
folder = char(job.folder);
originalFolder = pwd;
originalPath = path;
model = 'cs21_abs_smoke';
assert(~bdIsLoaded(model),'CarSim2021:ModelAlreadyLoaded', ...
    'A model named cs21_abs_smoke is already loaded. Close it before running this experiment.');
libraryWasLoaded = bdIsLoaded('Solver_SF');
if libraryWasLoaded
    assert(strcmp(get_param('Solver_SF','FileName'), ...
        fullfile(char(job.program),'Programs','solvers','Matlab84+','Solver_SF.slx')), ...
        'CarSim2021:LibraryConflict','An unexpected Solver_SF library is loaded.');
end
restore = onCleanup(@() restoreSession(originalFolder,originalPath, ...
    model,folder,libraryWasLoaded));
cd(folder);
addpath(folder);
solverFolder = fullfile(char(job.program),'Programs','solvers','Matlab84+');
addpath(solverFolder);
assert(strcmp(version('-release'),'2025b'),'CarSim2021:Release', ...
    'This adapter is validated for MATLAB R2025b only.');
assert(strcmp(computer('arch'),'win64'),'CarSim2021:Architecture','Expected win64.');
assert(strcmp(which('vs_sf'),fullfile(solverFolder,'vs_sf.mexw64')), ...
    'CarSim2021:MexShadowed','The selected vs_sf is not the pinned 2021 MEX.');
pending = struct('passed',false,'stage','simulation_started','experimentId',job.id);
writeJson(fullfile(folder,'result.json'),pending);
in = Simulink.SimulationInput(model);
in = in.setModelParameter('StartTime','0','StopTime',num2str(job.stopTime,17), ...
    'SimulationMode','normal','ReturnWorkspaceOutputs','on', ...
    'MaxStep',num2str(job.step,17)); %#ok<NASGU>
started = datetime('now','TimeZone','Asia/Shanghai');
out = Simulink.SimulationOutput;
try
    transcript = evalc('out = sim(in);');
catch simulationError
    failure = struct('passed',false,'stage','simulation_failed','experimentId',job.id, ...
        'identifier',simulationError.identifier, ...
        'message',getReport(simulationError,'extended','hyperlinks','off'));
    writeJson(fullfile(folder,'result.json'),failure);
    rethrow(simulationError);
end
writeText(fullfile(folder,'matlab.log'),transcript);
save(fullfile(folder,'simulation.mat'),'out','started');
pending.stage = 'validating';
writeJson(fullfile(folder,'result.json'),pending);
t = double(out.cs21_exports.Time(:));
y = double(out.cs21_exports.Data);
tu = double(out.cs21_imports.Time(:));
u = double(out.cs21_imports.Data);
assert(size(y,2)==6 && size(u,2)==4,'CarSim2021:ChannelCount','Unexpected port dimensions.');
assert(all(isfinite([t;y(:);tu;u(:)])),'CarSim2021:Nonfinite','Nonfinite samples.');
assert(numel(t)>1 && all(diff(t)>0) && abs(t(end)-job.stopTime)<1e-8, ...
    'CarSim2021:TimeGrid','Invalid export time grid.');
assert(isequal(t,tu),'CarSim2021:FeedbackGrid','Input/output time grids differ.');
assert(all(max(u,[],1)-min(u,[],1)>0),'CarSim2021:InactiveControl','No control activity.');
writetable(array2table([t y],'VariableNames', ...
    {'Time_s','Vx_L1','Vx_R1','Vx_L2','Vx_R2','Vx_SM','Pbk_Con'}), ...
    fullfile(folder,'exports.csv'));
writetable(array2table([tu u],'VariableNames', ...
    {'Time_s','IMP_PBK_L1','IMP_PBK_R1','IMP_PBK_L2','IMP_PBK_R2'}), ...
    fullfile(folder,'imports.csv'));
result = struct('passed',true,'stage','matlab_completed','experimentId',job.id, ...
    'matlab',version,'architecture',computer('arch'),'endTime',t(end), ...
    'exportSamples',numel(t),'importSamples',numel(tu),'allFinite',true, ...
    'finalVehicleSpeed_kmh',y(end,5),'maxWheelPressure_MPa',max(u,[],1), ...
    'exportRange',max(y,[],1)-min(y,[],1),'importRange',max(u,[],1)-min(u,[],1));
writeJson(fullfile(folder,'result.json'),result);
disp(jsonencode(result,PrettyPrint=true));
end

function writeJson(filename,value)
writeText(filename,jsonencode(value,PrettyPrint=true));
end

function writeText(filename,value)
fid = fopen(filename,'w','n','UTF-8');
assert(fid~=-1,'CarSim2021:LogWrite','Cannot write run evidence.');
closeFile = onCleanup(@() fclose(fid));
fprintf(fid,'%s\n',value);
end

function restoreSession(folder,searchPath,model,experimentFolder,libraryWasLoaded)
if bdIsLoaded(model) && strcmp(get_param(model,'FileName'), ...
        fullfile(experimentFolder,[model '.slx']))
    close_system(model,0);
end
if ~libraryWasLoaded && bdIsLoaded('Solver_SF')
    close_system('Solver_SF',0);
end
cd(folder);
path(searchPath);
end
