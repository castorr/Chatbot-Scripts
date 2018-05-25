#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Replica of streamelements roulette system"""
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
ScriptName = "SE Roulette"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.6"
Description = "Streamelements Roulette system"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.6 - Fixed user showing id for mixer
1.5 - Fixed Not enough currency response
1.4 - Added mixer support
1.3 - Added checking if amount gambled is an int, if not send info response
1.2 - Fixed more default values
1.1 - Fixed default values and typos
1.0 - Initial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
MessageBox = ctypes.windll.user32.MessageBoxW
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
            self.OnlyLive = False
            self.Command = "!roulette"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 60
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.NotEnoughResponse = "{0} you don't that many {1} to gamble!"
            self.WinResponse = "/me {0} won {1} {2} in roulette and now has {3} {2}! FeelsGoodMan"
            self.LoseResponse = "/me {0} lost {1} {2} in roulette and now has {3} {2}! FeelsBadMan"
            self.AllWin = "/me PogChamp {0} went all in and won {1} {2} PogChamp they now has {3} {2} FeelsGoodMan"
            self.AllLose = "/me {0} went all in and lost every single one of their {1} {2} LUL"
            self.PermissionResp = "{0} -> only {1} ({2}) and higher can use this command"
            self.InfoResponse = "{0} you have to chose a number without decimals to gamble, or use \"all\" to go all in!"

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
# [OPTIONAL] Settings functions
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

        if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
            message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
            SendResp(data, MySet.Usage, message)
            return

        if not MySet.OnlyLive or Parent.IsLive():
            if IsOnCooldown(data):
                return

            global gambleInt
            # check if user tried to bet all points
            if data.GetParam(1).lower() == "all":

                gambleInt = Parent.GetPoints(data.User)

            else:
                try:
                    gambleInt = int(data.GetParam(1))

                except ValueError:
                    message = MySet.InfoResponse.format(data.UserName)
                    SendResp(data, MySet.Usage, message)
                    return

            if Parent.GetPoints(data.User) < gambleInt:
                SendResp(data, MySet.Usage, MySet.NotEnoughResponse.format(data.UserName, Parent.GetCurrencyName()))
                return

            rungame(data)

def Tick():
    """Required tick function"""

#---------------------------------------
# [Optional] Functions for usage handling
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

def rungame(data):
    """function used to run the core functions of the game"""
    rollvalue = Parent.GetRandom(1, 3)

    if rollvalue == 1:
        loss(data)
    else:
        win(data)

    AddCooldowns(data)

def win(data):
    """function to handle losses"""
    global gambleInt
    Parent.AddPoints(data.User, gambleInt)

    currency = Parent.GetCurrencyName()
    points = Parent.GetPoints(data.User)

    if data.GetParam(1).lower() == "all":
        message = MySet.AllWin.format(data.UserName, gambleInt, currency, points)
    else:
        message = MySet.WinResponse.format(data.UserName, gambleInt, currency, points)

    SendResp(data, MySet.Usage, message)

def loss(data):
    """function to handle losses"""
    global gambleInt
    Parent.RemovePoints(data.User, gambleInt)
    currency = Parent.GetCurrencyName()
    points = Parent.GetPoints(data.User)

    if data.GetParam(1).lower() == "all":
        message = MySet.AllLose.format(data.UserName, gambleInt, currency, points)
    else:
        message = MySet.LoseResponse.format(data.UserName, gambleInt, currency, points)

    SendResp(data, MySet.Usage, message)

def AddCooldowns(data):
    """Function to add cooldowns for users"""
    # if user is caster and caster cooldown is ignored do nothing
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        # add cooldowns
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)

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
                SendResp(data, MySet.Usage, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)
        return True
    return False
