from tools.shared.map.map_references import MAP_REFERENCES

def get_all_area_names():
    area_names = []

    for map_id, map_data in MAP_REFERENCES.items():
        area_names.append(map_id + " " + map_data["name"])
        
        for area_id, area_data in map_data["areas"].items():
            name = area_data["name"]
            area_names.append(area_id + " " + name)
    
    return area_names
