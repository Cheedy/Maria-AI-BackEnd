import os
import json
from os import walk

TEXT_FOLDER = 'rappeurs'


response = []

for (_, _, filenames) in walk(os.path.join(os.getcwd(), TEXT_FOLDER)):
    for artist_filename in filenames:
        
        artist = artist_filename.split('.')[0]
        d = {
                "subject": artist,
                "sentences": [],
                "responses": [artist],
                "value": 1,
                "type":"information"
            }

        with open(os.path.join(os.getcwd(), TEXT_FOLDER, artist_filename), 'r', encoding='utf-8') as f:
            sentences = f.readlines()
            sentences = list(map(lambda x : x.strip('\n'), sentences))
        
        d['sentences'] += sentences
        
        response.append(d)

with open("output.json", "w", encoding='utf-8') as f:
    json.dump(response, f,  ensure_ascii=False)

