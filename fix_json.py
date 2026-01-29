import json
import os

filepath = "data_hub/hub_index.json"
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the first valid JSON ending
    # The file is expected to be a single JSON object (dict)
    # So we find the first occurrence of the final closing brace that makes it valid
    
    # Actually, the corruption is specific: it has "193" then extra braces.
    # We can just search for the first occurrence of the stats block closure
    if "}193" in content:
        content = content.split("}193")[0] + "}"
    elif "}\n    }\n  }\n}" in content:
        # If I already replaced }193 with } but left the rest
        parts = content.split("}\n    }\n  }\n}")
        content = parts[0] + "}\n  }\n}"
        
    # Let's try to parse it to be sure
    data = json.loads(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Successfully fixed hub_index.json")
except Exception as e:
    print(f"Error: {e}")
