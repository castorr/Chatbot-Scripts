#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""A free for all game that is an replica of the built in free for all in case you want two."""
#---------------------------------------
# Libraries and references
#---------------------------------------
from random import shuffle
import codecs
import json
import os
import winsound
import ctypes
import time
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Free For All"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.0.0"
Description = "Additional Free For All game"
#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
1.0.0 - Initial Release
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
            self.Command = "!ffa2"
            self.Cooldown = 1
            self.UseCD = False
            self.Cost = 50
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Usage = "Stream Chat"
            self.StartDelay = 1
            self.MinEntries = 5
            self.MaxSurvivors = 2
            self.NotEnoughResponse = "{0} you don't have enough points!"
            self.PermissionResponse = "{0} -> only {1} ({2}) and higher can use this command"
            self.OpenEntriesMessage = "The arena is now open! Type $command to join!"
            self.StartingMessage = "The combatants have stepped in to the arena.... Who will emerge victorious?!"
            self.AbortMessage = "Not enough people were interested so the Arena has been called off."
            self.FightMessage = "The combatants are going head to head in the arena... You can hear their weapons clashing and sparks fly in all directions... Suddenly a sand storm erupt...."
            self.EndingMessage = "The dust finally settled and only the following people emerged: $results"
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.OffCooldown = "The arena has been cleaned up... Want to go again?! Type $command to start!"

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
    global EntriesOpened
    EntriesOpened = False
    global CooldownRunning
    CooldownRunning = False

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if not HasPermission(data):
            return

        if IsOnCooldown(data):
            return

        if not Parent.RemovePoints(data.User, data.UserName, MySet.Cost):
            NotEnoughResp(data)
            return

        global EntriesOpened
        if not EntriesOpened:
            message = MySet.OpenEntriesMessage
            SendResp(data, MySet.Usage, message)
            EntriesOpened = True
            global UsersList
            UsersList = []
            UsersList.append(data.User)

            global TimeStarted
            TimeStarted = int(time.time())
            return

        if EntriesOpened and not data.User in UsersList:
            global UsersList
            UsersList.append(data.User)

def Tick():
    """Required tick function"""
    global TimeStarted
    global EntriesOpened
    global CooldownRunning
    if CooldownRunning and not Parent.IsOnCooldown(ScriptName, MySet.Command):
        CooldownRunning = False
        message = MySet.OffCooldown.replace("$command", MySet.Command)
        if MySet.Usage == "Discord Chat":
            Parent.SendDiscordMessage(message)
        elif MySet.Usage == "Stream Chat":
            Parent.SendTwitchMessage(message)

    if not EntriesOpened:
        return

    if time.time() - TimeStarted > MySet.StartDelay*60:
        EntriesOpened = False

        global UsersList
        if len(UsersList) < MySet.MinEntries:
            if MySet.Usage == "Discord Chat":
                Parent.SendDiscordMessage(MySet.AbortMessage)
            elif MySet.Usage == "Stream Chat":
                Parent.SendTwitchMessage(MySet.AbortMessage)

            for user in UsersList:
                Parent.AddPoints(user, user, MySet.Cost)

            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown*30)
            CooldownRunning = True

        else:
            if MySet.Usage == "Discord Chat":
                Parent.SendDiscordMessage(MySet.FightMessage)
            elif MySet.Usage == "Stream Chat":
                Parent.SendTwitchMessage(MySet.FightMessage)

            Pot = MySet.Cost * len(UsersList)
            MaxValue = MySet.MaxSurvivors+1
            survivors = Parent.GetRandom(0, MaxValue)
            results = ""

            if survivors > 0:
                WinAmount = Pot / survivors
                shuffle(UsersList)
                survived = ""

                for user in UsersList[:survivors]:
                    survived += user + ", "
                    Parent.AddPoints(user, user, WinAmount)

                results += survived
                results += " (" + str(WinAmount) + ")"
            else:
                WinAmount = 0

            message = MySet.EndingMessage.replace("$results", results)
            if MySet.Usage == "Discord Chat":
                Parent.SendDiscordMessage(message)
            elif MySet.Usage == "Stream Chat":
                Parent.SendTwitchMessage(message)

            Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown*60)
            CooldownRunning = True

#---------------------------------------
# [Optional] Functions for usage handling
#---------------------------------------
def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)
    Message = Message.replace("$permission", MySet.Permission)
    Message = Message.replace("$command", MySet.Command)


    l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and (Usage in l) and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
    if data.IsFromDiscord() and not data.IsWhisper() and (Usage in l):
        Parent.SendDiscordMessage(Message)

def IsFromValidSource(data, Usage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord():
        if not data.IsWhisper() and Usage == "Stream Chat":
            return True

    if data.IsFromDiscord():
        if not data.IsWhisper() and Usage == "Discord Chat":
            return True

    return False

#---------------------------------------
# [Optional] Misc functions
#---------------------------------------

def NotEnoughResp(data):
    """Send message about not having enough currency"""
    currency = Parent.GetCurrencyName()
    notEnough = MySet.NotEnoughResponse.format(data.UserName, currency, MySet.Command)
    SendResp(data, MySet.Usage, notEnough)

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResponse.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, MySet.Usage, message)
        return False
    return True

def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    if Parent.IsOnCooldown(ScriptName, MySet.Command):
        if MySet.UseCD:
            message = MySet.OnCooldown.format(data.UserName, Parent.GetCooldownDuration(ScriptName, MySet.Command))
            SendResp(data, MySet.Usage, message)
        return True
    return False
