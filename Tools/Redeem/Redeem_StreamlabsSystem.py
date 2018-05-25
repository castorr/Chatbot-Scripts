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
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Redeem"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.1.0"
Description = "Right Click -> Insert API Key"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.1.0   - Alerts now support text below the image! Customizable for each reward

1.0.10  - !redeem list now only show rewards available for the user
        - fixed !redeem not returning anything

1.0.9   - Improved overlay stability
        - Fixed default cost value for reward 1

1.0.8   - Added Mixer support
        - Removed ton of return statements
        - Added functions for cleaner code
        - Renamed functions for readability
        - Removed unnecessary repetitions

1.0.7   - Updated to work with Youtube & fixed caster ignore cooldown option

1.0.6   - Code cleanup, improved usage stability added option to save message to file

1.0.5   - Fixed cost handling

1.0.4   - Fixed cooldown management
        - Changed version numbering

1.0.0.3 - Added sounds on errorboxes
        - Cleaned up some code

1.0.0.2 - Fixed to work with Streamlabs Chatbot

1.0.0.1 - Added "target2" for chat response
        - Added messagebox when redeem file is reset successfully

1.0.0.0 - Initial Release
"""
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
            self.Command = "!redeem"
            self.Volume = 50
            self.Usage = "Stream Chat"
            self.stf = True
            self.textline = "{0} - {1} - {2} {3} - {4}"
            self.NotEnough = "{0} -> you don't have the {1} {2} required to redeem this reward."
            self.NotAvailable = "{0} -> {1} isn't an available reward"
            self.Info = "{0} -> you have to define a reward to redeem!"
            self.ListBase = "Right now you can redeem: "
            self.NotPerm = "{0} -> you don't have permission to redeem this reward. Permission is: [{1} / {2}]"
            self.ListCost = True
            self.UseCD = True
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.r1Enabled = True
            self.r1 = "follow"
            self.r1Cost = 100
            self.r1SM = True
            self.r1Message = "{0} spent {1} {2} to redeem a follow on twitch"
            self.r1BWS = True
            self.r1LocalGif = False
            self.r1GifLink = "https://media3.giphy.com/avatars/100soft/WahNEDdlGjRZ.gif"
            self.r1Duration = 5
            self.r1Text = ""
            self.r1PS = True
            self.r1Sound = "test.mp3"
            self.r1Permission = "Everyone"
            self.r1PermissionInfo = ""
            self.r1UseCD = True
            self.r1Cooldown = 0
            self.r1UserCooldown = 10
            self.r2Enabled = False
            self.r2 = ""
            self.r2Cost = 100
            self.r2SM = False
            self.r2Message = ""
            self.r2BWS = False
            self.r2LocalGif = False
            self.r2GifLink = "insert gif link"
            self.r2Duration = 5
            self.r2Text = ""
            self.r2PS = True
            self.r2Sound = "insert sound file"
            self.r2Permission = "Everyone"
            self.r2PermissionInfo = ""
            self.r2Cooldown = 5
            self.r2UserCooldown = 10
            self.r3Enabled = False
            self.r3 = ""
            self.r3Cost = 100
            self.r3SM = False
            self.r3Message = ""
            self.r3BWS = False
            self.r3LocalGif = False
            self.r3GifLink = "insert gif link"
            self.r3Duration = 5
            self.r3Text = ""
            self.r3PS = True
            self.r3Sound = "insert sound file"
            self.r3Permission = "Everyone"
            self.r3PermissionInfo = ""
            self.r3Cooldown = 5
            self.r3UserCooldown = 10
            self.r4Enabled = False
            self.r4 = ""
            self.r4Cost = 100
            self.r4SM = False
            self.r4Message = ""
            self.r4BWS = False
            self.r4LocalGif = False
            self.r4GifLink = "insert gif link"
            self.r4Duration = 5
            self.r4Text = ""
            self.r4PS = True
            self.r4Sound = "insert sound file"
            self.r4Permission = "Everyone"
            self.r4PermissionInfo = ""
            self.r4Cooldown = 5
            self.r4UserCooldown = 10
            self.r5Enabled = False
            self.r5 = ""
            self.r5Cost = 100
            self.r5SM = False
            self.r5Message = ""
            self.r5BWS = False
            self.r5LocalGif = False
            self.r5GifLink = "insert gif link"
            self.r5Duration = 5
            self.r5Text = ""
            self.r5PS = True
            self.r5Sound = "insert sound file"
            self.r5Permission = "Everyone"
            self.r5PermissionInfo = ""
            self.r5Cooldown = 5
            self.r5UserCooldown = 10
            self.r6Enabled = False
            self.r6 = ""
            self.r6Cost = 100
            self.r6SM = False
            self.r6Message = ""
            self.r6BWS = False
            self.r6LocalGif = False
            self.r6GifLink = "insert gif link"
            self.r6Duration = 5
            self.r6Text = ""
            self.r6PS = True
            self.r6Sound = "insert sound file"
            self.r6Permission = "Everyone"
            self.r6PermissionInfo = ""
            self.r6Cooldown = 5
            self.r6UserCooldown = 10
            self.r7Enabled = False
            self.r7 = ""
            self.r7Cost = 100
            self.r7SM = False
            self.r7Message = ""
            self.r7BWS = False
            self.r7LocalGif = False
            self.r7GifLink = "insert gif link"
            self.r7Duration = 5
            self.r7Text = ""
            self.r7PS = True
            self.r7Sound = "insert sound file"
            self.r7Permission = "Everyone"
            self.r7PermissionInfo = ""
            self.r7Cooldown = 5
            self.r7UserCooldown = 10
            self.r8Enabled = False
            self.r8 = ""
            self.r8Cost = 100
            self.r8SM = False
            self.r8Message = ""
            self.r8BWS = False
            self.r8LocalGif = False
            self.r8GifLink = "insert gif link"
            self.r8Duration = 5
            self.r8Text = ""
            self.r8PS = True
            self.r8Sound = "insert sound file"
            self.r8Permission = "Everyone"
            self.r8PermissionInfo = ""
            self.r8Cooldown = 5
            self.r8UserCooldown = 10
            self.r9Enabled = False
            self.r9 = ""
            self.r9Cost = 100
            self.r9SM = False
            self.r9Message = ""
            self.r9BWS = False
            self.r9LocalGif = False
            self.r9GifLink = "insert gif link"
            self.r9Duration = 5
            self.r9Text = ""
            self.r9PS = True
            self.r9Sound = "insert sound file"
            self.r9Permission = "Everyone"
            self.r9PermissionInfo = ""
            self.r9Cooldown = 5
            self.r9UserCooldown = 10
            self.r10Enabled = False
            self.r10 = ""
            self.r10Cost = 100
            self.r10SM = False
            self.r10Message = ""
            self.r10BWS = False
            self.r10LocalGif = False
            self.r10GifLink = "insert gif link"
            self.r10Duration = 5
            self.r10Text = ""
            self.r10PS = True
            self.r10Sound = "insert sound file"
            self.r10Permission = "Everyone"
            self.r10PermissionInfo = ""
            self.r10Cooldown = 5
            self.r10UserCooldown = 10

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        if not CheckSoundFiles():
            MessageBox = ctypes.windll.user32.MessageBoxW
            winsound.MessageBeep()
            global soundsList
            returnValue = MessageBox(0, u"Some soundfiles could not be found."
                                        "\r\nMake sure the name is correct and that "
                                        "the file is located in the sounds folder"
                                        "\r\nThe following rewards got invalid soundfiles:\r\n{0}"
                                        "\r\nDo you want to open the sounds"
                                        " folder now?".format(soundsList)
                                     , u"File not found", 4)
            if returnValue == 6:
                OpenSoundFolder()
        return

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
    location = (os.path.dirname(os.path.realpath(__file__)))
    location += "/sounds/"
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
            returnValue = MessageBox(0, u"Redeem file successfully reset."
                                     , u"Redeem file reset!", 0)

#---------------------------------------
# Optional functions
#---------------------------------------
def IsOnCooldown(data, command):
    """Handle cooldowns"""

    cooldown = Parent.IsOnCooldown(ScriptName, command)
    usercooldown = Parent.IsOnUserCooldown(ScriptName, command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    #check if command is on cooldown
    if (cooldown or usercooldown) and caster is False:

        #check if cooldown message is enabled
        if MySet.UseCD:

            #set variables for cooldown
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, command, data.User)

            #check for the longest CD!
            if cooldownDuration > userCDD:

                #send cooldown message
                SendResp(data, MySet.OnCooldown.format(data.UserName, cooldownDuration))

            else:
                #send usercooldown message
                SendResp(data, MySet.OnUserCooldown.format(data.UserName, userCDD))
        return False

    return True

def GetCommand(reward):
    """Get full command name for cooldown handeling"""
    command = MySet.Command
    command += " "
    command += reward
    return command

def SendResp(data, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))

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

def CheckSoundFiles():
    """Function to check all soundfiles while reloading settings"""
    fullpath = os.path.join(AudioFilesPath, MySet.r1Sound)
    global soundsList
    soundsList = ""
    fullpath = os.path.join(AudioFilesPath, MySet.r1Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r1PS and MySet.r1Enabled:
        soundsList += (MySet.r1 + " - (reward1)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r2Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r2PS and MySet.r2Enabled:
        soundsList += (MySet.r2 + " - (reward2)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r3Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r3PS and MySet.r3Enabled:
        soundsList += (MySet.r3 + " - (reward3)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r4Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r4PS and MySet.r4Enabled:
        soundsList += (MySet.r4 + " - (reward4)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r5Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r5PS and MySet.r5Enabled:
        soundsList += (MySet.r5 + " - (reward5)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r6Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r6PS and MySet.r6Enabled:
        soundsList += (MySet.r6 + " - (reward6)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r7Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r7PS and MySet.r7Enabled:
        soundsList += (MySet.r7 + " - (reward7)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r8Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r8PS and MySet.r8Enabled:
        soundsList += (MySet.r8 + " - (reward8)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r9Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r9PS and MySet.r9Enabled:
        soundsList += (MySet.r9 + " - (reward9)\r\n")
    fullpath = os.path.join(AudioFilesPath, MySet.r1Sound)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.r10PS and MySet.r10Enabled:
        soundsList += (MySet.r10 + " - (reward10)\r\n")
    return bool(soundsList == "")

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

        if MySet.OnlyLive and not data.IsLive():
            return

        if data.GetParamCount() < 2:
            message = MySet.Info.format(data.UserName)
            SendResp(data, message)
            return

        if data.GetParam(1).lower() == MySet.r1.lower():
            Reward1(data)

        elif data.GetParam(1).lower() == MySet.r2.lower():
            Reward2(data)

        elif data.GetParam(1).lower() == MySet.r3.lower():
            Reward3(data)

        elif data.GetParam(1).lower() == MySet.r4.lower():
            Reward4(data)

        elif data.GetParam(1).lower() == MySet.r5.lower():
            Reward5(data)

        elif data.GetParam(1).lower() == MySet.r6.lower():
            Reward6(data)

        elif data.GetParam(1).lower() == MySet.r7.lower():
            Reward7(data)

        elif data.GetParam(1).lower() == MySet.r8.lower():
            Reward8(data)

        elif data.GetParam(1).lower() == MySet.r9.lower():
            Reward9(data)

        elif data.GetParam(1).lower() == MySet.r10.lower():
            Reward10(data)

        elif data.GetParam(1).lower() == "list":
            SendResp(data, GetList(data))

        else:
            message = MySet.NotAvailable.format(data.UserName, data.GetParam(1))
            SendResp(data, message)

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue:
        if Parent.PlaySound(AudioPlaybackQueue[0], MySet.Volume*0.01):
            AudioPlaybackQueue.popleft()

#---------------------------------------
# [Optional] Reward functions
#---------------------------------------
def redeem(data, sm, ps, bws, message, dump, SF, cost):
    """First redeem reward function"""
    if Parent.GetPoints(data.User) >= cost:
        if not MySet.OnlyLive or Parent.IsLive():
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

                with open(RewardFile, "a") as f:
                    f.write(textline + "\n")

    else:
        currency = Parent.GetCurrencyName()
        points = Parent.GetPoints(data.User)
        message = MySet.NotEnough.format(data.UserName, cost, currency, points)
        SendResp(data, message)
        return False
    return True

def GetList(data):
    """Get list of all enabled rewards"""
    RewardList = MySet.ListBase

    if MySet.r1Enabled and Parent.HasPermission(data.User, MySet.r1Permission, MySet.r1PermissionInfo):
        RewardList += (MySet.r1)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r1Cost) + ")" + " - ")

    if MySet.r2Enabled and Parent.HasPermission(data.User, MySet.r2Permission, MySet.r2PermissionInfo):
        RewardList += (MySet.r2)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r2Cost) + ")" + " - ")

    if MySet.r3Enabled and Parent.HasPermission(data.User, MySet.r3Permission, MySet.r3PermissionInfo):
        RewardList += (MySet.r3)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r3Cost) + ")" + " - ")

    if MySet.r4Enabled and Parent.HasPermission(data.User, MySet.r4Permission, MySet.r4PermissionInfo):
        RewardList += (MySet.r4)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r4Cost) + ")" + " - ")

    if MySet.r5Enabled and Parent.HasPermission(data.User, MySet.r5Permission, MySet.r5PermissionInfo):
        RewardList += (MySet.r5)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r5Cost) + ")" + " - ")

    if MySet.r6Enabled and Parent.HasPermission(data.User, MySet.r6Permission, MySet.r6PermissionInfo):
        RewardList += (MySet.r6)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r6Cost) + ")" + " - ")

    if MySet.r7Enabled and Parent.HasPermission(data.User, MySet.r7Permission, MySet.r7PermissionInfo):
        RewardList += (MySet.r7)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r7Cost) + ")" + " - ")

    if MySet.r8Enabled and Parent.HasPermission(data.User, MySet.r8Permission, MySet.r8PermissionInfo):
        RewardList += (MySet.r8)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r8Cost) + ")" + " - ")

    if MySet.r9Enabled and Parent.HasPermission(data.User, MySet.r9Permission, MySet.r9PermissionInfo):
        RewardList += (MySet.r9)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r9Cost) + ")" + " - ")

    if MySet.r10Enabled and Parent.HasPermission(data.User, MySet.r10Permission, MySet.r10PermissionInfo):
        RewardList += (MySet.r10)
        if MySet.ListCost:
            RewardList += ("(" + str(MySet.r10Cost) + ")" + " - ")

    return RewardList

def HasPermission(data, permission, permissioninfo):
    """Return true or false dending on if the user has permission.
    Also sends permission response if user doesn't"""
    if not Parent.HasPermission(data.User, permission, permissioninfo):
        message = MySet.NotPerm.format(data.UserName, permission, permissionfnfo)
        SendResp(data, message)
        return False
    return True

