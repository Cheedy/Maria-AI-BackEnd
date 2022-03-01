import time
import sys
sys.path.append('../../')
from pluginDefault import PluginDefault
import os



class PluginTasks(PluginDefault):

    _tasks= []

    def response(self, sentence=""):
        themeName= self.subject.split(".")[1]
        if themeName == "today":
            if len(type(self)._tasks) == 0:
                return "Rien de prévu aujourd'hui"
            else:
                tasks=""
                for i in range(len(type(self)._tasks)):
                    tasks+=type(self)._tasks[i]+"\n"
                return tasks
        elif themeName == "soundDown":
            if type(self)._volume - 20 >= 0:
                type(self)._volume-= 20
                os.system("setvol "+str(type(self)._volume))
            return "Ok"
        elif themeName == "soundMute":
            if  not type(self)._isMute :
                os.system("setvol mute")
            else: 
                os.system("setvol unmute")
            type(self)._isMute= not  type(self)._isMute
            return "Ok"

    