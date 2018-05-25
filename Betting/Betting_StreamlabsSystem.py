#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Doc string"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
import time
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Betting"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.1"
Description = "Custom betting"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.2 - Fixed reset, now returning all points placed in the bet
1.1 - Added !win & !lose, added action to take on announcing winning option
1.0 - Initial Release
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

        else: #set variables if no custom settings file is found
            self.OnlyLive = False
            self.Command = "!bet"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.AutoClose = True
            self.Timer = 5
            self.AutoClear = True
            self.Action = "None"
            self.OpenMessage = "Betting is now opened! Use !win # or !lose # to bet on the outcome of this game"
            self.CloseMessage = "Betting is now closed!"
            self.WinBetMessage = "{0} placed a bet of {1} {2} on win FeelsGoodMan"
            self.LoseBetMessage = "{0} placed a bet of {1} {2} on lose FeelsBadMan"
            self.OutcomeLoseMessage = "The winning bet was lose. Payout: {0}"
            self.OutcomeWinMessage = "The winning bet was win. Payout: {0}"
            self.ResetMessage = "Bets have been cleared!"

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
# [Optional] UI buttons
#---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

    global BettingOpen
    BettingOpen = False

    reset()

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == "!bet":

        if MySet.OnlyLive and Parent.IsLive() is False:
            return

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not HasPermission(data):
            return

        if Parent.GetPoints(data.User) == 0:
            return

        global BettingOpen
        global TotalLosePoints
        global TotalLoseUsers
        global TotalWinPoints
        global TotalWinUsers

        if data.GetParam(1).lower() == "start" and Parent.HasPermission(data.User, "caster", ""):
            BettingOpen = True
            SendResp(data, MySet.OpenMessage)
            global BetOpenedAt
            BetOpenedAt = time.time()
            Parent.BroadcastWsEvent("EVENT_BET_STARTED", json.dumps({}))

        if data.GetParam(1).lower() == "close" and Parent.HasPermission(data.User, "caster", ""):
            BettingOpen = False
            SendResp(data, MySet.CloseMessage)
            Parent.BroadcastWsEvent("EVENT_BET_CLOSED", json.dumps({}))

        if data.GetParam(1).lower() == "reset" and Parent.HasPermission(data.User, "caster", ""):

            Parent.Log(ScriptName, str(LoseList))
            for user, value in LoseList.iteritems():
                LoseList[user] = int(value)/2
            Parent.Log(ScriptName, str(LoseList))
            Parent.Log(ScriptName, str(WinList))
            for user, value in WinList.iteritems():
                WinList[user] = int(value)/2
            Parent.Log(ScriptName, str(WinList))
            Parent.AddPointsAll(LoseList)
            Parent.AddPointsAll(WinList)

            reset()
            SendResp(data, MySet.ResetMessage)
            Parent.BroadcastWsEvent("EVENT_BET_RESET", json.dumps({}))

        if data.GetParam(1).lower() == "lost" and Parent.HasPermission(data.User, "caster", ""):
            BettingOpen = False
            Parent.AddPointsAll(LoseList)
            PayOutString = ""
            for user, value in LoseList.iteritems():
                PayOutString += "{0}({1}) -".format(user, value)
            message = MySet.OutcomeLoseMessage.format(PayOutString)
            SendResp(data, message)
            Parent.BroadcastWsEvent("EVENT_BET_OUTCOME", json.dumps({"winners": LoseList, "winningoption": "lose"}))
            if MySet.AutoClear:
                reset()
                SendResp(data, MySet.ResetMessage)
                Parent.BroadcastWsEvent("EVENT_BET_RESET", json.dumps({}))
            if MySet.Action == "Close Betting":
                BettingOpen = False
                SendResp(data, MySet.CloseMessage)
            elif MySet.Action == "Open New Betting":
                SendResp(data, MySet.OpenMessage)
                BetOpenedAt = time.time()


        if data.GetParam(1).lower() == "won" and Parent.HasPermission(data.User, "caster", ""):
            Parent.AddPointsAll(WinList)
            PayOutString = ""
            for user, value in WinList.iteritems():
                PayOutString += "{0}({1}) -".format(user, value)
            message = MySet.OutcomeWinMessage.format(PayOutString)
            SendResp(data, message)
            Parent.BroadcastWsEvent("EVENT_BET_OUTCOME", json.dumps({"winners": WinList, "winningoption": "win"}))
            if MySet.AutoClear:
                reset()
                SendResp(data, MySet.ResetMessage)
                Parent.BroadcastWsEvent("EVENT_BET_RESET", json.dumps({}))
            if MySet.Action == "Close Betting":
                BettingOpen = False
                SendResp(data, MySet.CloseMessage)
            elif MySet.Action == "Open New Betting":
                SendResp(data, MySet.OpenMessage)
                BetOpenedAt = time.time()

        if data.GetParam(1).lower() == "win" and HasPermission(data) and BettingOpen:
            if data.User in UsersList:
                return
            try:
                int(data.GetParam(2))
                if Parent.GetPoints(data.User) < int(data.GetParam(2)):
                    return
            except ValueError:
                return

            BetAmount = int(data.GetParam(2))
            TotalWinPoints += BetAmount
            TotalWinUsers += 1
            dump = {"userid": data.User, "username": data.UserName, "betsize": BetAmount, "betoption": "win", "totalwinbets": TotalWinUsers, "totalwinpoints": TotalWinPoints}
            Parent.BroadcastWsEvent("EVENT_NEW_BET_WIN", json.dumps(dump))
            UsersList.append(data.User)
            WinList[data.User] = BetAmount*2
            message = MySet.WinBetMessage.format(data.User, data.GetParam(2), Parent.GetCurrencyName())
            SendResp(data, message)
            Parent.RemovePoints(data.User, BetAmount)

        if data.GetParam(1).lower() == "!lose" and HasPermission(data) and BettingOpen:
            if data.User in UsersList:
                return

            try:
                int(data.GetParam(2))
                if Parent.GetPoints(data.User) < int(data.GetParam(2)):
                    return
            except ValueError:
                return

            BetAmount = int(data.GetParam(2))
            TotalLosePoints += BetAmount
            TotalLoseUsers += 1
            dump = {"userid": data.User, "username": data.UserName, "betsize": BetAmount, "betoption": "lose", "totallosebets": TotalLoseUsers, "totallosepoints": TotalLosePoints}
            Parent.BroadcastWsEvent("EVENT_NEW_BET_LOSE", json.dumps(dump))
            UsersList.append(data.User)
            LoseList[data.User] = BetAmount*2
            message = MySet.LoseBetMessage.format(data.User, data.GetParam(2), Parent.GetCurrencyName())
            SendResp(data, message)
            Parent.RemovePoints(data.User, BetAmount)


    if data.GetParam(0).lower() == "!win" and HasPermission(data) and BettingOpen:
        if data.User in UsersList:
            return
        try:
            int(data.GetParam(1))
            if Parent.GetPoints(data.User) < int(data.GetParam(1)):
                return
        except ValueError:
            return

        BetAmount = int(data.GetParam(1))
        TotalWinPoints += BetAmount
        TotalWinUsers += 1
        dump = {"userid": data.User, "username": data.UserName, "betsize": BetAmount, "betoption": "win", "totalwinbets": TotalWinUsers, "totalwinpoints": TotalWinPoints}
        Parent.BroadcastWsEvent("EVENT_NEW_BET_WIN", json.dumps(dump))
        UsersList.append(data.User)
        WinList[data.User] = BetAmount*2
        message = MySet.WinBetMessage.format(data.User, data.GetParam(1), Parent.GetCurrencyName())
        SendResp(data, message)
        Parent.RemovePoints(data.User, BetAmount)

    if data.GetParam(0).lower() == "!lose" and HasPermission(data) and BettingOpen:
        if data.User in UsersList:
            return

        try:
            int(data.GetParam(1))
            if Parent.GetPoints(data.User) < int(data.GetParam(1)):
                return
        except ValueError:
            return

        BetAmount = int(data.GetParam(1))
        TotalLosePoints += BetAmount
        TotalLoseUsers += 1
        dump = {"userid": data.User, "username": data.UserName, "betsize": BetAmount, "betoption": "lose", "totallosebets": TotalLoseUsers, "totallosepoints": TotalLosePoints}
        Parent.BroadcastWsEvent("EVENT_NEW_BET_LOSE", json.dumps(dump))
        UsersList.append(data.User)
        LoseList[data.User] = BetAmount*2
        message = MySet.LoseBetMessage.format(data.User, data.GetParam(1), Parent.GetCurrencyName())
        SendResp(data, message)
        Parent.RemovePoints(data.User, BetAmount)

def Tick():
    """Required tick function"""
    global BettingOpen
    if BettingOpen and MySet.AutoClose and (BetOpenedAt + MySet.Timer*60) < time.time():
        BettingOpen = False
        message = "Betting is now closed!"
        Parent.SendStreamMessage(message)
        Parent.BroadcastWsEvent("EVENT_BETSCLOSED", json.dumps({}))

#---------------------------------------
# [Optional] Functions for usage handling
#---------------------------------------
def SendResp(data, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)
    Message = Message.replace("$permission", MySet.Permission)

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, Message)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(Message)

    if data.IsFromDiscord() and data.IsWhisper():
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
# [Optional] Functions for permission handling
#---------------------------------------
def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        return False
    return True

def reset():
    """Reset betting numbers"""
    global UsersList
    UsersList = []

    global LoseList
    LoseList = {}

    global WinList
    WinList = {}

    global TotalLosePoints
    TotalLosePoints = 0

    global TotalWinPoints
    TotalWinPoints = 0

    global TotalWinUsers
    TotalWinUsers = 0

    global TotalLoseUsers
    TotalLoseUsers = 0
