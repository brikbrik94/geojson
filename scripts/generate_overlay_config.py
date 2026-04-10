#!/usr/bin/env python3
"""Generate overlay_config.json based on directory structure and mapping rules."""

import json
from pathlib import Path
from typing import Any, Dict, List

def main():
    repo_root = Path(__file__).resolve().parents[1]
    mapping_file = repo_root / "scripts" / "overlay_mapping.json"
    output_file = repo_root / "overlay_config.json"

    if not mapping_file.exists():
        print(f"Error: Mapping file {mapping_file} not found.")
        return

    with open(mapping_file, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    exact_matches = mapping.get("exact_matches", {})
    prefix_matches = mapping.get("prefix_matches", {})

    datasets: List[Dict[str, Any]] = []

    # Get all directories that contain at least one .geojson file
    dirs_with_geojson = set()
    for geojson_path in repo_root.rglob("*.geojson"):
        if ".git" in geojson_path.parts or "scripts" in geojson_path.parts:
            continue
        dirs_with_geojson.add(geojson_path.parent)

    # Sort directories to ensure consistent output
    for dir_path in sorted(dirs_with_geojson):
        rel_path = dir_path.relative_to(repo_root).as_posix()
        
        dataset_config = None

        # Try exact match first
        if rel_path in exact_matches:
            dataset_config = exact_matches[rel_path].copy()
        else:
            # Try prefix match
            for prefix, config in prefix_matches.items():
                if rel_path.startswith(prefix) or dir_path.name.startswith(prefix):
                    dataset_config = config.copy()
                    break

        if dataset_config:
            dataset_config["path"] = rel_path
            # If name is not provided, use the folder name
            if "name" not in dataset_config:
                dataset_config["name"] = dir_path.name
            datasets.append(dataset_config)
        else:
            print(f"Warning: No mapping found for directory '{rel_path}'. Skipping.")

    overlay_config = {
        "version": "1.0",
        "datasets": datasets
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(overlay_config, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Successfully generated {output_file} with {len(datasets)} datasets.")

if __name__ == "__main__":
    main()
