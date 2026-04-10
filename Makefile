.PHONY: all manifest overlay clean

all: manifest overlay

manifest:
	@echo "Generating manifest.json..."
	python3 scripts/generate_geojson_manifest.py

overlay:
	@echo "Generating overlay_config.json..."
	python3 scripts/generate_overlay_config.py

clean:
	rm -f manifest.json overlay_config.json
	@echo "Cleaned generated files."
