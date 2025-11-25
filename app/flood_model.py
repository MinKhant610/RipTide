def build_flood_input(city, lat, lon, ow, wb):
    return {
        "location": city,
        "lat": lat,
        "lon": lon,
        "openweather": ow,
        "weatherbit": wb
    }
