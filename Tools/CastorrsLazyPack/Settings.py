import os
import json
import codecs

class Settings():
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsfile=None):
        if settingsfile and os.path.isfile(settingsfile):
            with codecs.open(settingsfile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file is found
            self.nightbot = True
            self.streamelements = True
            self.deepbot = True
            self.phantombot = True
            self.wizebot = True
            self.time = "%H:%M:%S"
            self.date = "%d/%m-%Y"
            self.excluded = ""
            self.srmessage = "{0} in order to request a song you need to add a song/video ID, url or a search term"
            self.srenabled = True
            self.imperial = False
            self.volume = 50
            self.ytuser = ""
            self.twitteruser = ""
            self.norts = True
            self.tweeturl = True
            self.tweetshort = True
            self.tweethowlong = True
            self.ctt = "Come join me over at https://www.twitch.tv/$mychannel"
            self.cttfailed = "Failed to update click to tweet link!"

    # Reload settings on save through UI
    def reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            pass
