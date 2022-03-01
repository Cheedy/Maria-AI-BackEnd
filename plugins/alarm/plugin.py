import time
import sys
sys.path.append('../../')
from pluginDefault import PluginDefault

class PluginAlarm(PluginDefault):

    def response(self, sentence=""):
        themeName= self.subject.split(".")[1]
        if themeName == "whatTime":    
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            return "il est "+ current_time
        elif themeName == "whatTimeAlarm":
            return "l'alarm ne fonction pas"
        elif themeName == "configAlarm":
            return "l'alarm ne fonction pas encore"

    