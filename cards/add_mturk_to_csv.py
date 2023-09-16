#!/usr/bin/env python3

import csv
#import pandas as pd
import json
import os.path
from pathlib import Path


def rowcolor(row, n):
  colors = ["red", "orange", "blue", "yellow", "green", "purple", "white"]
  for c in colors:
    if 'Answer.'+str(n)+'-'+c+'.on' in row:
      if row['Answer.'+str(n)+'-'+c+'.on'] == "true":
        return c
  return "none"


def addtotherow(mkrow, csvrow, field):
  k = 'Answer.'+field
  if k in mkrow:

    v = mkrow[k].replace("jabba the hutt", "Jabba the Hutt").replace(" ,", ",").replace("Hutt or", "Hutt, or").replace('“', '"').replace('”', '"').replace("—", "-").replace("Tu as débloqué 'Royaume de Chocolat' - Voyage plus haut pour en débloquer davantage!", "").replace("''", '"').replace("Tatoonie", "Tatooine")

    f = field.replace("wcutc", "whoCanUseTheCard").replace("wcutwb", "whoCanUseTheCard")
    if f == "whoCanUseTheCard":
      f = "whoCanUseTheCard1"
    if f == "powerdots":
      f = "powerdots1"
    if f == "powercubes":
      f = "powercubes1"
    if "powercubes" or "powerdots" in f:
      v = v.replace("N/A", "0").replace("?", "1")
    print(field, f)
    csvrow[f] = v
  return csvrow




csv_files = {
  0: {"name":"sample deck",                   "abbr":"SMP", "csv":"sampledeck/index.csv"},
  1: {"name":"menace of darth maul",          "abbr":"DM",  "csv":"menaceofdarthmaul/index.csv"},
  2: {"name":"the jedi council",              "abbr":"JC",  "csv":"thejedicouncil/index.csv"},
  3: {"name":"battle of naboo",               "abbr":"BN",  "csv":"battleofnaboo/index.csv"},
  4: {"name":"enhanced menace of darth maul", "abbr":"EDM", "csv":"enhancedmenaceofdarthmaul/index.csv"},
  5: {"name":"duel of the fates",             "abbr":"DF",  "csv":"duelofthefates/index.csv"},
  6: {"name":"enhanced battle of naboo",      "abbr":"EBN", "csv":"enhancedbattleofnaboo/index.csv"},
  7: {"name":"reflections",                   "abbr":"RF",  "csv":"reflections/index2.csv"},
  8: {"name":"boonta eve podrace",            "abbr":"BP",  "csv":"boontaevepodrace/index.csv"},
}

mturk_result_csv_files = {
  "character": "../mturk/character_results.csv",
  "battle":    "../mturk/battle_results.csv",
  "weapon":    "../mturk/weapon_results.csv",
}

dots = ".................................."

rows_assembled = dict()
print("\n\n")
print("Parsing mturk Files:")
for i in mturk_result_csv_files:
  csvf = mturk_result_csv_files[i]
  print("  *",i)
  with open(csvf, 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
      #print(dict(row))
      gempid = row['Input.gempId']
      title = row['Input.title']
      rarity = row['Input.rarity']
      imageUrl = row['Input.imageUrl']

      n = 0
      colors = ["red", "orange", "blue", "yellow", "green", "purple", "white"]
      while n < 7:
        n = n + 1
        for c in colors:
          if 'Answer.'+str(n)+'-'+c+'.on' not in row:
            row['Answer.'+str(n)+'-'+c+'.on'] = "false"
          if 'Answer.'+str(n)+'-'+c+'.off' not in row:
            row['Answer.'+str(n)+'-'+c+'.off'] = "false"


      row1color = rowcolor(row, 1)
      row2color = rowcolor(row, 2)
      row3color = rowcolor(row, 3)
      row4color = rowcolor(row, 4)
      row5color = rowcolor(row, 5)
      row6color = rowcolor(row, 6)

      rows_assembled[gempid] = {
        "gempid":gempid,
        "title":title,
        "rarity":rarity,
        "imageUrl":imageUrl,
        "row1color":row1color,
        "row2color":row2color,
        "row3color":row3color,
        "row4color":row4color,
        "row5color":row5color,
        "row6color":row6color,
      }


      ## Characters
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'counters')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'damage')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'destiny')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'lore')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'power')

      ## Weapons
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'powercubes1')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'powercubes2')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'powerdots1')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'powerdots2')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'wcutwb1')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'wcutwb2')

      ## Battle
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'powerdots')
      rows_assembled[gempid] = addtotherow(row, rows_assembled[gempid], 'wcutc')

      create_power_list = False
      if create_power_list:
        rows_assembled[gempid]["powerdots"] = []
        rows_assembled[gempid]["powercubes"] = []
        rows_assembled[gempid]["whoCanUseTheCard"] = []

        if 'powerdots1' in rows_assembled[gempid]:
          rows_assembled[gempid]["powerdots"].append(rows_assembled[gempid]["powerdots1"])
        if 'powerdots2' in rows_assembled[gempid]:
          rows_assembled[gempid]["powerdots"].append(rows_assembled[gempid]["powerdots2"])

        if 'powercubes1' in rows_assembled[gempid]:
          rows_assembled[gempid]["powercubes"].append(rows_assembled[gempid]["powercubes1"])
        if 'powercubes2' in rows_assembled[gempid]:
          rows_assembled[gempid]["powercubes"].append(rows_assembled[gempid]["powercubes2"])

        if 'whoCanUseTheCard1' in rows_assembled[gempid]:
          rows_assembled[gempid]["whoCanUseTheCard"].append(rows_assembled[gempid]["whoCanUseTheCard1"])
        if 'whoCanUseTheCard2' in rows_assembled[gempid]:
          rows_assembled[gempid]["whoCanUseTheCard"].append(rows_assembled[gempid]["whoCanUseTheCard2"])



#print(json.dumps(rows_assembled))



cards = dict()
print("\n\n")
print("Parsing CSV Files:")
for i in csv_files:
  #if i > 1:
  #  continue
  csvf = csv_files[i]
  print("  *",csvf["abbr"] + dots[0:(6-len(csvf["abbr"]))] + ": " + csvf["name"])
  #pd.read_csv(csvf["csv"])
  with open(csvf["csv"], 'r') as file:
    ##
    ## https://docs.python.org/3/library/csv.html#csv.DictReader
    ##
    csv_file = csv.DictReader(file, delimiter="|", quotechar="^")
    for row in csv_file:
      #print(dict(row))
      gempid = str(i) + "_" + row["id"]
      row["gempId"] = gempid
      row["setId"] = str(i)


      if gempid in rows_assembled:
        for k in rows_assembled[gempid]:
          row[k] = rows_assembled[gempid][k]

      cards[gempid] = row

print("\n\n")


fh = open("allcards.json", "w")
fh.write(json.dumps(cards))
fh.close()



print("\n\n")
print("Generating Field Names:")
fieldnames = []
for c in cards:
  for k in cards[c].keys():
    if k not in fieldnames:
      fieldnames.append(k)



print("\n\n")
print("Writing new CSV files:")
for i in csv_files:
  new_csv_filename = csv_files[i]['csv'].replace("index", "new")
  print("  *",new_csv_filename)
  with open(new_csv_filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|') #, quoting=csv.QUOTE_NONE)
    writer.writeheader()
    for c in cards:
      if str(i)+"_" in c:
        writer.writerow(cards[c])



print("\n\n")














