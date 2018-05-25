#!/usr/bin/python
# -*- encoding: utf-8 -*-
# pylint: disable=invalid-name
"""Make it rain command to allow users to pay a
 cost to make it rain currency for all viewers in chat"""
#---------------------------------------
# Import Libraries
#---------------------------------------
from collections import deque
import json
import os
import codecs
import ctypes
import winsound
#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "MakeItRain"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.2.8"
Description = "Right Click -> Insert Api Key | Make it rain!"

#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue = deque()
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
#---------------------------------------
# Versions
#---------------------------------------
"""Versions: (major updates only, see readme.txt for full changelog)
    1.2.8
    - Fixed cost for mixer
    - Fixed default response when user have insufficient funds

    1.2.7
    - Fixed usernames for mixer
    1.2.6
    - Added mixer support

    1.2.3
    - Updated to work with chatbot 1.0.2.29

    1.2.0.0
    - Added sound and gif playback on successful trigger
    - Fixed cooldown handling
    - Cleaned up GetUsage
    - Added functions for command handling
    - Removed unnecessary libraries
    - Added buttons in UI to open soundsfolder & locate index.html

    1.0.0.0
        Official Release
    """

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """Settings class to handle settings from file and use default if no file is found"""

    def __init__(self, settingsFile=None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')
        else: #set variables if no settings file
            self.OnlyLive = False
            self.Command = "!makeitrain"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.Cost = 300
            self.UseCD = True
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "{0} just spent {1} {3} to make it rain! Everyone in chat got awarded {2} {3}!"
            self.NotEnoughResponse = "{0} you don't have enough points to make it rain"
            self.PermissionResp = "$user -> only $permission ($permissioninfo) and higher can use this command"
            self.Payout = 30
            self.Random = False
            self.Min = 10
            self.Max = 50
            self.PS = False
            self.SF = "test.mp3"
            self.Volume = 50
            self.BWS = False
            self.Gif = "https://media3.giphy.com/avatars/100soft/WahNEDdlGjRZ.gif"
            self.Duration = 5

    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        fullpath = os.path.join(AudioFilesPath, MySet.SF)
        if not (fullpath and os.path.isfile(fullpath)) and MySet.PS:
            returnValue = MessageBox(0, u"Couldn't find the specified soundfile."
                                        "\r\nMake sure the name is correct and that "
                                        "the file is located in the sounds folder"
                                        "\r\n\r\nDo you want to open the sounds folder now?"
                                     , u"File not found", 4)
            if returnValue == 6:
                OpenSoundsFolder()
            return


    def Save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False, indent=4)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False, indent=4)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------------------
# Required functions
#---------------------------------------
def Init():
    """Required init function"""
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
    """Required execute function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():
        if MySet.OnlyLive and Parent.IsLive() is False:
            return

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not HasPermission(data):
            return

        if IsOnCooldown(data):
            return

        if Parent.GetPoints(data.User) < MySet.Cost:
            NotEnoughResp(data)
            return

        Parent.RemovePoints(data.User, data.UserName, MySet.Cost)

        global PayoutAmount
        PayoutAmount = MySet.Payout

        if MySet.Random:
            PayoutAmount = Parent.GetRandom(MySet.Min, MySet.Max)

        AddPointsAll(data, PayoutAmount)

        fullpath = os.path.join(AudioFilesPath, MySet.SF)
        if MySet.PS and fullpath and os.path.isfile(fullpath):
            EnqueueAudioFile(MySet.SF)

        if MySet.BWS:
            dump = {"duration": MySet.Duration*1000, "link": MySet.Gif}
            Parent.BroadcastWsEvent("EVENT_MAKE_IT_RAIN", json.dumps(dump))

        AddCooldowns(data)

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue:
        if Parent.PlaySound(AudioPlaybackQueue[0], MySet.Volume*0.01):
            AudioPlaybackQueue.popleft()

#---------------------------------------
# Setting functions
#---------------------------------------
def ReloadSettings(jsonData):
    """Reload settings"""
    global MySet
    MySet.Reload(jsonData)

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

#---------------------------------------
# Alert functions
#---------------------------------------
def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    fullpath = os.path.join(AudioFilesPath, audiofile)
    AudioPlaybackQueue.append(fullpath)

#---------------------------------------
# Command functions
#---------------------------------------
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

def AddCooldowns(data):
    """Function to add cooldowns for users"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
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

def NotEnoughResp(data):
    """Send message about not having enough currency"""
    currency = Parent.GetCurrencyName()
    notEnough = MySet.NotEnoughResponse.format(data.UserName, currency, MySet.Command)

    SendResp(data, MySet.Usage, notEnough)

def AddPointsAll(data, PayoutAmount):
    """Add points to all users"""
    Mydict = {}
    for viewer in Parent.GetViewerList():
        Mydict[viewer] = PayoutAmount

    Parent.AddPointsAll(Mydict)

    message = MySet.BaseResponse.format(data.UserName, MySet.Cost, PayoutAmount, Parent.GetCurrencyName())
    SendResp(data, MySet.Usage, message)

#---------------------------------------
# UI button functions
#---------------------------------------
def OpenSoundsFolder():
    """Open specific sound folder"""
    os.startfile(AudioFilesPath)

def OpenSoundFolder():
    """Open specific sounds folder"""
    location = (os.path.dirname(os.path.realpath(__file__)))
    location += "/sounds/"
    os.startfile(location)

def OpenFolder():
    """Open specific sounds folder"""
    location = (os.path.dirname(os.path.realpath(__file__)))
    os.startfile(location)

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, MySet.Usage, message)
        return False
    return True
