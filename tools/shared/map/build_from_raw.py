import pprint

state = 'map-name'
map_id = None
map_name = None
area_id = None
area_name = None

result = {}

with open('./tools/shared/map/raw_map.txt', 'r') as file:
    for line in file:
        if not line.strip():
            map_id = None
            map_name = None
            area_id = None
            area_name = None
            state = 'map-name'
        elif state == 'map-name':
            map_name = line.strip()
            state = 'area-id'
        elif state == 'area-id':
            area_id = line.strip()
            if area_id.endswith(':'):
                area_id = area_id[:-1]

            if map_id is None:
                map_id = area_id.split("_")[0]
                result[map_id] = {
                    "name": map_name,
                    "areas": {}
                }
            
            state = 'area-name'
        elif state == 'area-name':
            area_name = line.strip()
            state = 'area-id'
            result[map_id]["areas"][area_id] = {
                "name": area_name
            }

with open("mydict.py", "w") as f:
    f.write("MAP_REFERENCES = ")
    f.write(pprint.pformat(result, indent=4))
    f.write("\n")