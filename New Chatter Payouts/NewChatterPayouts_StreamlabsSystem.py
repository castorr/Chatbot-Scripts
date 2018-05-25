#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Award new chatters with currency when they share it!"""

#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import re
import ctypes
import winsound
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "New Chatter Payout"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.0"
Description = "Give users currency for announcing that they are new"

#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.0 - Initial Release
"""

#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
LogFile = os.path.join(os.path.dirname(__file__), "Log.txt")
reUserNotice = re.compile(r"(?:^(?:@(?P<irctags>[^\ ]*)\ )?:tmi\.twitch\.tv\ USERNOTICE)")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no custom settings file is found
            self.Payout = 20
            self.Message = "Welcome to the stream {0}! Here have {1} {2} <3"
            self.Log = True
            self.LogFormat = "User: {0} | Points added: {1}"

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def Save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------------------
# [OPTIONAL] Settings functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    if returnValue == MB_YES:
        MySet = Settings()
        MySet.Save(settingsFile)

        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

def ReloadSettings(jsondata):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsondata)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

def Execute(data):
    """Required Execute data function"""
    if data.IsRawData() and data.IsFromTwitch():

		# Apply regex on raw data to detect new chatter usernotice
        usernotice = reUserNotice.search(data.RawData)
        if usernotice:

			# Parse IRCv3 tags in a dictionary
            tags = dict(re.findall(r"([^=]+)=([^;]*)(?:;|$)", usernotice.group("irctags")))
			# user-id							> User id of the subscriber/gifter
			# login								> User name of the subscriber/gifter
			# display-name						> Display name of the subscriber/gifter
			# msg-id							> Type of notice; sub, resub, charity, subgift
			# msg-param-months					> Amount of consecutive months
			# msg-param-sub-plan				> sub plan; prime, 1000, 2000, 3000
			# msg-param-recipient-id 			> user id of the gift receiver
			# msg-param-recipient-user-name		> user name of the gift receiver
			# msg-param-recipient-display-name	> display name of the gift receiver

            if tags["msg-param-ritual-name"] == "new_chatter":
                username = tags["display-name"] if tags["display-name"] else tags["login"]
                Parent.AddPoints(username, username, MySet.Payout)

                if MySet.Log:
                    with open(LogFile, "a") as f:
                        f.write(MySet.LogFormat.format(username, MySet.Payout) + "\n")

                if MySet.Message != "":
                    Parent.SendStreamMessage(MySet.Message.format(username, MySet.Payout, Parent.GetCurrencyName()))

def Tick():
    """Required tick function"""
