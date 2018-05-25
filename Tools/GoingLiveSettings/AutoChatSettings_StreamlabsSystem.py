#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Changes twitch chat settings when you go live or offline"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import ctypes
import winsound
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Auto Chat Settings"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.6"
Description = "Set chat settings automatically when you go online/offline"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.6b    - Going offline settings
1.5     - Fixed errorlog.txt spam
1.4     - Code cleanup
1.3     - Fixed loading issues
1.2     - Updated to work with Youtube
1.0.0.1 - Fixed saved settings bug
1.0.0.0 - Initial release
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
            self.GoingLive = True
            self.GoingOffline = True
            self.message = "Stream is now live! If you can't see it hit refresh"
            self.sendMessage = True
            self.Dmessage = "@everone Stream is now live! Come join me over at {0}"
            self.DsendMessage = True
            self.subonly = False
            self.slowmode = False
            self.followers = False
            self.r9k = False
            self.unhost = True
            self.emoteonly = False
            self.followersinfo = ""
            self.slowmodeinfo = ""
            self.messageOFF = "Stream is now offline! BibleThump"
            self.sendMessageOFF = True
            self.DmessageOFF = "Stream just went offline http://offli.ne/dashboard/images/OFFLINE_LOGO_CYAN.png"
            self.DsendMessageOFF = True
            self.subonlyOFF = True
            self.slowmodeOFF = False
            self.followersOFF = False
            self.r9kOFF = False
            self.emoteonlyOFF = True
            self.followersinfoOFF = ""
            self.slowmodeinfoOFF = ""

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
        global MySet
        Settings.Save(MySet, settingsFile)

def ReloadSettings(jsonData):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsonData)

#---------------------------------------
# Usage functions
#---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

def TestLive():
    """Test going live settings by activating them"""
    emoteonly(MySet.emoteonly)
    subonly(MySet.subonly)
    r9k(MySet.r9k)
    slowmode(MySet.slowmode)
    followers(MySet.followers)
    unhost()
    message()

def TestOff():
    """Test going offline by activating them"""
    emoteonly(MySet.emoteonlyOFF)
    subonly(MySet.subonlyOFF)
    r9k(MySet.r9kOFF)
    slowmode(MySet.slowmodeOFF)
    followers(MySet.followersOFF)
    messageOFF()


#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global MySet
    global SettingsUpdated
    global isLive
    MySet = Settings(settingsFile)

    isLive = Parent.IsLive()

    if isLive:
        SettingsUpdated = True
    else:
        SettingsUpdated = False

def Tick():
    """Required tick function"""
    global SettingsUpdated
    isLive = Parent.IsLive()
    if not SettingsUpdated and isLive:
        emoteonly(MySet.emoteonly)
        subonly(MySet.subonly)
        r9k(MySet.r9k)
        slowmode(MySet.slowmode)
        followers(MySet.followers)
        unhost()
        message()
        SettingsUpdated = True

    if SettingsUpdated and not isLive:
        emoteonly(MySet.emoteonlyOFF)
        subonly(MySet.subonlyOFF)
        r9k(MySet.r9kOFF)
        slowmode(MySet.slowmodeOFF)
        followers(MySet.followersOFF)
        messageOFF()
        SettingsUpdated = False

def Execute(data):
    """Required Execute Data function"""

#---------------------------------------
# Update chat setting functions
#---------------------------------------
def emoteonly(state):
    """Toggle emoteonly on or off"""
    if state:
        Parent.SendTwitchMessage("/emoteonly")
    else:
        Parent.SendTwitchMessage("/emoteonlyoff")

def subonly(state):
    """Toggle subscriber only chat on or off"""
    if state:
        Parent.SendTwitchMessage("/subscribers")
    else:
        Parent.SendTwitchMessage("/subscribersoff")

def r9k(state):
    """Toggle r9kbeta on or off"""
    if state:
        Parent.SendTwitchMessage("/R9KBeta")
    else:
        Parent.SendTwitchMessage("/R9KBetaoff")

def slowmode(state):
    """Togggle slowmode on or off"""
    if state:
        Parent.SendTwitchMessage("/slow {0}".format(MySet.slowmodeinfo))
    else:
        Parent.SendTwitchMessage("/slowoff")

def followers(state):
    """Togggle slowmode on or off"""
    if state:
        Parent.SendTwitchMessage("/followers {0}".format(MySet.followersinfo))
    else:
        Parent.SendTwitchMessage("/followersoff")

def unhost():
    """Unhost when going live if enabled"""
    if MySet.unhost:
        Parent.SendTwitchMessage("/unhost")

def message():
    """Send message when going live if enabled"""
    if MySet.sendMessage:
        Parent.SendStreamMessage(MySet.message)

    if MySet.DsendMessage:

        url = "https://www.twitch.tv/" + Parent.GetChannelName()
        message = MySet.Dmessage.format(url)
        Parent.SendDiscordMessage(message)

def messageOFF():
    """Send message when going live if enabled"""
    if MySet.sendMessageOFF:
        Parent.SendStreamMessage(MySet.messageOFF)

    if MySet.DsendMessageOFF:

        url = "https://www.twitch.tv/" + Parent.GetChannelName()
        message = MySet.DmessageOFF.format(url)
        Parent.SendDiscordMessage(message)
