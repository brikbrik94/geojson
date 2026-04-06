# geojson

## GeoJSON-Manifest generieren

Das Skript `scripts/generate_geojson_manifest.py` durchsucht das Repository rekursiv nach `*.geojson`-Dateien und erzeugt daraus eine zentrale `manifest.json`.

Es unterstützt folgende GeoJSON-Strukturen:

- `FeatureCollection` (mit `features[]`)
- einzelnes `Feature`
- rohe Geometrieobjekte (z. B. `LineString`, `Polygon`, …)

Pro Datei werden der Pfadname, die gefundenen (eindeutigen, sortierten) Geometrietypen und die Anzahl erkannter Features gespeichert. Bei `geometry: null` wird der Typ als String `"null"` erfasst.

Ungültige JSON-Dateien werden nicht den gesamten Lauf abbrechen: sie landen stattdessen mit Fehlermeldung im Feld `errors`.

### Aufruf

```bash
python scripts/generate_geojson_manifest.py
```

Optional kann ein Ausgabepfad gesetzt werden:

```bash
python scripts/generate_geojson_manifest.py --output output/manifest.json
```

Optional können sensible Ordner (`.git`, `node_modules`, `venv`) mit durchsucht werden:

```bash
python scripts/generate_geojson_manifest.py --include-sensitive
```

### Beispielstruktur der erzeugten Manifest-Datei

```json
{
  "generated_at": "2026-04-06T12:34:56Z",
  "files": [
    {
      "name": "Straßen/Autobahnen/A1.geojson",
      "feature_types": ["LineString"],
      "feature_count": 1
    }
  ],
  "errors": [
    {
      "name": "defekt.geojson",
      "error": "Expecting value: line 1 column 1 (char 0)"
    }
  ]
}
```