def Reward1(data):
    """Reward 1 setup function"""
    if not HasPermission(data, MySet.r1Permission, MySet.r1PermissionInfo):
        return

    command = GetCommand(MySet.r1)
    if MySet.r1Enabled and IsOnCooldown(data, command):
        a = MySet.r1SM
        b = MySet.r1PS
        c = MySet.r1BWS
        e = MySet.r1Message
        textalert = MySet.r1Text.format(data.UserName, MySet.r1Cost, MySet.r1)
        f = {"duration": MySet.r1Duration*1000, "link": MySet.r1GifLink, "text": textalert}
        g = MySet.r1Sound
        h = MySet.r1Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r1UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r1Cooldown)

def Reward2(data):
    """Reward 2 setup function"""
    if not HasPermission(data, MySet.r2Permission, MySet.r2PermissionInfo):
        return

    command = GetCommand(MySet.r2)
    if MySet.r2Enabled and IsOnCooldown(data, command):
        a = MySet.r2SM
        b = MySet.r2PS
        c = MySet.r2BWS
        e = MySet.r2Message
        textalert = MySet.r2Text.format(data.UserName, MySet.r2Cost, MySet.r2)
        f = {"duration": MySet.r2Duration*1000, "link": MySet.r2GifLink, "text": textalert}
        g = MySet.r2Sound
        h = MySet.r2Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r2UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r2Cooldown)

