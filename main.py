import requests
import json
from bs4 import BeautifulSoup

petData = []
hugeData = requests.get("https://petsimulatorvalues.com/ps99.php?category=Huges").content
titanicData = requests.get("https://petsimulatorvalues.com/ps99.php?category=titanics").content

def handleValue(value):
    if value == "O/C" or value == "SOON":
        return 0
    if "M" in value:
        return int(float(value.replace("M", "")) * 1000000)
    if "B" in value:
        return int(float(value.replace("B", "")) * 1000000000)
    if "T" in value:
        return int(float(value.replace("B", "")) * 1000000000000)

def handleData(data, petData):
    soup = BeautifulSoup(data, "html.parser")
    pets = soup.find_all("div", {"class": "cards-groups"})[0]

    for pet in pets.findChildren("a"):
        base = pet.find("div", {"class": "text-white"})
        valueBase = base.find("div", {"class": "p-1 pl-3 pr-3"})

        name = base.find("h5", {"class": "item-name"}).text.strip().lower()
        value = handleValue(valueBase.find("span", {"class": "float-right pt-2"}).text.strip())

        info = {
            "name": name.replace("shiny ", "").replace(" (rainbow)", "").replace(" (golden)", ""),
            "value": value,
            "rarity": ("rainbow" in name and "rainbow") or ("golden" in name and "golden") or "normal",
            "shiny": "shiny" in name
        }

        petData.append(info)

    return petData

petData = handleData(hugeData, petData)
petData = handleData(titanicData, petData)

with open("values.json", "r+") as valuesFile:
    values = json.load(valuesFile)
    values["values"] = petData
    valuesFile.seek(0)
    json.dump(values, valuesFile, indent=4)
    valuesFile.truncate()