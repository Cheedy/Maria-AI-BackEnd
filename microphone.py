#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import models
import pyttsx3
import tools
import app
import numpy
import tensorflow as tf
import gc

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def getSpeaker(vector):
    modelSpeaker= models.getModelSpeaker(["Joan", "Unknown"])
    modelSpeaker.load("data/modelSpeaker.tflearn")
    result= modelSpeaker.predict([vector])
    print(result)
    tf.keras.backend.clear_session()
    del modelSpeaker
    gc.collect()
    return numpy.argmax(result[0])

try:
    subjects, types, stopwords, dictionnary = tools.defaultValues()
    device_info = sd.query_devices(None, 'input')
    # soundfile expects an int, sounddevice provides a float:
    default_samplerate = int(device_info['default_samplerate'])

    model = vosk.Model("model")
    spk_model = vosk.SpkModel("model-spk")

    with sd.RawInputStream(samplerate=default_samplerate, blocksize = 8000, device=None, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, default_samplerate)
            rec.SetSpkModel(spk_model)
            engine = pyttsx3.init()
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result= json.loads(rec.Result())
                    if "spk" in result:
                        speaker= getSpeaker(result["spk"])
                        if speaker == 0:
                            print("YOU:", result["text"])
                            rSubject, rType, rValue= app.analyse(result["text"])
                            result = app.searchAnswer(result["text"], subjects[numpy.argmax(rSubject)], types[numpy.argmax(rType)])
                            print("LINA:",result)
                            engine.say(result)
                            engine.runAndWait()

except KeyboardInterrupt:
    print('\nDone')
    exit(0)
except Exception as e:
    exit(type(e).__name__ + ': ' + str(e))
