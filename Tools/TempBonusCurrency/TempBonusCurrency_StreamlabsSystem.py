#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Let viewers pay currency to boost currency payouts
for everyone in chat for x seconds"""
import json
import os
import time
import codecs
import winsound
import ctypes
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "TempBonusCurrency"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.1.3"
Description = "adds a command to temp boost the currency for all viewers"

#---------------------------------------
# Versions
#---------------------------------------
"""
1.1.3   - Added Mixer support
1.1.2   - Updated to work with chatbot 1.0.2.29 (Youtube release)
1.1.1   - Removed log spam
1.1.0   - Added usage options, fixed cooldowns, tweaked UI
1.0.4   - Fixed payouts not stopping on time
1.0.3   - Fixed sending messages
1.0.2   - Fixed payouts, added usage, changed version numbering
1.0.0.1 - Updated to work with AnkhBot 1.0.2.1
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
    """
    Tries to load settings from file if given
    The 'default' variable names need to match UI_Config"""
    def __init__(self, settingsFile=None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = "!bonus"
            self.Usage = "Stream Chat"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Cost = 300
            self.Payout = 15
            self.PayoutDuration = 300
            self.PayoutInterval = 30
            self.UseCD = True
            self.Cooldown = 305
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "{0} paid {1} to give everyone in chat {2} bonus {3} every {4} seconds for the next {5} seconds"
            self.NotEnoughResponse = "{0} you don't have enough {1}! "
            self.PermissionResp = "{0} -> only {1} ({2}) and higher can use this command"
            self.EnablePayoutResponse = False
            self.PayoutResponse = "Woop woop, another payout!"

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
# [Required] functions
#---------------------------------------
def Init():
    """Required tick function"""
    global MySet
    global m_Active
    m_Active = False
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
    """Required Execute function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():
        if not IsFromValidSource(data, MySet.Usage):
            return

        if MySet.OnlyLive and Parent.IsLive() is False:
            return

        if not HasPermission(data):
            return

        if MySet.Cost > Parent.GetPoints(data.User):
            message = MySet.NotEnoughResponse.format(data.UserName, Parent.GetCurrencyName())
            SendResp(data, MySet.Usage, message)
            return

        if IsOnCooldown(data):
            return

        Parent.RemovePoints(data.User, MySet.Cost)
        global m_Active
        m_Active = True
        global LastPayout
        LastPayout = time.time()
        global PayoutStart
        PayoutStart = time.time()

        cost = MySet.Cost
        payout = MySet.Payout
        currency = Parent.GetCurrencyName()
        message = MySet.BaseResponse.format(data.UserName, cost, payout, currency, MySet.PayoutInterval, MySet.PayoutDuration)

        SendResp(data, MySet.Usage, message)
        AddCooldowns(data)

def Tick():
    """Required tick function"""
    global m_Active
    if m_Active:
        global LastPayout
        global PayoutStart

        if time.time() - PayoutStart < MySet.PayoutDuration:
            if time.time() - LastPayout > MySet.PayoutInterval:

                myDict = {}
                for viewers in Parent.GetViewerList():
                    myDict[viewers] = MySet.Payout

                Parent.AddPointsAll(myDict)

                if MySet.EnablePayoutResponse:
                    Parent.SendTwitchMessage(MySet.PayoutResponse)

                LastPayout = time.time()

        else:
            m_Active = False

#---------------------------------------
# [Optional] Usage functions
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
# [Optional] Setting functions
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

def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.Reload(jsondata)

#---------------------------------------
# [Optional] Cooldown functions
#---------------------------------------
def AddCooldowns(data):
    """Function to add cooldowns for users"""
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
