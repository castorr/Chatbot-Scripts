#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Roulette minigame for chat only so far!"""
# Import Libraries
import codecs
import json
import os
import winsound
import ctypes
#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Roulette"
Website = "https://www.AnkhBot.com"
Creator = "Castorr91"
Version = "1.1.3"
Description = "Roulette minigame"
#---------------------------------------
# Versions
#---------------------------------------
"""
    1.1.3 - Hotfixed usernames for mixer
    1.1.2 - Added mixer support
    1.1.1 - Updated to work with youtube.
    1.1.0 - Complete code overhaul, fixed permission settings, added usage options
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
    """ Tries to load settings from file if given"""
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = "!roulette"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.MaxBet = 0
            self.MinBet = 0
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "{0} spins the roulette and it lands on {2} {1} ... "
            self.NotEnoughResponse = "{0} you don't have that many {1} to gamble! "
            self.WinResponse = "{0} won {1} {3} and now has {2} {3} "
            self.LoseResponse = "{0} lost {1} {3} and now has {2} {3} "
            self.TooMuchResponse = "{0} you can't gamble more than {1} {2}"
            self.TooLowResponse = "{0} you can't gamble less than {1} {2}"
            self.PermissionResp = "{0} -> only {1} ({2}) and higher can use this command"
            self.InfoResponse = "To spin the roulette use !Roulette [option] [amount].Available options to bet on: high, low, red, black, even, odd, zero, basket, dozen1-3, column1-3, any single number.For more information on the payout amounts check this link: http://imgur.com/a/uu1Yf"

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

#---------------------------------------
#	[Required] Functions
#---------------------------------------
def Init():
    """ Initial loading function """
    global counter
    counter = 0
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
    """Execute Data / Process Messages"""
    if data.IsChatMessage() and data.GetParam(0) == MySet.Command:

        if MySet.OnlyLive and Parent.IsLive() is False:
            return

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not HasPermission(data):
            return

        if IsOnCooldown(data):
            return

        if Parent.GetPoints(data.User) == 0:
            return

        options = ("black", "red", "green", "odd", "even", "high", "low", "zero",
                   "basket", "dozen1", "dozen2", "dozen3", "column1", "column2",
                   "column3", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                   "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                   "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
                   "33", "34", "35", "36")
        if data.GetParamCount() < 3 or data.GetParam(1).lower() not in options:
            SendResp(data, MySet.Usage, MySet.InfoResponse)
            return

        global gambleInt
        if data.GetParam(2).lower() == "all":
            gambleInt = Parent.GetPoints(data.User)

        else:
            try:
                int(data.GetParam(2))

            except ValueError:
                SendResp(data, MySet.Usage, MySet.InfoResponse)
                return

        gambleInt = int(data.GetParam(2))
        Parent.Log(ScriptName, str(gambleInt))
        if MySet.MaxBet < gambleInt and MySet.MaxBet != 0:
            currencyname = Parent.GetCurrencyName()
            message = MySet.TooMuchResponse.format(data.UserName, MySet.MaxBet, currencyname)

            SendResp(data, MySet.Usage, message)
            return

        if MySet.MinBet > gambleInt:
            currencyname = Parent.GetCurrencyName()
            message = MySet.TooLowResponse.format(data.UserName, MySet.MinBet, currencyname)

            SendResp(data, MySet.Usage, message)
            return

        if Parent.GetPoints(data.User) < gambleInt:
            currencyname = Parent.GetCurrencyName()
            message = MySet.NotEnoughResponse.format(data.UserName, currencyname, MySet.Command)

            SendResp(data, MySet.Usage, message)
            return

        rungame(data)

def Tick():
    """Required tick function"""

#---------------------------------------
#	[Optional] Usage functions
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
#	Game functions
#---------------------------------------
def rungame(data):
    """Runs the game if all the requirements were met"""
    global rollValue
    rollValue = int(Parent.GetRandom(0, 36))

    global colorValue
    if rollValue in (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36):
        colorValue = "red"

    elif rollValue in (2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35):
        colorValue = "black"

    else:
        colorValue = "green"

    if data.GetParam(1).lower() == "odd":
        if rollValue in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35):
            Win(data, gambleInt)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "even":
        if rollValue in (2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36):
            Win(data, gambleInt)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "black":
        if colorValue == "black":
            Win(data, gambleInt)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "red":
        if colorValue == "red":
            Win(data, gambleInt)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "green":
        if colorValue == "green":
            Win(data, gambleInt*35)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "high":
        if rollValue > 16:
            Win(data, gambleInt)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "low":
        if rollValue < 17 and rollValue != 0:
            Win(data, gambleInt)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == str(rollValue):
        Win(data, gambleInt*35)

    elif data.GetParam(1).lower() == "dozen1":
        if rollValue < 13 and rollValue != 0:
            Win(data, gambleInt*2)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "dozen2":
        if rollValue > 12 and rollValue < 24:
            Win(data, gambleInt*2)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "dozen3":
        if rollValue > 24:
            Win(data, gambleInt*2)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "column1":
        if rollValue in (1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34):
            Win(data, gambleInt*2)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "column2":
        if rollValue in (2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35):
            Win(data, gambleInt*2)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "column3":
        if rollValue in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36):
            Win(data, gambleInt*2)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "basket":
        if rollValue <= 3:
            Win(data, gambleInt*6)

        else:
            Loss(data, gambleInt)

    elif data.GetParam(1).lower() == "zero":
        if rollValue == 0:
            Win(data, gambleInt*6)

        else:
            Loss(data, gambleInt)

    else:
        Loss(data, gambleInt)

    AddCooldown(data)

def Loss(data, pointslost):
    """message handling on loss"""
    global rollValue
    global colorValue
    Parent.RemovePoints(data.User, data.UserName, pointslost)
    base = MySet.BaseResponse.format(data.UserName, rollValue, colorValue, pointslost)
    newbalance = Parent.GetPoints(data.User)
    currencyname = Parent.GetCurrencyName()
    lose = MySet.LoseResponse.format(data.UserName, pointslost, newbalance, currencyname)
    message = (base + lose)
    SendResp(data, MySet.Usage, message)

def Win(data, amount):
    """message and points handling on win"""
    global rollValue
    global colorValue
    Parent.AddPoints(data.User, data.UserName, amount)
    base = MySet.BaseResponse.format(data.UserName, rollValue, colorValue, amount)
    newbalance = Parent.GetPoints(data.User)
    win = MySet.WinResponse.format(data.UserName, amount, newbalance, Parent.GetCurrencyName())
    message = (base + win)
    SendResp(data, MySet.Usage, message)

def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
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

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, MySet.Usage, message)
        return False
    return True