def Reward3(data):
    """Reward 3 setup function"""
    if not HasPermission(data, MySet.r3Permission, MySet.r3PermissionInfo):
        return

    command = GetCommand(MySet.r3)
    if MySet.r3Enabled and IsOnCooldown(data, command):
        a = MySet.r3SM
        b = MySet.r3PS
        c = MySet.r3BWS
        e = MySet.r3Message
        textalert = MySet.r3Text.format(data.UserName, MySet.r3Cost, MySet.r3)
        f = {"duration": MySet.r3Duration*1000, "link": MySet.r3GifLink, "text": textalert}
        g = MySet.r3Sound
        h = MySet.r3Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r3UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r3Cooldown)

def Reward4(data):
    """Reward 4 setup function"""
    if not HasPermission(data, MySet.r4Permission, MySet.r4PermissionInfo):
        return

    command = GetCommand(MySet.r4)
    if MySet.r4Enabled and IsOnCooldown(data, command):
        a = MySet.r4SM
        b = MySet.r4PS
        c = MySet.r4BWS
        e = MySet.r4Message
        textalert = MySet.r4Text.format(data.UserName, MySet.r4Cost, MySet.r4)
        f = {"duration": MySet.r4Duration*1000, "link": MySet.r4GifLink, "text": textalert}
        g = MySet.r4Sound
        h = MySet.r4Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r4UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r4Cooldown)

