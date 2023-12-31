#!/usr/bin/env python3


import csv
import json
import os.path
from pathlib import Path

csv_files = {
  0:   {"name":"sample deck",                   "abbr":"SMP", "csv":"sampledeck/index.csv"},
  1:   {"name":"menace of darth maul",          "abbr":"DM",  "csv":"menaceofdarthmaul/index.csv"},
  2:   {"name":"the jedi council",              "abbr":"JC",  "csv":"thejedicouncil/index.csv"},
  3:   {"name":"battle of naboo",               "abbr":"BN",  "csv":"battleofnaboo/index.csv"},
  4:   {"name":"enhanced menace of darth maul", "abbr":"EDM", "csv":"enhancedmenaceofdarthmaul/index.csv"},
  5:   {"name":"duel of the fates",             "abbr":"DF",  "csv":"duelofthefates/index.csv"},
  6:   {"name":"enhanced battle of naboo",      "abbr":"EBN", "csv":"enhancedbattleofnaboo/index.csv"},
  7:   {"name":"reflections",                   "abbr":"RF",  "csv":"reflections/index.csv"},
  8:   {"name":"boonta eve podrace",            "abbr":"BP",  "csv":"boontaevepodrace/index.csv"},
  101: {"name":"vset1",                         "abbr":"VS1", "csv":"vset1/index.csv"},
}

#Set Name Abbreviations: 
#MDM  = Menace Of Darth Maul 
#TJC  = The Jedi Council 
#BON  = Battle of Naboo 
#EMDM = Enhanced Menace Of Darth Maul 
#DOTF = Duel Of The Fates 
#EBON = Enhanced Battle Of Naboo 
#BEP  = Boonta Eve Podrace (special preview) 
#PREM = Premium (Shmi Skywalker card only).




cards = []
cards_dark = []
cards_light = []
sets  = []
mturk = {}

