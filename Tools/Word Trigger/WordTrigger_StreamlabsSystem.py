#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Any word in a sentence can trigger the command"""
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
ScriptName = "Word Trigger"
Website = "https://www.Twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.3"
Description = "Set a word to trigger a response anywhere in a sentence"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.3 Fixed userid showing instead of username
1.2 Fixed HasPermission & cooldown
1.1 Added Mixer support
1.0 Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue = deque()
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""
    #The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file is found
            self.OnlyLive = True
            self.Command = "Kappa"
            self.Words = False
            self.PS = False
            self.SF = "Example.mp3"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.UseCD = True
            self.CasterCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 0
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.BaseResponse = "{0} don't you dare being sarcastic here!"
            self.PermissionResp = "{0} -> only {1} ({2}) and higher can use trigger this secret"
            self.Count = 0
            self.Volume = 50

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        fullpath = os.path.join(AudioFilesPath, MySet.SF)
        if not (fullpath and os.path.isfile(fullpath)) and MySet.PS:
            MessageBox = ctypes.windll.user32.MessageBoxW
            returnValue = MessageBox(0, u"Couldn't find the specified soundfile."
                                        "\r\nMake sure the name is correct and that "
                                        "the file is located in the sounds folder"
                                        "\r\n\r\nDo you want to open the sounds folder now?"
                                     , u"File not found", 4)
            if returnValue == MB_YES:
                OpenSoundFolder()

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
    """Data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue:
        if Parent.PlaySound(AudioPlaybackQueue[0], MySet.Volume*0.01):
            AudioPlaybackQueue.popleft()

def Execute(data):
    """Required Execute Data function"""
    if data.IsChatMessage():
        if not IsFromValidSource(data, MySet.Usage):
            return

        myString = data.Message
        if not MySet.Command.lower() in myString.lower() and not multiWords(data):
            return

        if not HasPermission(data):
            return

        if IsOnCooldown(data):
            return

        if MySet.OnlyLive and Parent.IsLive() is False:
            return

        RunCommand(data)

#---------------------------------------
# [Optional] functions
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

def RunCommand(data):
    """Execute the command if triggered"""
    message = MySet.BaseResponse.format(data.UserName, MySet.Count)
    SendResp(data, MySet.Usage, message)

    if MySet.PS:
        SoundsPath = os.path.join(AudioFilesPath, MySet.SF)
        EnqueueAudioFile(SoundsPath)

    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        return

    Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
    Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)

def multiWords(data):
    """Check if one of the word is in the message"""
    if MySet.Words:
        words = MySet.Command.split()
        for word in words:
            if word.lower() in data.Message.lower():
                return True
    return False

def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    fullpath = os.path.join(AudioFilesPath, audiofile)
    AudioPlaybackQueue.append(fullpath)

def OpenSoundFolder():
    """Open specific sounds folder"""
    location = (os.path.dirname(os.path.realpath(__file__)))
    location += "/sounds/"
    os.startfile(location)

def TestSound():
    """Test sound & volume through UI button"""
    SoundsPath = os.path.join(AudioFilesPath, MySet.SF)
    Parent.PlaySound(SoundsPath, MySet.Volume*0.01)

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, MySet.Usage, message)
        return False
    return True

def IsOnCooldown(data):
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
                SendResp(data, MySet.Usage, message)

            else: #set cd remaining
                m_CooldownRemaining = userCDD

                #send usercooldown message
                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)
        return True
    return False
