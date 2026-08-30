import json
import os

input_file = '/root/git/geojson/Linz-AG-Linien-2/Linz-AG-Linien.geojson'
output_dir = '/root/git/geojson/Linz-AG-Linien-2/split_linien'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group features by 'ref'
features_by_ref = {}

for feature in data.get('features', []):
    props = feature.get('properties', {})
    ref = props.get('ref')
    
    if not ref:
        # If there's no ref, maybe it has a name like 'Linie 1', or we can try to extract it.
        # Let's print a warning for features without ref.
        print(f"Warning: Feature missing 'ref' property: {props.get('name')}")
        continue
    
    if ref not in features_by_ref:
        features_by_ref[ref] = []
        
    features_by_ref[ref].append(feature)

for ref, features in features_by_ref.items():
    # Make sure we use a valid filename, remove any weird characters
    safe_ref = str(ref).replace('/', '_').replace('\\', '_')
    filename = f"Linie-{safe_ref}.geojson"
    filepath = os.path.join(output_dir, filename)
    
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(feature_collection, f, indent=2, ensure_ascii=False)
        
    print(f"Created {filename} with {len(features)} features.")

print(f"\nDone! Split into {len(features_by_ref)} files in {output_dir}")
