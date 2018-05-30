#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Gamble game with lot of variation and customization to fit most streamers"""
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
ScriptName = "Gamble"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "2.1.7"
Description = "Gamble minigame"
#---------------------------------------
# Versions
#---------------------------------------
""" Major and recent Releases (open README.txt for full release notes)
2.1.7   - Fixed issues with saving and loading some settings, mainly jackpot amount
2.1.6   - Fixed username showing as userid for certain responses
2.1.5   - Fixed $permissioninfo
        - Added no currency response
2.1.4   - Fixed jackpot reset
2.1.3   - Added mixer support
2.1.2   - Fixed permissions
2.1.1   - Fixed saving to settings file with non ascii characters
        - Improved readability
        - Fixed revlo advanced
2.1.0   - Fixed payouts for Revlo Advanced
        - Fixed Max Bet ammount for Single Number
        - Added functions for the different outcomes
        - Added functions to handle all checks
        - Added button to copy index.html filepath to clipboard
        - Fixed automatic reloading on save
        - Fixed usernames for youtube

2.0.0.0 - Added 5 gamemodes and lots of options
1.0.0.0 - Initial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")
jackpotFile = os.path.join(os.path.dirname(__file__), "jackpot.txt")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsfile=None):
        if settingsfile and os.path.isfile(settingsfile):
            with codecs.open(settingsfile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no custom settings file is found
            self.OnlyLive = False
            self.Command = "!gamble"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Mode = "Revlo"
            self.Usage = "Stream Chat"
            self.AllWord = "all"
            self.ForceAll = False
            self.UseRandom = False
            self.RandomMax = 1
            self.RandomMin = 100
            self.Jackpot = 500
            self.JackpotEnabled = False
            self.JackpotNumber = 100
            self.JackpotPercentage = 50
            self.JackpotBase = 500
            self.JackpotCheck = True
            self.JackpotWord = "jackpot"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "Rolled {0}. "
            self.NotEnoughResponse = "{0} you don't have that many {1} to gamble! "
            self.WinResponse = "{0} won {1} {3} and now has {2} {3} "
            self.LoseResponse = "{0} lost {1} {3} and now has {2} {3} "
            self.TooMuchResponse = "{0} you can't gamble more than {1} {2}"
            self.TooLowResponse = "{0} you can't gamble less than {1} {2}"
            self.InfoResponse = "To gamble use !gamble <amount>"
            self.PermissionResp = "$user -> only $permission ($permissioninfo) and higher can use this command"
            self.JackpotWin = "{0} won the jackpot of {1} {3} and now has a total of {2} {3}"
            self.JackpotResponse = "There's currently {0} {1} in the jackpot!"
            self.MinValue = 0
            self.MaxValue = 100
            self.WinChance = 40
            self.TripleWinEnabled = True
            self.TripleChance = 2
            self.MinBet = 1
            self.MaxBet = 9999
            self.RMinValue = 1
            self.RMaxValue = 100
            self.RWinChance = 40
            self.RMinBet = 1
            self.RMaxBet = 9999
            self.PMinValue = 0
            self.PMaxValue = 100
            self.PMinBet = 1
            self.PMaxBet = 9999
            self.SMinValue = 0
            self.SMaxValue = 100
            self.SMinBet = 1
            self.SMaxBet = 9999
            self.SWinNumbers = "42 69 100"
            self.SMultiplier = 30
            self.CMaxBet = 0
            self.CMinBet = 0
            self.NoZero = "{0} -> You are not allowed to roll anything less than 1!"
            self.NoCurrency = "{0} -> You don't have any currency to gamble!"

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
        Settings.Save(MySet, settingsfile)

def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    Init()

def SaveSettings():
    """Save settings on pressing the save button"""
    Settings.Save(MySet, settingsfile)
    jackpot = MySet.Jackpot

    with open(jackpotFile, "w+") as f:
        f.write(str(jackpot))

#---------------------------------------
# Optional functions
#---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)
    Message = Message.replace("$permission", MySet.Permission)

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

def ControlC():
    """Copy index.html filepath to clipboard"""
    """    winsound.MessageBeep()
        returnValue = MessageBox(0, u"You are about copy the index.html filepath "
                                    "to your clipboard, this will overwrite any "
                                    "information you have there now. "
                                    "Are you sure you want to contine?"
                                , u"Copy to clipboard", 4)
        if returnValue == 6:
            indexPath = os.path.dirname(os.path.abspath(__file__)) + "\\index.html"
            command = 'echo ' + indexPath.strip() + '| clip'
            os.system(command)
    """
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"This is just a placeholder.\r\nWanna open another box?"
                             , u"Open another window?", 4)
    if returnValue == 6:
        returnValue = MessageBox(0, u"Here's your box, now you gotta be happy!"
                                 , u"Happy now?", 0)        
#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsfile)

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        Settings.Save(MySet, settingsfile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        Settings.Save(MySet, settingsfile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        Settings.Save(MySet, settingsfile)

    global jackpot
    jackpot = MySet.Jackpot

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if Parent.GetPoints(data.User) == 0:
            message = MySet.NoCurrency.format(data.UserName)
            SendResp(data, MySet.Usage, message)
            return

        if not HasPermission(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():

            if IsOnCooldown(data):
                return

            if data.GetParamCount() < 2 and not MySet.UseRandom:

                SendResp(data, MySet.Usage, MySet.InfoResponse)
                return

            global gambleInt
            gambleInt = data.GetParam(1)

            try:
                int(gambleInt)
                if int(gambleInt) < 1:
                    SendResp(data, MySet.Usage, MySet.NoZero.format(data.UserName))
                    return

            except ValueError:
                setBet = MySet.UseRandom or MySet.ForceAll

                if data.GetParam(1).lower() == MySet.AllWord.lower() and not setBet:
                    gambleInt = Parent.GetPoints(data.User)

                elif data.GetParam(1).lower() == MySet.JackpotWord and MySet.JackpotCheck:

                    message = MySet.JackpotResponse.format(jackpot, Parent.GetCurrencyName())
                    SendResp(data, MySet.Usage, message)
                    return

                else:
                    return

            if MySet.UseRandom:

                maxRandom = int(Parent.GetPoints(data.User)*MySet.RandomMax/100)
                minRandom = int(Parent.GetPoints(data.User)*MySet.RandomMin/100)
                gambleInt = Parent.GetRandom(minRandom, maxRandom+1)

            if MySet.ForceAll:
                gambleInt = Parent.GetPoints(data.User)

            try:
                gambleInt = int(gambleInt)

            except ValueError:
                pass

            if MySet.Mode == "Revlo":
                Revlo(data)

            elif MySet.Mode == "Revlo Advanced":
                RevloAdvanced(data)

            elif MySet.Mode == "Random":
                Random(data)

            elif MySet.Mode == "Percentage":
                Percentage(data)

            elif MySet.Mode == "Single Number":
                SingleNumber(data)

def Tick():
    """Required tick function"""

#---------------------------------------
# Functions for all game modes
#---------------------------------------
def Revlo(data):
    """Revlo game mode function"""
    global gambleInt
    if Parent.GetPoints(data.User) < gambleInt:
        NotEnoughResp(data)
        return

    rollValue = Parent.GetRandom(1, 101)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    if int(rollValue) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, rollValue, gambleInt)
        return

    if rollValue >= 99:
        HandleTripleWin(data, rollValue, gambleInt)

    elif rollValue >= 61:
        HandleWin(data, rollValue, gambleInt, 2)

    else:
        HandleLoss(data, rollValue, gambleInt)

    AddCooldown(data)

def RevloAdvanced(data):
    """Revlo Advanced game mode function"""
    if MySet.MaxBet < gambleInt and MySet.MaxBet != 0:
        MaxBetResp(data, MySet.MaxBet)
        return

    if MySet.MinBet > gambleInt:
        MinBetResp(data, MySet.MinBet)
        return

    if Parent.GetPoints(data.User) < gambleInt:
        NotEnoughResp(data)
        return

    rollValue = Parent.GetRandom(MySet.MinValue, MySet.MaxValue+1)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    tripleWin = MySet.MaxValue-MySet.MaxValue*MySet.TripleChance/100

    if int(rollValue) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, rollValue, gambleInt)
        return

    if rollValue > tripleWin and MySet.TripleWinEnabled:
        HandleTripleWin(data, rollValue, gambleInt)

    elif rollValue > int(MySet.MaxValue-MySet.MaxValue*MySet.WinChance/100):
        HandleWin(data, rollValue, gambleInt, 2)

    else:
        HandleLoss(data, rollValue, gambleInt)

    AddCooldown(data)

def Random(data):
    """Random game mode function"""
    #check if amount gambled is more than max bet allowed
    if MySet.RMaxBet < gambleInt and MySet.RMaxBet != 0:
        MaxBetResp(data, MySet.RMaxBet)
        return

    if MySet.RMinBet > gambleInt:
        MinBetResp(data, MySet.RMinBet)
        return

    if Parent.GetPoints(data.User) < gambleInt:
        NotEnoughResp(data)
        return

    rollValue = Parent.GetRandom(MySet.RMinValue, MySet.RMaxValue+1)
    RrollValue = Parent.GetRandom(1, 100)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    if int(rollValue) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, rollValue, gambleInt)
        return

    if RrollValue >= 100-MySet.RWinChance:
        HandleWin(data, rollValue, gambleInt, 2)

    else:
        HandleLoss(data, rollValue, gambleInt)

    AddCooldown(data)

def Percentage(data):
    """Percentage game mode function"""
    if MySet.PMaxBet < gambleInt and MySet.PMaxBet != 0:
        MaxBetResp(data, MySet.PMaxBet)
        return

    if MySet.PMinBet > gambleInt:
        MinBetResp(data, MySet.PMinBet)
        return

    if Parent.GetPoints(data.User) < gambleInt:
        NotEnoughResp(data)
        return

    rollValue = Parent.GetRandom(MySet.PMinValue, MySet.PMaxValue+1)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    if int(rollValue) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, rollValue, gambleInt)
        return

    pPayout = float(rollValue*2.000/100)

    Parent.AddPoints(data.User, data.UserName, int(gambleInt*pPayout))

    if pPayout > 1:
        points = Parent.GetPoints(data.User)
        currency = Parent.GetCurrencyName()
        newBalance = int(gambleInt*pPayout-gambleInt)
        winMessage = MySet.WinResponse.format(data.UserName, newBalance, points, currency)

        SendResp(data, MySet.Usage, MySet.BaseResponse.format(rollValue, data.UserName) + winMessage)

    else:
        global jackpot
        jackpot += int(gambleInt*MySet.JackpotPercentage/100)
        MySet.Jackpot = jackpot
        Settings.Save(MySet, settingsfile)

        with open(jackpotFile, "w+") as f:
            f.write(str(jackpot))

        points = Parent.GetPoints(data.User)
        currency = Parent.GetCurrencyName()
        newBalance = abs(int(gambleInt*pPayout-gambleInt))
        loseMessage = MySet.LoseResponse.format(data.UserName, newBalance, points, currency)

        SendResp(data, MySet.Usage, MySet.BaseResponse.format(rollValue, data.UserName) + loseMessage)

    AddCooldown(data)

def SingleNumber(data):
    """Single number game mode function"""
    if MySet.SMaxBet < gambleInt and MySet.SMaxBet != 0:
        MaxBetResp(data, MySet.SMaxBet)
        return

    if MySet.SMinBet > gambleInt:
        MinBetResp(data, MySet.SMinBet)
        return

    if Parent.GetPoints(data.User) < gambleInt:
        NotEnoughResp(data)
        return

    rollValue = Parent.GetRandom(MySet.SMinValue, MySet.SMaxValue+1)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    numbersList = MySet.SWinNumbers.split(" ")

    winCheck = False

    for number in numbersList:
        if number == str(rollValue):
            winCheck = True

    if int(rollValue) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, rollValue, gambleInt)
        return

    if winCheck:
        HandleWin(data, rollValue, gambleInt, MySet.SMultiplier)

    else:
        HandleLoss(data, rollValue, gambleInt)

    AddCooldown(data)

#---------------------------------------
# Game functions
#---------------------------------------
def MaxBetResp(data, maxbet):
    """Send message about maximum bet size"""
    currency = Parent.GetCurrencyName()
    maxBetMessage = MySet.TooMuchResponse.format(data.UserName, maxbet, currency)

    SendResp(data, MySet.Usage, maxBetMessage)

def MinBetResp(data, minbet):
    """Send message about minimum bet size"""
    currency = Parent.GetCurrencyName()
    minBetMessage = MySet.TooLowResponse.format(data.UserName, minbet, currency)

    SendResp(data, MySet.Usage, minBetMessage)

def NotEnoughResp(data):
    """Send message about not having enough currency"""
    currency = Parent.GetCurrencyName()
    notEnough = MySet.NotEnoughResponse.format(data.UserName, currency, MySet.Command)
    SendResp(data, MySet.Usage, notEnough)

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

#---------------------------------------
# Game outcomes
#---------------------------------------
def HandleJackpot(data, roll, bet):
    """Handle jackpot"""
    global jackpot
    Parent.AddPoints(data.User, data.UserName, bet)
    Parent.AddPoints(data.User, data.UserName, jackpot)

    points = Parent.GetPoints(data.User)
    currency = Parent.GetCurrencyName()
    jackpotMessage = MySet.JackpotWin.format(data.UserName, jackpot, points, currency)
    message = MySet.BaseResponse.format(roll, data.UserName)
    SendResp(data, MySet.Usage, message + jackpotMessage)

    MySet.Jackpot = MySet.JackpotBase
    Settings.Save(MySet, settingsfile)
    jackpot = MySet.Jackpot

    with open(jackpotFile, "w+") as f:
        f.write(str(jackpot))

def HandleTripleWin(data, roll, bet):
    """Handle triple wins!"""
    Parent.AddPoints(data.User, data.UserName, bet*3)

    points = Parent.GetPoints(data.User)
    currency = Parent.GetCurrencyName()
    winMessage = MySet.WinResponse.format(data.UserName, bet*3, points, currency)

    SendResp(data, MySet.Usage, MySet.BaseResponse.format(roll, data.UserName) + winMessage)

def HandleWin(data, roll, bet, multiplier):
    """Handle wins, adding points and sending message"""
    Parent.AddPoints(data.User, data.UserName, bet*multiplier)

    points = Parent.GetPoints(data.User)
    currency = Parent.GetCurrencyName()
    winMessage = MySet.WinResponse.format(data.UserName, bet*multiplier, points, currency)

    SendResp(data, MySet.Usage, MySet.BaseResponse.format(roll, data.UserName) + winMessage)

def HandleLoss(data, roll, bet):
    """Handle loss message"""
    global jackpot
    global MySet

    jackpot += int(bet*MySet.JackpotPercentage/100)
    MySet.Jackpot = jackpot
    MySet.Save(settingsfile)

    with open(jackpotFile, "w+") as f:
        f.write(str(jackpot))

    points = Parent.GetPoints(data.User)
    currency = Parent.GetCurrencyName()
    loseMessage = MySet.LoseResponse.format(data.UserName, bet, points, currency, MySet.Jackpot)

    SendResp(data, MySet.Usage, MySet.BaseResponse.format(roll, data.UserName) + loseMessage)
