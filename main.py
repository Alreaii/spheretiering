import pnwkit
import numpy
import pandas as pd
import streamlit as st


kit = pnwkit.QueryKit(st.secrets["api_key"])

#list of odoo alliances

names = True
confirmed = False

sphere1name = st.text_input("Sphere 1 name", "")
sphere2name = st.text_input("Sphere 2 name", "")

if sphere1name and sphere2name:
    sphere1 = st.text_input(f"{sphere1name} alliance IDs, separate by comma (eg 1584, 7000, 4468)", "")
    sphere2 = st.text_input(f"{sphere2name} alliance IDs, separate by comma (eg 1584, 7000, 4468)", "")
    greyvmbutton = st.checkbox("Exclude grey nations and VM nations?")
    confirmed = st.button("Submit")
    sphere1, sphere2 = sphere1.split(","), sphere2.split(",")

sphere1cities = []
sphere1aas = []
sphere2cities = []
sphere2aas = []


if confirmed:
    for i in range(len(sphere1)):
        allianceNations = kit.query("nations", {"alliance_id": int(sphere1[i])}, "num_cities vmode last_active color").get()
        for j in range(len(allianceNations.nations)):
            if greyvmbutton:
                if allianceNations.nations[j].color != "gray" and allianceNations.nations[j].vmode == 0:
                    sphere1cities.append(allianceNations.nations[j].num_cities)
            else:
                sphere1cities.append(allianceNations.nations[j].num_cities)

    for i in range(len(sphere2)):
        allianceNations = kit.query("nations", {"alliance_id": int(sphere2[i])}, "num_cities vmode last_active color").get()
        for j in range(len(allianceNations.nations)):
            if greyvmbutton:
                if allianceNations.nations[j].color != "gray" and allianceNations.nations[j].vmode == 0:
                    sphere2cities.append(allianceNations.nations[j].num_cities)
            else:
                sphere2cities.append(allianceNations.nations[j].num_cities)

    if names:
        for aa in range(len(sphere1)):
            allianceNames = kit.query("alliances", {"id": int(sphere1[aa])}, "name").get()
            sphere1aas.append(allianceNames.alliances[0].name)
        for aa2 in range(len(sphere2)):
            allianceNames2 = kit.query("alliances", {"id": int(sphere2[aa2])}, "name").get()
            sphere2aas.append(allianceNames2.alliances[0].name)


    sphere1cities0to9 = []
    sphere1cities10to15 = []
    sphere1cities16to21 = []
    sphere1cities22to25 = []
    sphere1cities26to29 = []
    sphere1cities30to35 = []
    sphere1cities36to40 = []
    sphere1cities41to44 = []
    sphere1cities45to49 = []
    sphere1cities50plus = []

    for i in range(len(sphere1cities)):
        if sphere1cities[i] <= 9:
            sphere1cities0to9.append(sphere1cities[i])
        elif sphere1cities[i] <= 15:
            sphere1cities10to15.append(sphere1cities[i])
        elif sphere1cities[i] <= 21:
            sphere1cities16to21.append(sphere1cities[i])
        elif sphere1cities[i] <= 25:
            sphere1cities22to25.append(sphere1cities[i])
        elif sphere1cities[i] <= 29:
            sphere1cities26to29.append(sphere1cities[i])
        elif sphere1cities[i] <= 35:
            sphere1cities30to35.append(sphere1cities[i])
        elif sphere1cities[i] <= 40:
            sphere1cities36to40.append(sphere1cities[i])
        elif sphere1cities[i] <= 44:
            sphere1cities41to44.append(sphere1cities[i])
        elif sphere1cities[i] <= 49:
            sphere1cities45to49.append(sphere1cities[i])
        else:
            sphere1cities50plus.append(sphere1cities[i])


    sphere2cities0to9 = []
    sphere2cities10to15 = []
    sphere2cities16to21 = []
    sphere2cities22to25 = []
    sphere2cities26to29 = []
    sphere2cities30to35 = []
    sphere2cities36to40 = []
    sphere2cities41to44 = []
    sphere2cities45to49 = []
    sphere2cities50plus = []

    for i in range(len(sphere2cities)):
        if sphere2cities[i] <= 9:
            sphere2cities0to9.append(sphere2cities[i])
        elif sphere2cities[i] <= 15:
            sphere2cities10to15.append(sphere2cities[i])
        elif sphere2cities[i] <= 21:
            sphere2cities16to21.append(sphere2cities[i])
        elif sphere2cities[i] <= 25:
            sphere2cities22to25.append(sphere2cities[i])
        elif sphere2cities[i] <= 29:
            sphere2cities26to29.append(sphere2cities[i])
        elif sphere2cities[i] <= 35:
            sphere2cities30to35.append(sphere2cities[i])
        elif sphere2cities[i] <= 40:
            sphere2cities36to40.append(sphere2cities[i])
        elif sphere2cities[i] <= 44:
            sphere2cities41to44.append(sphere2cities[i])
        elif sphere2cities[i] <= 49:
            sphere2cities45to49.append(sphere2cities[i])
        else:
            sphere2cities50plus.append(sphere2cities[i])


    sphere1citiesdf = pd.DataFrame({"0-9 cities": [len(sphere1cities0to9)], "10-15 cities": [len(sphere1cities10to15)], "16-21 cities": [len(sphere1cities16to21)], "22-25 cities": [len(sphere1cities22to25)], "26-29 cities": [len(sphere1cities26to29)], "30-35 cities": [len(sphere1cities30to35)], "36-40 cities": [len(sphere1cities36to40)], "41-44 cities": [len(sphere1cities41to44)], "45-49 cities": [len(sphere1cities45to49)], "50+ cities": [len(sphere1cities50plus)]})
    sphere1citiesdf = sphere1citiesdf.rename(index={0: {sphere1name}})

    sphere2citiesdf = pd.DataFrame({"0-9 cities": [len(sphere2cities0to9)], "10-15 cities": [len(sphere2cities10to15)], "16-21 cities": [len(sphere2cities16to21)], "22-25 cities": [len(sphere2cities22to25)], "26-29 cities": [len(sphere2cities26to29)], "30-35 cities": [len(sphere2cities30to35)], "36-40 cities": [len(sphere2cities36to40)], "41-44 cities": [len(sphere2cities41to44)], "45-49 cities": [len(sphere2cities45to49)], "50+ cities": [len(sphere2cities50plus)]})
    sphere2citiesdf = sphere2citiesdf.rename(index={0: {sphere2name}})

    if names:
        st.write(f"Sphere 1 Alliances: {sphere1aas}")

    st.table(sphere1citiesdf)

    if names:
        st.write(f"Sphere 2 Alliances: {sphere2aas}")
    st.table(sphere2citiesdf)

    st.write(f"Sphere 1 total cities: {sum(sphere1cities)}")
    st.write(f"Sphere 2 total cities: {sum(sphere2cities)}")

    st.write(f"Sphere 1 average cities: {numpy.mean(sphere1cities)}")
    st.write(f"Sphere 2 average cities: {numpy.mean(sphere2cities)}")

    st.write(f"Sphere 1 median cities: {numpy.median(sphere1cities)}")
    st.write(f"Sphere 2 median cities: {numpy.median(sphere2cities)}")

    st.write(f"Sphere 1 standard deviation cities: {numpy.std(sphere1cities)}")
    st.write(f"Sphere 2 standard deviation cities: {numpy.std(sphere2cities)}")

    st.write(f"Sphere 1 variance cities: {numpy.var(sphere1cities)}")
    st.write(f"Sphere 2 variance cities: {numpy.var(sphere2cities)}")


