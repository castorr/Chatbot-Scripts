#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Extra parameters including a bunch from Nightbot"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Close Spotify"
Website = "https://www.Stream.tv/castorr91"
Creator = "Castorr91"
Version = "1.3"
Description = "Allows shutdown of Spotify through command"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.3     - Added mixer support
1.2     - Fixed non ascii characters, added comments
1.1     - Updated to work with chatbot 1.0.2.29 (Youtube Update)
1.0.0.0 - Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
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
            self.Command = "!shutdown"
            self.Usage = "Stream Chat"
            self.Permission = "Caster"
            self.PermissionInfo = ""
            self.message = "{0} -> Spotify is now shutting down!"

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
def ReloadSettings(jsondata):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsondata)

#---------------------------------------
# Usage function
#---------------------------------------
def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$permission", MySet.Permission)
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)

    l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and (Usage in l) and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendStreamWhisper(data.User, Message)

    l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
    if data.IsFromDiscord() and not data.IsWhisper() and (Usage in l):
        Parent.SendDiscordMessage(Message)

    l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
    if data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendDiscordDM(data.User, Message)

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

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        SaveSettings(MySet, settingsFile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        SaveSettings(MySet, settingsFile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        SaveSettings(MySet, settingsFile)

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():
        if not IsFromValidSource(data, MySet.Usage):
            return

        HasPerm = Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo)
        if HasPerm:
            message = MySet.message.format(data.UserName)
            SendResp(data, MySet.Usage, message)

            os.system("taskkill /f /im  Spotify.exe")

def Tick():
    """Required tick function"""