print_row = False
print("")
for i in csv_files:
  csv_file = csv_files[i]["csv"]
  print("")
  print("  * "+str(i)+":["+csv_file+"]")

  sets.append({
    "id":       i,
    "name":     csv_files[i]["name"],
    "gempName": csv_files[i]["name"],
    "abbr":     csv_files[i]["abbr"],
    "legacy":   "false"
  })

  with open(csv_file, 'r') as cf:
    csv_file = csv.DictReader(cf, delimiter="|", quotechar="^")
    for row in csv_file:
      if (print_row):
        print(len(row), row)

      if (len(row) > 0):
        side     = row["side"].strip()
        release  = row["set"].strip().lower()
        cardtype = row["type"].strip().lower()
        cardid   = row["id"].strip()
        name     = row["title"].strip()
        image    = row["image"].strip()
        rarity   = row["rarity"].strip().lower()
        subtype  = ""



        foil     = "false"
        if (cardid[0:1] == "F"):
          subtype = "foil"
          foil    = "true"


        #print('"' + release + "\"\t\"" + cardtype + "\"\t\"" + cardid + "\"\t\"" + name + "\"\t\"" + image + "\"\t\"" + rarity + '"')
        print('    ** [' + cardid + "]:\t\"" + name + "\"")

        missing_images = [
          #"/menaceofdarthmaul/light/20naboosecurityguard.gif",
          #"/duelofthefates/dark/raynovaca.gif",
          #"/duelofthefates/light/yodajediphilosopher.gif",
          #"/duelofthefates/light/quigonnsfinalstand.gif",
          ]

        if (image in missing_images):
          image = "/missing_image.png"
        elif not os.path.isfile('.'+image):
          print('       *** Image missing: '+image)
          image_bits        = image.split("/")
          search_for_path  = image_bits[1] + "/" + image_bits[2]
          search_for_image = image_bits[3][0:8] + "*"
          print('       *** Searching in.: /'+search_for_path)
          print('       *** For image....: '+search_for_image)

          for found_image in Path(search_for_path).glob(search_for_image):
            print('       *** Found image..: /'+str(found_image))
          exit(1)
          #if not os.path.isfile('.'+image):
          #  print('       *** Image missing: .'+image)


        powercubes = list()
        if row['powercubes1']:
          powercubes.append(row['powercubes1'])
        if row['powercubes2']:
          powercubes.append(row['powercubes2'])
        
        powerdots = list()
        if row['powerdots1']:
          powerdots.append(row['powerdots1'])
        if row['powerdots2']:
          powerdots.append(row['powerdots2'])
        
        whoCanUseTheCard = list()
        if row['whoCanUseTheCard1']:
          whoCanUseTheCard.append(row['whoCanUseTheCard1'])
        if row['whoCanUseTheCard2']:
          whoCanUseTheCard.append(row['whoCanUseTheCard2'])

        deploy = 0
        if row['row1color'] != "none":
          deploy = deploy + 1
        if row['row2color'] != "none":
          deploy = deploy + 1
        if row['row3color'] != "none":
          deploy = deploy + 1
        if row['row4color'] != "none":
          deploy = deploy + 1
        if row['row5color'] != "none":
          deploy = deploy + 1
        if row['row6color'] != "none":
          deploy = deploy + 1


        card = {
          "id": i,
          "gempId": str(i)+"_"+cardid,
          "side": side.capitalize(),
          "rarity": rarity,
          "set": i,
          "printings": [{"set": release}],
          "foil": foil,
          "front": {
            "title": name,
            "imageUrl": "https://res.starwarsccg.org/youngjedi/cards"+image,
            "type": row["type"],
            "subType": subtype,
            "destiny": row["destiny"],
            "power": row["power"],
            "deploy": deploy,
            "forfeit": 0,
            "gametext": "",
            "lore": row["lore"],

            "row1color": row['row1color'],
            "row2color": row['row2color'],
            "row3color": row['row3color'],
            "row4color": row['row4color'],
            "row5color": row['row5color'],
            "row6color": row['row6color'],
            "counters": row['counters'],
            "damage": row['damage'],

            "powercubes1": row['powercubes1'],
            "powercubes2": row['powercubes2'],
            "powercubes": powercubes,

            "powerdots1": row['powerdots1'],
            "powerdots2": row['powerdots2'],
            "powerdots": powerdots,

            "whoCanUseTheCard1": row['whoCanUseTheCard1'],
            "whoCanUseTheCard2": row['whoCanUseTheCard2'],
            "whoCanUseTheCard": whoCanUseTheCard,

            "extraText": [""]
          },
          "counterpart": "",
          #"legacy": "false"
        }
        if (side == "dark"):
          cards_dark.append(card)
        else:
          cards_light.append(card)
        
        cardtype = card["front"]["type"]
        if cardtype not in mturk:
          mturk[cardtype] = []
          mturk[cardtype].append(["gempId", "title", "rarity", "imageUrl"])
        else:
          if i != 0:
            mturk[cardtype].append([card["gempId"], card["front"]["title"], card["rarity"], card["front"]["imageUrl"]])


print("\nWriting Mechanical Turk CSV files")
for cardtype in mturk:
  mturk_csv_file = "../mturk/"+cardtype+".csv"
  print("  * "+mturk_csv_file+" ("+str(len(mturk[cardtype]))+")")
  with open(mturk_csv_file, 'w', newline='') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
      for row in mturk[cardtype]:
        spamwriter.writerow(row)


print("\nWriting JSON files")
print("  * Dark.json")
fh = open("Dark.json", "w")
fh.write(json.dumps({"cards":cards_dark}, indent=2))
fh.close()

print("  * Light.json")
fh = open("Light.json", "w")
fh.write(json.dumps({"cards":cards_light}, indent=2))
fh.close()

print("  * sets.json")
fh = open("sets.json", "w")
fh.write(json.dumps(sets, indent=2))
fh.close()

print("\ndone.\n")

