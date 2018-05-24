#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Extra parameters including a bunch from Nightbot"""
#---------------------------------------
# Libraries and references
#---------------------------------------
from collections import deque
import codecs
import json
import os
import ctypes
import winsound
import time
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Message Sounds"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.5"
Description = "Plays sound on new messages!"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.5 - Fixed issue with message sound cooldown
1.4 - Added Mixer support
1.3 - Updated to work with chatbot 1.0.2.29 (YouTube Release)
1.2 - Added option to ignore caster messages
1.1 - Updated to work with Youtube
1.0 - Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue2 = deque()
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
            self.Volume = 50
            self.Usage = "Twitch Chat"
            self.Cooldown = 3
            self.Sound = "Discord"
            self.Caster = True

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
# Settings functions
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
    global lastMessage

    MySet = Settings(settingsFile)
    lastMessage = time.time() - MySet.Cooldown*60

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue2:
        if Parent.PlaySound(AudioPlaybackQueue2[0], MySet.Volume*0.01):
            AudioPlaybackQueue2.popleft()

def Execute(data):
    """Required Execute Data function"""
    if data.IsChatMessage() and IsFromValidSource(data, MySet.Usage):
        if Parent.HasPermission(data.User, "Caster", "") and MySet.Caster:
            return

        global lastMessage
        if (lastMessage + MySet.Cooldown*60) < time.time():
            EnqueueAudioFile(MySet.Sound)

        lastMessage = time.time()

def IsFromValidSource(data, Usage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (Usage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (Usage in l):
            return True
    return False

def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    SoundsPath = os.path.join(AudioFilesPath, audiofile + ".mp3")
    AudioPlaybackQueue2.append(SoundsPath)

def TestSound():
    """Test sound & volume through UI button"""
    SoundsPath = os.path.join(AudioFilesPath, MySet.Sound + ".mp3")
    Parent.PlaySound(SoundsPath, MySet.Volume*0.01)
