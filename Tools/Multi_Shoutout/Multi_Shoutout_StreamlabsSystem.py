#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Shoutout script to shout out one or multiple targets in an easy way"""
import json
import os
import codecs
import ctypes
import winsound
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Multi Shoutout"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.15"
Description = "Basic multi-shoutout, shoutout one or more at once"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

ICON_EXLAIM = 0x30
ICON_INFO = 0x40
ICON_STOP = 0x10
#---------------------------------------
# Versions
#---------------------------------------
"""
1.15
    Automatically removes @ in the links

1.14
    Fixed issues when not using seperators
    Fixed seperators default length
    Cleaned up cooldown and permission handling
    Fixed issue with reloading settings on save

1.13
    Added option for youtube
    Fixed cooldown bug
    Fixed caster ignore cooldown option

1.12
    Code cleanup
    Added usage options
    Changed version numbering (previous version 1.1.0.1)
    Tweaked UI functionality

1.1.0.1
    added option to extend the lines to fit new twitch formatting

1.1.0.0
    Made the code a lot smaller and cleaner
    Script now allow for more than 9 users
    Removed enable button in UI config
    added restore default button in UI config

1.0.0.1
    Updated to work with AnkhBot 1.0.2.1 and utf-8

1.0.0.0
    Inital release
"""
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
            self.Enabled = True
            self.OnlyLive = False
            self.Command = "!so"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Cost = 0
            self.Service = "Twitch"
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "/me go give these guys a follow <3 "
            self.Emotes = "Kappa Kappa Keepo Keepo"
            self.Seperator = True
            self.EndSeperator = True
            self.Extended = False
            self.Thick = False
            self.EndResponse = ""

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    # Save settings to files (json and js)
    def Save(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig', ensure_ascii=False)))

#---------------------------------------
# Setting functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    MessageBox = ctypes.windll.user32.MessageBoxW
    returnValue = MessageBox(None, u"You are about to reset the settings, "
                                   "are you sure you want to contine?"
                             , u"Reset settings file?", ICON_EXLAIM | 4)
    if returnValue == 6:

        MessageBox = ctypes.windll.user32.MessageBoxW
        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", ICON_INFO | 0)


        MySet = Settings()
        Settings.Save(MySet, settingsFile)

def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.Reload(jsondata)

#---------------------------------------
# Optional functions
#---------------------------------------
def SendResp(data, sendMessage):
    """Sends message to Stream or discord chat depending on settings"""
    if (data.IsFromTwitch() or data.IsFromYoutube()) and not data.IsWhisper():
        Parent.SendStreamMessage(sendMessage)

    if (data.IsFromTwitch() or data.IsFromYoutube()) and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, sendMessage)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(sendMessage)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, sendMessage)

def IsFromValidSource(data, rUsage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if data.IsFromTwitch() or data.IsFromYoutube():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (rUsage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (rUsage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (rUsage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (rUsage in l):
            return True

    return False

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """
    Required init function, read the settingsfile for saved settings.
    """
    global MySet
    MySet = Settings(settingsFile)

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        Save(MySet, settingsFile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        Save(MySet, settingsFile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        Save(MySet, settingsFile)


def Execute(data):
    """Required execute function"""
    if data.IsChatMessage() and data.GetParam(0) == MySet.Command:

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
            return

        if not MySet.OnlyLive or Parent.IsLive():

            if IsOnCooldown(data):
                return

            if data.GetParamCount() < 2:
                return

            else:
                LSeperator = " ▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬ "

                if MySet.Extended:
                    LSeperator = " ▬▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬▬ "

                if MySet.Thick:
                    LSeperator = " ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ "

                if MySet.Seperator:
                    MyStart = MySet.BaseResponse + LSeperator
                else:
                    MyStart = MySet.BaseResponse

                if MySet.EndSeperator:
                    MyEnd = LSeperator + MySet.EndResponse
                else:
                    MyEnd = MySet.EndResponse

                Shoutout = MyStart
                counter = 1

                #if MySet.Service == "Twitch":
                baseLink = "https://www.twitch.tv/"

                #if MySet.Service == "Youtube":
                #    baseLink = "www.youtube.com/"

                if data.GetParamCount() == 2:

                    while counter <= data.GetParamCount():
                        Shoutout += baseLink + data.GetParam(1) + " " + MySet.Emotes + " "
                        counter += 1

                else:
                    while counter <= data.GetParamCount() - 1:
                        Shoutout += baseLink + data.GetParam(counter)
                        Shoutout += " " + MySet.Emotes + " "
                        counter += 1

                Shoutout += MyEnd

                Shoutout = Shoutout.replace("@", "")

                SendResp(data, Shoutout)
                AddCooldowns(data)

def Tick():
    """Required tick function"""

def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    #introduce globals for cooldown management
    cooldown = Parent.IsOnCooldown(ScriptName, MySet.Command)
    userCooldown = Parent.IsOnUserCooldown(ScriptName, MySet.Command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    #check if command is on cooldown
    if (cooldown or userCooldown) and caster is False:

        #check if cooldown message is enabled
        if MySet.UseCD:

            #set variables for cooldown
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, MySet.Command, data.User)

            #check for the longest CD!
            if cooldownDuration > userCDD:

                #set cd remaining
                m_CooldownRemaining = cooldownDuration

                #send cooldown message
                message = MySet.OnCooldown.format(data.User, m_CooldownRemaining)
                SendResp(data, message)

            else: #set cd remaining
                m_CooldownRemaining = userCDD

                #send usercooldown message
                message = MySet.OnUserCooldown.format(data.User, m_CooldownRemaining)
                SendResp(data, message)
        return True
    return False

def AddCooldowns(data):
    """Function to add cooldowns for users"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
