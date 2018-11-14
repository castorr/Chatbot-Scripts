#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Simple Steal command, replica of the textbased version."""
# ---------------------------------------
# Libraries and references
# ---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
import random

# ---------------------------------------
# [Required] Script information
# ---------------------------------------
ScriptName = "Steal"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.1"
Description = "Simple steal command"
# ---------------------------------------
# Versions
# ---------------------------------------
""" Releases (open README.txt for full release notes)
1.1 - Fixed cooldowns, added mixer & youtube support
1.0 - Initial Release
"""
# ---------------------------------------
# Variables
# ---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")


# ---------------------------------------
# Classes
# ---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else:  # set variables if no custom settings file is found
            self.OnlyLive = False
            self.Command = "!steal"
            self.Cost = 10
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.NotEnoughResponse = "{0} you don't have enough {1} to attempt this!"
            self.WinResponse = "{0} managed to steal {1} {2} from {3}"
            self.LoseResponse = "{0} tried to steal some {1} from {2} but {0} got rekt and {2} managed to steal {3} {1} from {0} instead!"
            self.PermissionResp = "{0} -> only {1} ({2}) and higher can use this command"
            self.InfoResponse = "{0} you have to chose a target to try to steal from"
            self.NotHere = "{0} you can only steal from users who are currently in the viewerlist and that got at least {1} {2}. They can however get some free {2} if you try!"
            self.Max = 112
            self.Min = 32
            self.Protected = True
            self.Timeout = False
            self.TL = 60

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig', ensure_ascii=False)))
        return


# ---------------------------------------
# [OPTIONAL] Settings functions
# ---------------------------------------
def SetDefaults():
    """Set default settings function"""

    # play windows sound
    winsound.MessageBeep()

    # open messagebox with a security check
    MessageBox = ctypes.windll.user32.MessageBoxW
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    # if user press "yes"
    if returnValue == 6:
        # Save defaults back to file
        Settings.SaveSettings(MySet, settingsFile)

        # show messagebox that it was complete
        MessageBox = ctypes.windll.user32.MessageBoxW
        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)


# ---------------------------------------
# [Required] functions
# ---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)


def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not HasPermission(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():

            if IsOnCooldown(data):
                return

            if data.GetParamCount() < 2:
                message = MySet.InfoResponse.format(data.UserName)
                return

            if Parent.RemovePoints(data.User, data.UserName, MySet.Cost):
                if data.GetParam(1).lower == Parent.GetChannelName().lower and Myset.Protected:
                    value = Parent.GetRandom(MySet.Min, MySet.Max)
                    Parent.RemovePoints(data.User, data.UserName, value)
                    message = MySet.LoseResponse.format(data.UserName, Parent.GetCurrencyName(), value, data.GetParam(1))
                    AddCooldown(data)
                    return

                outcome = Parent.GetRandom(1, 3)
                viewer_dict = Parent.GetDisplayNames(Parent.GetViewerList())
                user_name = data.GetParam(1)
                user_id = [key for key, value in viewer_dict.iteritems() if value == user_name][0]

                if outcome == 1:
                    value = Parent.GetRandom(MySet.Min, MySet.Max)
                    Parent.RemovePoints(data.User, data.UserName, value)
                    Parent.AddPoints(user_id, user_name, value)
                    message = MySet.LoseResponse.format(data.UserName, Parent.GetCurrencyName(), user_name, value)
                    SendResp(data, message)
                    AddCooldown(data)
                    if MySet.Timeout:
                        Parent.SendStreamMessage("/timeout {0} {1}".format(data.User, MySet.TL))
                    return

                elif outcome == 2:
                    value = Parent.GetRandom(MySet.Min, MySet.Max)
                    if not Parent.RemovePoints(user_id, user_name, value):
                        message = MySet.NotHere.format(data.UserName, MySet.Min, Parent.GetCurrencyName())
                        SendResp(data, message)
                        return
                    Parent.AddPoints(data.User, data.UserName, value)
                    message = MySet.WinResponse.format(data.UserName, value, Parent.GetCurrencyName(), user_name)
                    SendResp(data, message)
                    AddCooldown(data)
                    return

                else:
                    message = "Shit went wrong #blameCastorr #blamePowerclan"
                    SendResp(data, message)
            else:
                message = MySet.NotEnoughResponse.format(data.UserName, Parent.GetCurrencyName())
                SendResp(data, message)


def Tick():
    """Required tick function"""
    pass


# ---------------------------------------
# [Optional] Functions for usage handling
# ---------------------------------------
def SendResp(data, sendMessage):
    """Sends message to Stream or discord chat depending on settings"""

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(sendMessage)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, sendMessage)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(sendMessage)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, sendMessage)


def CheckUsage(data, rUsage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""

    if not data.IsFromDiscord():
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


def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    cooldown = Parent.IsOnCooldown(ScriptName, MySet.Command)
    userCooldown = Parent.IsOnUserCooldown(ScriptName, MySet.Command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    if (cooldown or userCooldown) and caster is False:

        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, MySet.Command, data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration

                message = MySet.OnCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)
        return True
    return False


def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, message)
        return False
    return True


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


def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
