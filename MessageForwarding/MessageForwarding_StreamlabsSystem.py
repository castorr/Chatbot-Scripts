#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Forward messages from twitch chat to discord chat or the other way around"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Message Forwarding"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.5"
Description = "Forward messages between discord, twitch and youtube"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.5         Added Mixer support
1.4         Fixed typos in UI config
1.3         Updated to work with Youtube (Chatbot 1.0.2.29)
1.0.0.2     Names are now displayed with proper capitalization
            Added button to readme.txt
1.0.0.1     Added option to enable/disable whispers & DMs
1.0.0.0     Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
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

        else: #set variables if no settings file is found
            self.Enabled = True
            self.OnlyLive = True
            self.Whispers = True
            self.BaseResponse = "[DISCORD] {0}: {1}"
            self.DEnabled = True
            self.NotLive = True
            self.DM = True
            self.Response = "[STREAM] {0}: {1}"


    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def Save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------------------
# Optional functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    if returnValue == MB_YES:

        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

        MySet = Settings()
        MySet.Save(settingsFile)

def ReloadSettings(jsonData):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsonData)

def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

def Tick():
    """Required tick function"""

def Execute(data):
    """Required Execute Data function"""
    if MySet.Enabled and data.IsChatMessage() and data.IsFromDiscord():
        if not MySet.OnlyLive or Parent.IsLive():
            if MySet.DM or not data.IsWhisper():
                Parent.SendStreamMessage(MySet.BaseResponse.format(data.UserName, data.Message))

    if MySet.DEnabled and data.IsChatMessage() and not data.IsFromDiscord():
        if not MySet.NotLive or not Parent.IsLive():
            if MySet.Whispers or not data.IsWhisper():
                Parent.SendDiscordMessage(MySet.Response.format(data.UserName, data.Message))
