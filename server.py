from flask import Flask, request
from app import analyse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from models import getModelSubjects
import numpy 
import tools
import os
import json 
import tensorflow as tf
import gc

APP_CLIENT_ID = '46779c3107054077b4759735552b9706' #clientID of spotify developer
APP_CLIENT_SECRET = 'a8691ff53d6242f5ab6f866bd4de4814' #same for client secret

app = Flask(__name__)
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=APP_CLIENT_ID,
                                                                client_secret=APP_CLIENT_SECRET))



@app.route("/")
def get_answer():
    subjects, types, stopwords, dictionnary = tools.defaultValues()
    text = request.args.get("text")
    rSubject, rType, rValue= analyse(text)
    response = subjects[numpy.argmax(rSubject)]
    print(response)
    if response.split('.')[0] != 'rap':
        response = "not found"
        return {"results" : 0}

    name    = response.split('.')[1]
    q       = f'"{name}" genre:"french hip hop"'
    results = spotify.search(q, type='artist', market="FR")

    return {"results" : results['artists']['items']}

@app.route("/correct")
def correct_output():
    text = request.args.get("text")
    rappeur = request.args.get("rappeur")

    file_path = os.path.join(os.getcwd(), 'training_data', 'rap.json')

    with open(file_path, 'r') as f:
        records = json.load(f)

    idx = -1

    for i, record in enumerate(records):
        if record["subject"] == rappeur:
            idx = i
            break
    
    if idx != -1:
        records[idx]['sentences'].append(text)
    else:
        records.append({
                    "subject":rappeur,
                    "sentences": [text],
                    "responses": [rappeur],
                    "value": 1,
                    "type":"information"
                })
    
    with open(file_path, 'w') as f:
        json.dump(records, f, ensure_ascii=False)

    subjects, types, stopwords, dictionnary = tools.defaultValues()
    print("subjects:", subjects)
    print("types:", types)
    print("stopwords:", stopwords)
    print(len(dictionnary), "mots")

    input, outputS, outputT, outputV = tools.readPathForTraining("plugins", subjects, types, dictionnary, stopwords)
    input2, outputS2, outputT2, outputV2 = tools.readPathForTraining("training_data", subjects, types, dictionnary, stopwords)
    input= input + input2
    outputS= outputS + outputS2
    outputT= outputT + outputT2
    outputV= outputV + outputV2

    modelSubjects= getModelSubjects(dictionnary, subjects)
    modelSubjects.fit(input, outputS, n_epoch=len(input), batch_size=len(subjects), show_metric=True)
    modelSubjects.save("data/modelSubjects.tflearn")
    tf.keras.backend.clear_session()
    del modelSubjects
    gc.collect()
    
    return {"response" : 1}


if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=8080)