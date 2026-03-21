#!/usr/bin/env python3
"""
Strip a GeoJSON file down to only the properties needed by the hfxtrees app,
shorten property keys, and truncate coordinate precision.

Usage:
    python clean-geojson.py <input.json> <output.json>

Example:
    python clean-geojson.py trees.json ../static/hfxtrees-min.json
"""

import json
import sys

# Properties to keep, mapped to short keys
PROPERTY_MAP = {
    "SP_SCIEN": "s",
    "SP_COMM": "c",
    "DBH": "d",
    "INSTYR": "y",
    "WIRES": "w",
    "OWNER": "o",
    "LOCGEN": "l",
    "TREEID": "t",
}

# Decimal places for coordinates (4 = ~11m accuracy)
COORD_PRECISION = 4


def clean_feature(feature):
    props = feature.get("properties", {})
    new_props = {}
    for old_key, new_key in PROPERTY_MAP.items():
        if old_key in props:
            new_props[new_key] = props[old_key]

    coords = feature["geometry"]["coordinates"]
    new_coords = [round(c, COORD_PRECISION) for c in coords]

    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": new_coords},
        "properties": new_props,
    }


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path) as f:
        data = json.load(f)

    cleaned = {
        "type": "FeatureCollection",
        "features": [clean_feature(f) for f in data["features"]],
    }

    with open(output_path, "w") as f:
        json.dump(cleaned, f, separators=(",", ":"))

    in_size = os.path.getsize(input_path)
    out_size = os.path.getsize(output_path)
    print(f"{input_path}: {in_size / 1_048_576:.1f}MB")
    print(f"{output_path}: {out_size / 1_048_576:.1f}MB")
    print(f"Reduction: {(1 - out_size / in_size) * 100:.0f}%")


if __name__ == "__main__":
    import os
    main()
