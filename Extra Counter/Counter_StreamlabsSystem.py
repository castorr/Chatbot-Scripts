#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Additional counter"""
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
ScriptName = "Extra Counter"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.5"
Description = "Extra counter"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.5     - Fixed permission to set count
1.4     - Added mixer support
1.3     - Updated to work with chatbot 1.0.2.29 (YouTube update)
1.2     - Added setting to change textfile layout. Added buttons to UI
1.1     - Cleaned up code, improved usage stability
1.0     - Added usage options, fixed set glitch, ui tweaks
1.0.0.0 - Intial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
countFile = os.path.join(os.path.dirname(__file__), "count.txt")
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

        else: #set variables if no settings file is found
            self.OnlyLive = False
            self.Command = "!rip"
            self.Usage = "Twitch Chat"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.ModPerm = "Moderator"
            self.ModPermInfo = ""
            self.TextFormat = "{0}"
            self.dCount = 0
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 0
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "Deaths: {1}"
            self.Increased = "[Increased] {1}"
            self.Decreased = "[Decreased] {1}"
            self.Set = "[Set] New count: {1}"
            self.Reset = "[Reset] New count: 0"
            self.PermissionResp = "$user -> only $permission ($permissioninfo) and higher can use this command"

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
# Optional functions
#---------------------------------------
def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
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
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        MySet.Save(settingsFile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        MySet.Save(settingsFile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        MySet.Save(settingsFile)

def Tick():
    """Required tick function"""

def Execute(data):
    """Required Execute Data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():
        if not IsFromValidSource(data, MySet.Usage):
            return

        if not HasPermission(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():
            if IsOnCooldown(data):
                return

        if data.GetParamCount() < 2:

            message = MySet.BaseResponse.format(data.UserName, MySet.dCount)
            SendResp(data, MySet.Usage, message)
            return

        HasModPerm = Parent.HasPermission(data.User, MySet.ModPerm, MySet.ModPermInfo)
        if data.GetParam(1) == "+" and HasModPerm:

            MySet.dCount += 1
            MySet.Save(settingsFile)
            SaveToFile(str(MySet.TextFormat.format(MySet.dCount)))

            message = MySet.Increased.format(data.UserName, MySet.dCount)
            SendResp(data, MySet.Usage, message)

        elif data.GetParam(1) == "-" and HasModPerm:

            MySet.dCount -= 1
            MySet.Save(settingsFile)
            SaveToFile(str(MySet.TextFormat.format(MySet.dCount)))

            message = MySet.Decreased.format(data.UserName, MySet.dCount)
            SendResp(data, MySet.Usage, message)

        elif data.GetParam(1) == "reset" and HasModPerm:

            MySet.dCount = 0
            MySet.Save(settingsFile)
            SaveToFile(str(MySet.TextFormat.format(MySet.dCount)))

            message = MySet.Reset.format(data.UserName)
            SendResp(data, MySet.Usage, message)

        else:
            try:
                int(data.GetParam(1))

                if HasModPerm:
                    MySet.dCount = int(data.GetParam(1))
                    MySet.Save(settingsFile)
                    SaveToFile(str(MySet.TextFormat.format(MySet.dCount)))

                    message = MySet.Set.format(data.UserName, MySet.dCount)
                    SendResp(data, MySet.Usage, message)

                else:
                    message = MySet.BaseResponse.format(data.UserName, MySet.dCount)
                    SendResp(data, MySet.Usage, message)

            except ValueError:
                message = MySet.BaseResponse.format(data.UserName, MySet.dCount)
                SendResp(data, MySet.Usage, message)

        if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
            return

        else:
            Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)

#---------------------------------------
# Additional functions
#---------------------------------------
def SaveToFile(text):
    """Update countfile"""
    with open(countFile, "w+") as f:
        f.write(text)

def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
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