def Reward5(data):
    """Reward 5 setup function"""
    if not HasPermission(data, MySet.r5Permission, MySet.r5PermissionInfo):
        return

    command = GetCommand(MySet.r5)
    if MySet.r5Enabled and IsOnCooldown(data, command):
        a = MySet.r5SM
        b = MySet.r5PS
        c = MySet.r5BWS
        e = MySet.r5Message
        textalert = MySet.r5Text.format(data.UserName, MySet.r5Cost, MySet.r5)
        f = {"duration": MySet.r5Duration*1000, "link": MySet.r5GifLink, "text": textalert}
        g = MySet.r5Sound
        h = MySet.r5Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r5UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r5Cooldown)

def Reward6(data):
    """Reward 6 setup function"""
    if not HasPermission(data, MySet.r6Permission, MySet.r6PermissionInfo):
        return

    command = GetCommand(MySet.r6)
    if MySet.r6Enabled and IsOnCooldown(data, command):
        a = MySet.r6SM
        b = MySet.r6PS
        c = MySet.r6BWS
        e = MySet.r6Message
        textalert = MySet.r6Text.format(data.UserName, MySet.r6Cost, MySet.r6)
        f = {"duration": MySet.r6Duration*1000, "link": MySet.r6GifLink, "text": textalert}
        g = MySet.r6Sound
        h = MySet.r6Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r6UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r6Cooldown)

