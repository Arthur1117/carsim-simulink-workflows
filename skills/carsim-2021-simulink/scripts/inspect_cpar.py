#!/usr/bin/env python3
"""Inspect a local ZIP-based CarSim CPAR without extracting or modifying it.

This verifies container/assets only. Native import and simulation need separate
evidence; neither is certified by this script.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile


def digest(stream):
    value = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        value.update(block)
    return value.hexdigest()


def inspect(args):
    source = args.archive.resolve(strict=True)
    report = {
        "archive": str(source),
        "bytes": source.stat().st_size,
        "scope": "local ZIP-based CPAR container and asset inspection only",
        "nativeExporterProvenanceVerified": None,
        "nativeImportVerified": None,
        "simulationVerified": None,
        "crcChecked": False,
        "errors": [],
    }
    with source.open("rb") as stream:
        report["sha256"] = digest(stream)
    if source.suffix.lower() != ".cpar":
        report["errors"].append("Expected a .cpar filename.")
    with zipfile.ZipFile(source) as archive:
        entries = [entry for entry in archive.infolist() if not entry.is_dir()]
        by_name = {entry.filename.replace("\\", "/"): entry for entry in entries}
        report["entryCount"] = len(entries)
        report["uncompressedBytes"] = sum(entry.file_size for entry in entries)
        if len(by_name) != len(entries):
            report["errors"].append("Ambiguous duplicate entry names.")
        for name in ["cpar_ver.ini", "temp.par"] + args.required_file:
            if name.replace("\\", "/") not in by_name:
                report["errors"].append("Required entry missing: " + name)
        if "cpar_ver.ini" in by_name:
            entry = by_name["cpar_ver.ini"]
            if entry.file_size <= 16384:
                report["formatMarker"] = archive.read(entry).decode("ascii", errors="replace")
            else:
                report["errors"].append("Unexpectedly large CPAR format marker.")
        if args.check_crc:
            bad_entry = archive.testzip()
            report["crcChecked"] = True
            report["crcValid"] = bad_entry is None
            if bad_entry is not None:
                report["errors"].append("CRC failed: " + bad_entry)
        if args.expect_model is not None:
            name = args.model_entry.replace("\\", "/")
            if name not in by_name:
                report["errors"].append("Model entry missing: " + name)
            else:
                with archive.open(by_name[name]) as stream:
                    actual = digest(stream)
                with args.expect_model.open("rb") as stream:
                    expected = digest(stream)
                report["model"] = {
                    "entry": name,
                    "expectedPath": str(args.expect_model.resolve()),
                    "archiveSHA256": actual,
                    "expectedSHA256": expected,
                    "identical": actual == expected,
                }
                if actual != expected:
                    report["errors"].append("Archived model differs from expected model.")
    report["containerInspectionPassed"] = not report["errors"]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--check-crc", action="store_true")
    parser.add_argument("--required-file", action="append", default=[])
    parser.add_argument("--model-entry")
    parser.add_argument("--expect-model", type=Path)
    args = parser.parse_args()
    if (args.model_entry is None) != (args.expect_model is None):
        parser.error("Use --model-entry and --expect-model together.")
    try:
        report = inspect(args)
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as error:
        report = {
            "archive": str(args.archive),
            "containerInspectionPassed": False,
            "nativeImportVerified": None,
            "simulationVerified": None,
            "errors": [str(error)],
        }
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if report["containerInspectionPassed"] else 2


if __name__ == "__main__":
    sys.exit(main())
