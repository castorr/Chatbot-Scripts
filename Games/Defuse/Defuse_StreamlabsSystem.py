#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Defuse game with lot of variation and customization to fit most streamers"""
#---------------------------------------
# Libraries and references
#---------------------------------------
from collections import deque
import codecs
import json
import os
import winsound
import ctypes
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Defuse"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.1.4 (Unreleased)"
Description = "Defuse minigame | Right click -> Insert API key"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases
1.1.4 - Cleaned up code, added default parameters, renamed functions and variables
1.1.3 - Fixed not enough currency response
1.1.2 - Added Mixer suport
1.1.1 - Fixed usernames for youtube
      - Removed some stupid code
1.1.0 - Code overhaul.
      - Added $user $target and $currencyname
      - Added $permission and $permissioninfo
      - Updated default values
      - Added option to use random payouts
      - Added button to calculate chances
      - Optimized randomisation
1.0.3 - Fixed payouts
1.0.2 - Updated to work with youtube
1.0.1 - Fixed permission handling
1.0.0 - Initial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue = deque()
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
            self.Command = "!defuse"
            self.Cost = 500
            self.Usage = "Stream Chat"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Mode = "3 Wires"
            self.UseRandom = True
            self.BWS = False
            self.Gif = "https://i.imgur.com/gInovKi.gif"
            self.Duration = 5
            self.PS = False
            self.SF = "test.mp3"
            self.BWSB = False
            self.GifB = "https://i.imgur.com/6bphR3T.gif"
            self.DurationB = 5
            self.PSB = False
            self.SFB = "test.mp3"
            self.Timeout = False
            self.TL = 60
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "$user the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "$user the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "The bomb is beeping and $user cuts the $target wire... "
            self.NotEnoughResponse = "$user you don't have enough points to get the tools needed to defuse the bomb!"
            self.WinResponse = "the bomb goes silent. As a thanks for saving the day you got awarded {1} $currencyname and now has {2} $currencyname "
            self.LoseResponse = " BOOM!!! The bomb explodes, you lost {1} $currencyname and now have {2} $currencyname"
            self.PermissionResp = "$user -> only $permission ($permissioninfo) and higher can use this command"
            self.InfoResponse = "$user you have to chose one of the following wires to cut: {1}"
            self.Volume = 50

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        if not CheckSoundFiles():
            winsound.MessageBeep()
            global soundsList
            returnValue = MessageBox(0, u"Some soundfiles could not be found."
                                        "\r\nMake sure the name is correct and that "
                                        "the file is located in the sounds folder."
                                        "\r\nThe following soundfiles can't be found:\r\n{0}"
                                        "\r\nDo you want to open the sounds"
                                        " folder now?".format(soundsList)
                                     , u"File not found", 4)
            if returnValue == 6:
                OpenSoundFolder()

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        Settings.SaveSettings(MySet, settingsFile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        Settings.SaveSettings(MySet, settingsFile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        Settings.SaveSettings(MySet, settingsFile)

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not CheckPerm(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():
            if CheckCooldown(data):
                return

            if Parent.GetPoints(data.User) < MySet.Cost:
                SendResp(data, MySet.NotEnoughResponse.format(data.UserName, Parent.GetCurrencyName()))
                return

            if MySet.Mode == "3 Wires":
                options = ["red", "blue", "yellow"]
                wires = "red, blue, yellow"
                Outcome(data, options, wires, 3)

            elif MySet.Mode == "4 Wires":
                options = ["red", "blue", "yellow", "black"]
                wires = "red, blue, yellow, black"
                Outcome(data, options, wires, 4)

            elif MySet.Mode == "5 Wires":
                options = ["red", "blue", "yellow", "black", "green"]
                wires = "red, blue, yellow, black, green"
                Outcome(data, options, wires, 5)

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue:
        if Parent.PlaySound(AudioPlaybackQueue[0], MySet.Volume*0.01):
            AudioPlaybackQueue.popleft()

#---------------------------------------
# Functions for all game modes
#---------------------------------------
def Outcome(data, options, wires, m):
    """Game outcome function
    Checks if there's enough parameters
    Shuffle the list of wires
    Selects one wire that's the safe one to cut
    Add/remove points
    Sends message
    Add cooldowns"""

    if data.GetParamCount() < 2 or (not data.GetParam(1).lower() in options):
        SendResp(data, MySet.InfoResponse.format(data.UserName, wires))
        return


    option = Parent.GetRandom(0,m)
    success = options[option]

    if data.GetParam(1).lower() == success.lower():

        if MySet.UseRandom:
            rMin = MySet.Cost*m - MySet.Cost/2
            rMax = MySet.Cost*m + MySet.Cost/2
            value = Parent.GetRandom(rMin, rMax)
        else:
            value = MySet.Cost*m

        Parent.AddPoints(data.User, data.UserName, value)

        points = Parent.GetPoints(data.User)
        currency = Parent.GetCurrencyName()
        winMessage = MySet.WinResponse.format(data.UserName, value, points, currency)

        message = (MySet.BaseResponse.format(data.UserName, data.GetParam(1)) + winMessage)
        SendResp(data, message)

        if MySet.BWS:
            dump = {"duration": MySet.Duration*1000, "link": MySet.Gif}
            Parent.BroadcastWsEvent("EVENT_DEFUSE", json.dumps(dump))

        if MySet.PS:
            #check if it should play sound
            fullpath = os.path.join(AudioFilesPath, MySet.SF)
            if MySet.PS and fullpath and os.path.isfile(fullpath):
                EnqueueAudioFile(MySet.SF)

    else:
        Parent.RemovePoints(data.User, data.UserName, MySet.Cost)

        points = Parent.GetPoints(data.User)
        currency = Parent.GetCurrencyName()
        loseMessage = MySet.LoseResponse.format(data.UserName, MySet.Cost, points, currency)

        message = (MySet.BaseResponse.format(data.UserName, data.GetParam(1)) + loseMessage)
        SendResp(data, message)

        if MySet.BWSB:
            dump = {"duration": MySet.Duration*1000, "link": MySet.GifB}
            Parent.BroadcastWsEvent("EVENT_DEFUSE", json.dumps(dump))

        if MySet.PSB:
            fullpath = os.path.join(AudioFilesPath, MySet.SFB)
            if MySet.PSB and fullpath and os.path.isfile(fullpath):
                EnqueueAudioFile(MySet.SFB)

        if MySet.Timeout:
            Parent.SendTwitchMessage("/timeout {0} {1}".format(data.UserName, MySet.TL))


    AddCooldown(data)

def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    fullpath = os.path.join(AudioFilesPath, audiofile)
    AudioPlaybackQueue.append(fullpath)

def CheckSoundFiles():
    """Function to check all soundfiles while reloading settings"""
    global soundsList
    soundsList = ""
    fullpath = os.path.join(AudioFilesPath, MySet.SF)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.PS:
        soundsList += (MySet.SF + "\r\n")

    fullpath = os.path.join(AudioFilesPath, MySet.SFB)
    if not (fullpath and os.path.isfile(fullpath)) and MySet.PSB:
        soundsList += (MySet.SFB + "\r\n")

    return bool(soundsList == "")

#---------------------------------------
# Functions for commands
#---------------------------------------
def CheckPerm(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, message)
        return False
    return True

def CheckCooldown(data):
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
                message = MySet.OnCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)

            else: #set cd remaining
                m_CooldownRemaining = userCDD

                #send usercooldown message
                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)
        return True
    return False

def SendResp(data, Message):
    """Sends message to Stream or discord chat depending on settings"""

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

def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)

