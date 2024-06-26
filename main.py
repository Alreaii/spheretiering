import pnwkit
import pandas as pd
import streamlit as st

kit = pnwkit.QueryKit(st.secrets["api_key"])


def getAllianceNations(allianceID: int, greyvm: bool) -> list: #returns a list of all nations in an alliance - list of pnwkit.Nation objects
    allianceNations = kit.query("nations", {"alliance_id": int(allianceID)}, "num_cities vmode last_active color").paginate('nations')
    cleanedNations = []
    for nation in allianceNations:
        if greyvm:
            if nation.color != "gray" and nation.vmode == 0:
                cleanedNations.append(nation)
        else:
            cleanedNations.append(nation)
    return cleanedNations

def getAllianceCities(allianceID: int, greyvm: bool) -> list: #returns a list of all cities in an alliance
    allianceNations = getAllianceNations(allianceID, greyvm)
    allianceCities = []
    for i in range(len(allianceNations)):
        allianceCities.append(allianceNations[i].num_cities)
    # print(sum(allianceCities))
    return allianceCities

def getSphereCities(sphere: list, greyvm: bool): 
    sphereCities = []
    for i in range(len(sphere)):
        sphereCities.append(getAllianceCities(sphere[i], greyvm))
    return sphereCities

def getAlliancesInSphere(sphere: list) -> list: #returns a list of alliance names in a sphere
    sphereNames = []
    for i in range(len(sphere)):
        allianceNames = kit.query("alliances", {"id": int(sphere[i])}, "name").get()
        sphereNames.append(allianceNames.alliances[0].name)
    return sphereNames

def sortCities(cities: list) -> list:
    cities.sort()
    brackets = [0 for _ in range(11)]  # Initialize with length 11
    for city_count in cities:
        if city_count >= 51:
            brackets[10] += 1
        else:
            bracket_index = min((city_count - 1) // 5, 9) 
            brackets[bracket_index] += 1
    return brackets


def castToDataframe(cities: list) -> pd.DataFrame:
    df = pd.DataFrame({"1-5 cities": [cities[0]], "6-10 cities": [cities[1]], "11-15 cities": [cities[2]], "16-20 cities": [cities[3]], "21-25 cities": [cities[4]], "26-30 cities": [cities[5]], "31-35 cities": [cities[6]], "36-40 cities": [cities[7]], "41-45 cities": [cities[8]], "46-50 cities": [cities[9]], "51+ cities": [cities[10]]})
    return df

def getSphereInput(index):
    alliance_ids = st.text_input(f"Alliance IDs for Sphere {index + 1} (separate by comma eg 1584, 7000, 4468)", key=f"sphere_{index}_alliance_ids")
    return alliance_ids.split(",")

num_spheres = st.number_input("How many spheres are you comparing?", value=0, step=1, min_value=0, max_value=10)
greyvmbutton = st.checkbox("Exclude grey nations and VM nations?")

spheres = []
if num_spheres > 0:
    for i in range(num_spheres):
        spheres.append(getSphereInput(i))

confirmed = st.button("Submit")

if confirmed:
    sphere_data = []
    for sphere_id in spheres:
        alliance_names = getAlliancesInSphere(sphere_id)
        sphere_cities = getSphereCities(sphere_id, greyvmbutton)
        sphere_city_distributions = [sortCities(city_distribution) for city_distribution in sphere_cities]
        total_city_distribution = [sum(x) for x in zip(*sphere_city_distributions)]
        st.write(f"Sphere {len(sphere_data) + 1} - {alliance_names}")
        st.table(castToDataframe(total_city_distribution))
        sphere_data.append((alliance_names, total_city_distribution))

    for i, (alliance_names, mean_city_distribution) in enumerate(sphere_data): # plot barcharts
        st.write(f"Sphere {i+1} - {alliance_names}")
        df = pd.DataFrame({"City Range": ["1-5 cities", "6-10 cities", "11-15 cities", "16-20 cities", "21-25 cities", "26-30 cities", "31-35 cities", "36-40 cities", "41-45 cities", "46-50 cities", "51+ cities"], "Mean City Count": mean_city_distribution})
        st.bar_chart(df.set_index("City Range"))




