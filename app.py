from fastapi import FastAPI, Query
import csv
import math

app = FastAPI()

# Load trails from CSV
trails = []
with open("snoqualmie_all_trails.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        trails.append(row)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(float(lat1)), math.radians(float(lat2))
    dphi = math.radians(float(lat2) - float(lat1))
    dlambda = math.radians(float(lon2) - float(lon1))
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1-a))

@app.get("/closest_trail")
def closest_trail(lat: float = Query(...), lon: float = Query(...)):
    closest = None
    min_dist = float("inf")

    for trail in trails:
        # Compare against midpoint (you can change to start/end)
        dist = haversine(lat, lon, trail["Mid Lat"], trail["Mid Lon"])
        if dist < min_dist:
            min_dist = dist
            closest = trail

    return {
        "Trail Name": closest["Trail Name"],
        "Difficulty": closest["Difficulty"],
        "Start": [closest["Start Lat"], closest["Start Lon"]],
        "Mid": [closest["Mid Lat"], closest["Mid Lon"]],
        "End": [closest["End Lat"], closest["End Lon"]],
        "Distance_km": round(min_dist, 3)
    }