def Reward7(data):
    """Reward 7 setup function"""
    if not HasPermission(data, MySet.r7Permission, MySet.r7PermissionInfo):
        return

    command = GetCommand(MySet.r7)
    if MySet.r7Enabled and MySet.r7Enabled and IsOnCooldown(data, command):
        a = MySet.r7SM
        b = MySet.r7PS
        c = MySet.r7BWS
        e = MySet.r7Message
        textalert = MySet.r7Text.format(data.UserName, MySet.r7Cost, MySet.r7)
        f = {"duration": MySet.r7Duration*1000, "link": MySet.r7GifLink, "text": textalert}
        g = MySet.r7Sound
        h = MySet.r7Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r7UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r7Cooldown)

def Reward8(data):
    """Reward 8 setup function"""
    if not HasPermission(data, MySet.r8Permission, MySet.r8PermissionInfo):
        return

    command = GetCommand(MySet.r8)
    if MySet.r8Enabled and IsOnCooldown(data, command):
        a = MySet.r8SM
        b = MySet.r8PS
        c = MySet.r8BWS
        e = MySet.r8Message
        textalert = MySet.r8Text.format(data.UserName, MySet.r8Cost, MySet.r8)
        f = {"duration": MySet.r8Duration*1000, "link": MySet.r8GifLink, "text": textalert}
        g = MySet.r8Sound
        h = MySet.r8Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r8UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r8Cooldown)

def Reward9(data):
    """Reward 9 setup function"""
    if not HasPermission(data, MySet.r9Permission, MySet.r9PermissionInfo):
        return

    command = GetCommand(MySet.r9)
    if MySet.r9Enabled and IsOnCooldown(data, command):
        a = MySet.r9SM
        b = MySet.r9PS
        c = MySet.r9BWS
        e = MySet.r9Message
        textalert = MySet.r9Text.format(data.UserName, MySet.r9Cost, MySet.r9)
        f = {"duration": MySet.r9Duration*1000, "link": MySet.r9GifLink, "text": textalert}
        g = MySet.r9Sound
        h = MySet.r9Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r9UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r9Cooldown)

def Reward10(data):
    """Reward 10 setup function"""
    if not HasPermission(data, MySet.r10Permission, MySet.r10PermissionInfo):
        return

    command = GetCommand(MySet.r10)
    if MySet.r10Enabled and IsOnCooldown(data, command):
        a = MySet.r10SM
        b = MySet.r10PS
        c = MySet.r10BWS
        e = MySet.r10Message
        textalert = MySet.r10Text.format(data.UserName, MySet.r10Cost, MySet.r10)
        f = {"duration": MySet.r10Duration*1000, "link": MySet.r10GifLink, "text": textalert}
        g = MySet.r10Sound
        h = MySet.r10Cost

        if redeem(data, a, b, c, e, f, g, h):
            Parent.RemovePoints(data.User, data.UserName, h)

            Parent.AddUserCooldown(ScriptName, command, data.User, MySet.r10UserCooldown)
            Parent.AddCooldown(ScriptName, command, MySet.r10Cooldown)
