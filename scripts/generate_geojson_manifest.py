#!/usr/bin/env python3
"""Generate a manifest of GeoJSON files in the repository."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SENSITIVE_DIRS = {".git", "node_modules", "venv"}
GEOMETRY_TYPES = {
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively scan for GeoJSON files and generate a manifest."
    )
    parser.add_argument(
        "--output",
        default="manifest.json",
        help="Path to the output manifest file (default: ./manifest.json)",
    )
    parser.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include files inside .git, node_modules, and venv directories.",
    )
    return parser.parse_args()


def should_skip(path: Path, include_sensitive: bool) -> bool:
    if include_sensitive:
        return False
    return any(part in SENSITIVE_DIRS for part in path.parts)


def extract_types_and_count(data: Any) -> tuple[set[str], int]:
    feature_types: set[str] = set()
    feature_count = 0

    def add_geometry_type(geometry: Any) -> None:
        if geometry is None:
            feature_types.add("null")
            return
        if not isinstance(geometry, dict):
            return
        geometry_type = geometry.get("type")
        if isinstance(geometry_type, str):
            feature_types.add(geometry_type)

    if not isinstance(data, dict):
        return feature_types, feature_count

    data_type = data.get("type")

    if data_type == "FeatureCollection":
        features = data.get("features")
        if isinstance(features, list):
            for feature in features:
                if not isinstance(feature, dict) or feature.get("type") != "Feature":
                    continue
                feature_count += 1
                add_geometry_type(feature.get("geometry"))
    elif data_type == "Feature":
        feature_count = 1
        add_geometry_type(data.get("geometry"))
    elif isinstance(data_type, str) and data_type in GEOMETRY_TYPES:
        add_geometry_type(data)

    return feature_types, feature_count


def main() -> int:
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = repo_root / output_path

    file_entries: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    geojson_paths = [
        path
        for path in repo_root.rglob("*.geojson")
        if path.is_file() and not should_skip(path.relative_to(repo_root), args.include_sensitive)
    ]

    for path in sorted(geojson_paths, key=lambda p: str(p.relative_to(repo_root))):
        rel_path = path.relative_to(repo_root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append({"name": rel_path, "error": str(exc)})
            continue

        feature_types, feature_count = extract_types_and_count(data)
        file_entries.append(
            {
                "name": rel_path,
                "feature_types": sorted(feature_types),
                "feature_count": feature_count,
            }
        )

    manifest: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "files": file_entries,
    }
    if errors:
        manifest["errors"] = errors

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Manifest written to {output_path}")
    if errors:
        print(f"Completed with {len(errors)} file error(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