#---------------------------------------
# Optional UI button functions
#---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

def OpenSoundFolder():
    """Open specific sounds folder"""
    location = (os.path.dirname(os.path.realpath(__file__)))
    location += "/sounds/"
    os.startfile(location)

def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    MessageBox = ctypes.windll.user32.MessageBoxW
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)
    if returnValue == 6:

        MessageBox = ctypes.windll.user32.MessageBoxW
        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

        # Set defaults by not supplying a settings file
        MySet = Settings()

        # Save defaults back to file
        MySet.SaveSettings(settingsFile)

def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.ReloadSettings(jsondata)

def CalculateChances():
    """Function to do 1 million test rolls and get the result"""
    n = 0
    reds = 0
    blues = 0
    yellows = 0
    blacks = 0
    greens = 0
    errors = 0
    if MySet.Mode == "3 Wires":
        m = 3
        options = ["red", "blue", "yellow"]
    elif MySet.Mode == "4 Wires":
        m = 4
        options = ["red", "blue", "yellow", "black"]
    elif MySet.Mode == "5 Wires":
        m = 5
        options = ["red", "blue", "yellow", "black", "green"]
    while n < 1000000:
        option = Parent.GetRandom(0,m)
        success = options[option]
        if success.lower() == "red":
            reds += 1
        elif success.lower() == "blue":
            blues += 1
        elif success.lower() == "yellow":
            yellows += 1
        elif success.lower() == "black":
            blacks += 1
        elif success.lower() == "green":
            greens += 1
        else:
            errors += 1
        n += 1
    redsp = reds/10000
    bluesp = blues/10000
    yellowsp = yellows/10000
    blacksp = blacks/10000
    greensp = greens/10000
    errorsp = errors/10000
    textMessage = " Red: {0} ({5}%) \r\n Blue: {1} ({6}%) \r\n Yellow: {2} ({7}%) \r\n Black: {3} ({8}%) \r\n Green: {4} ({9}%) \r\n Errors: {10} ({11}%)"
    winsound.MessageBeep()
    MessageBox(0, u" Below is the amount of times each color was the correct wire to cut! \r\n" + textMessage.format(reds, blues, yellows, blacks, greens, redsp, bluesp, yellowsp, blacksp, greensp, errors, errorsp), u"1million tests in {0} mode".format(MySet.Mode), 0)

def BuiltInVariables(data, Message):
    """Replace built in variables"""
    Message = Message.replace("$targetname", data.GetParam(1))
    Message = Message.replace("$targetid", data.GetParam(1).lower())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$username", data.UserName)
    Message = Message.replace("$userid", data.User)
    Message = Message.replace("$user", data.User)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)
    Message = Message.replace("$permission", MySet.Permission)
    
    return Message
