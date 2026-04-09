# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

A GeoJSON data repository for emergency medical services (Rettungsdienst) in Upper Austria (Oberösterreich) and neighboring regions (Bavaria, Lower Austria, Salzburg, Styria). Contains geographic boundaries, station locations, coverage zones, and road network data used for dispatch planning and visualization.

## Manifest generation

After adding, removing, or modifying `.geojson` files, regenerate the manifest:

```bash
python scripts/generate_geojson_manifest.py
```

Optional flags:
- `--output <path>` — write manifest to a custom path instead of `./manifest.json`
- `--include-sensitive` — also scan `.git`, `node_modules`, `venv`

The script resolves the repo root from its own location (`__file__`), so it works from any working directory.

## Data organization

| Directory | Geometry | Description |
|---|---|---|
| `Anfahrtszeit/Linz/` | MultiPolygon | Drive-time isochrones from Linz (0–15 min, 15–30 min, … up to 90 min) |
| `Bezirke/` | Polygon | 18 administrative districts of Upper Austria |
| `Gemeinden/` | Polygon | Municipal boundaries, one file per district |
| `Leitstellen-Bereiche/` | Polygon | Dispatch center coverage areas (HRV, INN, RLZ, SKG, SrKi) |
| `NAH-Stützpunkte/` | Point / MultiPolygon | Emergency helicopter (NAH) bases and seasonal zones (Sommer/Winter/Zwischensaison) for Austria and Bavaria |
| `RD-Dienststellen/` | Point | Rescue service stations by state and vehicle type (SEW = ambulance, NEF = emergency physician vehicle) |
| `Sonstiges/` | MultiLineString | Linz public transit lines |
| `Straßen/` | MultiLineString | Motorways (`Autobahnen/`) and federal roads (`Bundesstraßen/`) |
| `Zonen/` | MultiPolygon / Polygon | Coverage zones per dispatch center for NEF and SEW vehicles; `Zonen/X/` holds combined/experimental zones |
| `Zonen/farbzuordnung.json` | — | Maps station names/IDs to a color index (1–5) for map rendering |

## Domain abbreviations

- **RD** — Rettungsdienst (emergency medical service)
- **NEF** — Notarzteinsatzfahrzeug (emergency physician response vehicle)
- **SEW** — Sanitätseinsatzwagen (ambulance)
- **NAH** — Notarzthubschrauber (emergency helicopter)
- **BRD** — Bergrettungsdienst (Mountain Rescue Service)
- **Leitstelle** — dispatch center; region codes: INN = Innviertel, RLZ = Rettungsleitzentrale Linz, SKG = Salzkammergut, SrKi = Steyr/Kirchdorf, HRV = Hausruckviertel
- State suffixes: OOE = Oberösterreich, NÖ = Niederösterreich, SBG = Salzburg, STMK = Steiermark, BY = Bayern
