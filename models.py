import tools
import tflearn
import numpy
import time
import tensorflow as tf
import gc

def getModelSubjects(dictionnary, subjects):
    tf.keras.backend.clear_session()
    net = tflearn.input_data(shape=[None, len(dictionnary)])
    net = tflearn.fully_connected(net, len(dictionnary)//8, activation="linear")
    net = tflearn.fully_connected(net, len(subjects), activation="softmax")
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    return model

def getModelTypes(dictionnary, types):
    tf.keras.backend.clear_session()
    net2 = tflearn.input_data(shape=[None, len(dictionnary)])
    net2 = tflearn.fully_connected(net2, len(dictionnary)//8, activation="linear")
    net2 = tflearn.fully_connected(net2, len(types), activation="softmax")
    net2 = tflearn.regression(net2)
    model2 = tflearn.DNN(net2)
    return model2

def getModelValues(dictionnary):
    tf.keras.backend.clear_session()
    net3 = tflearn.input_data(shape=[None, len(dictionnary)])
    net3 = tflearn.fully_connected(net3, 16)
    net3 = tflearn.fully_connected(net3, 1, activation="sigmoid")
    net3 = tflearn.regression(net3)
    model3 = tflearn.DNN(net3)
    return model3

def getModelSpeaker(persons):
    tf.keras.backend.clear_session()
    net = tflearn.input_data(shape=[None, 128])
    net = tflearn.fully_connected(net, 64)
    net = tflearn.fully_connected(net, len(persons), activation="softmax")
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    return model

if __name__ == '__main__':
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