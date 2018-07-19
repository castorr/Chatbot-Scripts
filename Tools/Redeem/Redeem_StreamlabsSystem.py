#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Redeem script to redeem rewards for a cost for users"""
#---------------------------------------
# Libraries and references
#---------------------------------------
from collections import deque
import codecs
import json
import os
import datetime
import ctypes
import winsound
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "Modules"))
from settingsmodule import Settings

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Redeem V2"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "2.0.0"
Description = "Right Click -> Insert API Key"

#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue = deque()
RewardFile = os.path.join(os.path.dirname(__file__), "Redeems.txt")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6

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
        Settings().Save(settingsFile)
        MessageBox(0, u"Settings successfully restored to default values"
                   , u"Reset complete!", 0)

def ReloadSettings(jsonData):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsonData)

#---------------------------------------
# UI functions
#---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    fullpath = os.path.join(AudioFilesPath, audiofile)
    AudioPlaybackQueue.append(fullpath)

def OpenSoundFolder():
    """Open specific sounds folder"""
    location = (os.path.dirname(os.path.realpath(__file__))) + "/sounds/"
    os.startfile(location)

def OpenFolder():
    """Open specific sounds folder"""
    location = (os.path.dirname(os.path.realpath(__file__)))
    os.startfile(location)

def OpenRedeems():
    """Open the Redeems.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "Redeems.txt")
    os.startfile(location)

def ResetRedeems():
    """Reset Redeems.txt file"""
    winsound.MessageBeep(-1)
    returnValue = MessageBox(0, u"You are about to reset the redeem file "
                                "are you sure you want to contine?"
                             , u"Reset redeem file?", 4)
    if returnValue == MB_YES:
        with open(RewardFile, "w") as f:
            f.write("")
            MessageBox(0, u"Redeem file successfully reset."
                       , u"Redeem file reset!", 0)

#---------------------------------------
# Optional functions
#---------------------------------------
def IsOnCooldown(data, command):
    """Handle cooldowns"""
    cooldown = Parent.IsOnCooldown(ScriptName, command)
    usercooldown = Parent.IsOnUserCooldown(ScriptName, command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.castercd)

    if (cooldown or usercooldown) and caster is False:

        if MySet.usecd:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, command, data.User)

            if cooldownDuration > userCDD:
                SendResp(data, MySet.oncooldown.format(data.UserName, cooldownDuration))

            else:
                SendResp(data, MySet.onusercooldown.format(data.UserName, userCDD))
        return False
    return True

def GetCommand(reward):
    """Get full command name for cooldown handling"""
    if MySet.ignoreredeem:
        return "!" + reward
    return MySet.command + " " + reward

def SendResp(data, message):
    """Sends message to Stream or discord chat depending on settings"""
    message = message.replace("$user", data.UserName)
    message = message.replace("$currencyname", Parent.GetCurrencyName())
    message = message.replace("$target", data.GetParam(1))

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(message)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, message)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordmessage(message)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, message)

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
    MySet = Settings(Parent, settingsFile)

def Execute(data):
    """Required Execute data function"""
    if (data.IsChatMessage() and data.GetParam(0).lower() == MySet.command.lower()) or MySet.ignoreredeem:

        if not IsFromValidSource(data, MySet.usage) or (MySet.onlylive and not data.IsLive()):
            return

        Parent.Log(ScriptName, str(MySet.ignoreredeem))
        if data.GetParamCount() < 2 and not MySet.ignoreredeem:
            SendResp(data, MySet.info.format(data.UserName))
            return

        if MySet.ignoreredeem:

            for x in range(1, 11):
                if data.GetParam(0).lower() == "!" + getattr(MySet, "r{0}".format(x)).lower():
                    Reward(data, x)
                    return

        if not MySet.ignoreredeem:
            for x in range(1, 11):
                if data.GetParam(1).lower() == getattr(MySet, "r{0}".format(x)).lower():
                    Reward(data, x)
                    return

        if data.GetParam(1).lower() == "list":
            SendResp(data, GetList(data))

        else:
            if not MySet.ignoreredeem:
                message = MySet.notavailable.format(data.UserName, data.GetParam(1))
                SendResp(data, message)

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue:
        if Parent.PlaySound(AudioPlaybackQueue[0], MySet.volume*0.01):
            AudioPlaybackQueue.popleft()

#---------------------------------------
# [Optional] Reward functions
#---------------------------------------
def redeem(data, sm, ps, bws, message, dump, SF, cost):
    """First redeem reward function"""
    if Parent.GetPoints(data.User) >= cost:
        if not MySet.onlylive or Parent.IsLive():
            if sm:
                message = message.format(data.UserName, cost, Parent.GetCurrencyName(), data.GetParam(2))
                SendResp(data, message)

            if bws:
                Parent.BroadcastWsEvent("EVENT_REDEEM", json.dumps(dump))

            if ps:
                EnqueueAudioFile(SF)
                SF = ""

            if MySet.stf:
                date = datetime.datetime.now().strftime("Date: %d/%m-%Y Time: %H:%M:%S")
                currency = Parent.GetCurrencyName()
                p1 = data.GetParam(1)
                p2 = data.GetParam(2)
                message = data.Message
                textline = MySet.textline.format(data.UserName, p1, cost, currency, date, p2, message)

                with codecs.open(RewardFile, "a", "utf-8") as f:
                    f.write(u"" + textline + "\n")

    else:
        currency = Parent.GetCurrencyName()
        points = Parent.GetPoints(data.User)
        message = MySet.notenough.format(data.UserName, cost, currency, points)
        SendResp(data, message)
        return False
    return True

def GetList(data):
    """Get list of all enabled rewards"""
    RewardList = getattr(MySet, "listbase")
    for x in range(1, 11):
        if getattr(MySet, "r{0}enabled".format(x)) and Parent.HasPermission(data.User, getattr(MySet, "r{0}permission".format(x)), getattr(MySet, "r{0}permissioninfo".format(x))):
            RewardList += (getattr(MySet, "r{0}".format(x)))
            if getattr(MySet, "listcost"):
                RewardList += ("(" + str(getattr(MySet, "r{0}cost".format(x))) + ")" + " - ")
    return RewardList

def HasPermission(data, permission, permissioninfo):
    """Return true or false dending on if the user has permission.
    Also sends permission response if user doesn't"""
    if not Parent.HasPermission(data.User, permission, permissioninfo):
        message = MySet.notperm.format(data.UserName, permission, permissionfnfo)
        SendResp(data, message)
        return False
    return True

def Reward(data, x):
    """Reward 1 setup function"""
    if not HasPermission(data, getattr(MySet, "r{0}permission".format(x)), getattr(MySet, "r{0}permissioninfo".format(x))):
        return

    command = GetCommand(getattr(MySet, "r{0}".format(x)))
    if getattr(MySet, "r{0}enabled".format(x)) and IsOnCooldown(data, command):
        a = getattr(MySet, "r{0}sm".format(x))
        b = getattr(MySet, "r{0}ps".format(x))
        c = getattr(MySet, "r{0}bws".format(x))
        e = getattr(MySet, "r{0}message".format(x))
        textalert = getattr(MySet, "r{0}text".format(x)).format(data.UserName, getattr(MySet, "r{0}cost".format(x)), getattr(MySet, "r{0}".format(x)))
        f = {"duration": getattr(MySet, "r{0}duration".format(x))*1000, "link": getattr(MySet, "r{0}giflink".format(x)), "text": textalert}
        g = getattr(MySet, "r{0}sound".format(x))
        h = getattr(MySet, "r{0}cost".format(x))

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, getattr(MySet, "r{0}usercooldown".format(x)))
            Parent.AddCooldown(ScriptName, command, getattr(MySet, "r{0}cooldown".format(x)))
