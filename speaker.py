#!/usr/bin/env python3
from vosk import Model, KaldiRecognizer, SpkModel
import sys
import wave
import json
import os
import gc
import numpy as np
import models
import tensorflow as tf

def readAudioFile(filePath):
    wf = wave.open(filePath, "rb")
    model_path = "model"
    spk_model_path = "model-spk"
    model = Model(model_path)
    spk_model = SpkModel(spk_model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetSpkModel(spk_model)
    dataInput= []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print ("Text:", res['text'])
            if 'spk' in res:
                print ("X-vector:", len(res['spk']))
                dataInput.append(res['spk'])
    return  dataInput


if __name__ == '__main__':
    speakers= ["Joan", "unknown"]
    model= models.getModelSpeaker(speakers)
    inputData = readAudioFile("./training_data/mytest.wav")
    outputData = [[1, 0] for _ in range(len(inputData))]
    inputData2 = readAudioFile("./training_data/test2.wav")
    outputData2 = [[0, 1] for _ in range(len(inputData2))]
    inputData += inputData2 
    outputData += outputData2
    model.fit(inputData, outputData, n_epoch=1000, batch_size=128, show_metric=True)
    model.save("data/modelSpeaker.tflearn")
    tf.keras.backend.clear_session()
    del model
    gc.collect()
