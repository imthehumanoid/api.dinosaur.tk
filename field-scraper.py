from bs4 import BeautifulSoup
import numpy as np
import requests
import dinosaurs as dino_names

fields_collection = []
model = 'https://www.nhm.ac.uk/discover/dino-directory/'
i = 0
fails = 0
for name in dino_names.endpoints:
  try:
    i = i + 1
    fields = {
        "name": "",
        "pronunciation": "",
        "meaning": "",
        "named_by": "",
        "description": "",
        "type": "",
        "species_type": "",
        "diet": "",
        "era": "",
        "found": "",
        "avg_weight_kg": "",
        "avg_length_m": "",
        "movement": "",
        "taxonomy": "",
        "images": {
          "drawing": "",
          "silhouette": "",
        },
    }

    html = requests.get(model + name + '.html').text

    parsed_html = BeautifulSoup(html, features='html.parser')

    container1 = parsed_html.find('dl', 'dinosaur--description dinosaur--list')
    container2 = parsed_html.find('dl', 'dinosaur--info dinosaur--list')
    container3 = parsed_html.find('dl', 'dinosaur--name-description', 'dinosaur--list')
    container4 = parsed_html.find('dl', 'dinosaur--taxonomy dinosaur--list')
    container5 = parsed_html.find('div', 'dinosaur--content-container small-12 medium-12 large-12 columns')

    info1 = container1.findAll('dd')
    info2 = container2.findAll('dd')
    info3 = container4.findAll('dd')

    label1 = container1.findAll('dt')
    label2 = container2.findAll('dt')
    label3 = container4.findAll('dt')

    info = info1 + info2 + info3
    label = label1 + label2 + label3

    indexes = {
        "name": "",
        "pronunciation": "",
        "meaning": "",
        "named_by": "",
        "description": "",
        "type": "",
        "species_type": "",
        "diet": "",
        "era": "",
        "found": "",
        "avg_weight_kg": "",
        "avg_length_m": "",
        "movement": "",
        "taxonomy": "",
    }

    inx = 0
    for title in label:
      formed = title.contents[0].lower().strip()
      if formed == 'type of dinosaur:':
        indexes['type'] = inx
      elif formed == 'diet:':
        indexes['diet'] = inx
      elif formed == 'when it lived:':
        indexes['era'] = inx
      elif formed == 'found in:':
        indexes['found'] = inx
      elif formed == 'weight:':
        indexes['avg_weight_kg'] = inx
      elif formed == 'length:':
        indexes['avg_length_m'] = inx
      elif formed == 'how it moved:':
        indexes['movement'] = inx
      elif formed == 'named by:':
        indexes['named_by'] = inx
      elif formed == 'type species:':
        indexes['species_type'] = inx
      elif formed == 'taxonomy:':
        indexes['taxonomy'] = inx
      inx = inx + 1

    
    def getInfo(ty):
      try:
        try:
          return info[indexes[ty]].find('a').contents[0].lower().strip()
        except:
          return info[indexes[ty]].contents[0].lower().strip()
      except:
        return 'N/A'
    
    fields['name'] = name
    try:
      fields['pronunciation'] = container3.find('dd', 'dinosaur--pronunciation').contents[0].strip()
    except:
      fields['pronunciation'] = 'N/A'
    try:
      fields['meaning'] = container3.find('dd', 'dinosaur--meaning').contents[0].lower().strip()
    except:
      fields['meaning'] = 'N/A'
    fields['named_by'] = getInfo('named_by')
    try:
      fields['description'] = container5.get_text()
    except:
      fields['description'] = 'N/A'
    fields['type'] = getInfo('type')
    fields['species_type'] = getInfo('species_type')
    fields['diet'] = getInfo('diet')
    fields['era'] = getInfo('era')
    fields['found'] = getInfo('found')
    if getInfo('avg_weight_kg') != 'N/A':
      fields['avg_weight_kg'] = float(getInfo('avg_weight_kg').replace('kg',''))
    else:
      fields['avg_weight_kg'] = getInfo('avg_weight_kg')
    if getInfo('avg_length_m') != 'N/A':
      fields['avg_length_m'] = float(getInfo('avg_length_m').replace('m',''))
    else:
      fields['avg_length_m'] = getInfo('avg_length_m')
    fields['movement'] = getInfo('movement')
    try:
      fields['taxonomy'] = getInfo('taxonomy').split(', ')
    except:
      feilds['taxonomy'] = getInfo('taxonomy')
    try:
      container6 = parsed_html.find('img', 'dinosaur--image')
      fields['images']['drawing'] = container6['src']
    except:
      fields['images']['drawing'] = 'N/A'
    try:
      container7 = parsed_html.find('div', 'dinosaur--comparison-dino').find('img')
      fields['images']['silhouette'] = container7['src']
    except:
      fields['images']['silhouette'] = 'N/A'

    fields_collection.append(fields)
    
    print('Added ' + str(name) + ' | ' + str(i) + '/' + str(len(dino_names.endpoints)))
  except:
    print('Unable to add ' + str(name) + ' | ' + str(i) + '/' + str(len(dino_names.endpoints)))
    fails = fails + 1

print('Finished | ' + str(fails) + ' failed to add')

try:
  f = open('dinosaurs.js', 'w')
  try:
    f.write("module.exports = " + str(fields_collection).replace("'N/A'", 'null'))
    print("Successfully wrote file")
  except:
    print('Unable to write file | Emergency print here:')
    print(fields_collection)
  f.close()
except:
  print('Unable to open file | Emergency print here:')
  print(fields_collection)
