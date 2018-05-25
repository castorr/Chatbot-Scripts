# -*- coding: utf-8 -*-
#   Import
# pylint: disable=invalid-name
import json
import os
import codecs
import ctypes
import winsound
#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "Russian Roulette"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "1.17"
Description = "Let the viewers play russian roulette"

"""
# Versions
1.17     Fixed saving settings, fixed game crashing when user had 0 points
1.16     Fixed usernames for Mixer
1.15     Code overhaul, added mixer support
1.14     Updated to use the new scripting functions
1.1.0.3  Fixed 0 cost setting
1.1.0.2  Update information missing
1.1.0.1  Update information missing
1.1.0.0  Update information missing
1.0.0.2: Updated to work with AnkhBot 1.0.2.1 and later!
1.0.0.1: Bug fix default values with no settings file present
1.0.0.0: Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
m_Timeout = "/timeout {0} {1}"
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """Tries to load settings from file if given else set defaults
    The 'default' variable names need to match UI_Config"""
    def __init__(self, settingsFile=None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')
        else:
            self.OnlyLive = False
            self.Command = "!russian"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.Cost = 0
            self.CasterCD = True
            self.UseCD = False
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.Died = "{0} pulls the trigger and .... BOOMB {0} died!"
            self.Survived = "{0} pulls the trigger and .... BOOMB! nothing happens and {0} lives!"
            self.NotEnoughResponse = "{0} you don't have enough {1}! {2} costs {3} {1} "
            self.PermissionResp = "$user -> only $permission ($permissioninfo) and higher can use this command"
            self.Chambers = 6
            self.Bullets = 3
            self.TimeoutEnabled = True
            self.TimeoutLength = 60
            self.RCurrencyEnabled = True
            self.RCurrencyMin = 10
            self.RCurrencyMax = 1000
            self.ACurrencyEnabled = True
            self.ACurrencyMin = 10
            self.ACurrencyMax = 1000

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
        global MySet
        Settings.Save(MySet, settingsFile)

def ReloadSettings(jsondata):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.Reload(jsondata)

#---------------------------------------
# [Required] Base functions
#---------------------------------------
def Init():
    """required init function"""
    global MySet
    MySet = Settings(settingsFile)

def Execute(data):
    """Required Execute data function"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if MySet.OnlyLive and Parent.IsLive() is False:
            return

        if not IsFromValidSource(data):
            return

        if (HasPermission(data) is False):
            return

        if IsOnCooldown(data):
            return

        if Parent.GetPoints(data.User) < MySet.Cost:
            NotEnoughResp(data)
            return

        outcome = Parent.GetRandom(1, MySet.Chambers)
        Parent.RemovePoints(data.User, data.UserName, MySet.Cost)

        if outcome > MySet.Bullets:
            AddAmount = Parent.GetRandom(MySet.ACurrencyMin, MySet.ACurrencyMax)
            message = MySet.Survived.format(data.UserName, MySet.Cost, Parent.GetCurrencyName(), AddAmount)
            SendResp(data, message)

            if MySet.ACurrencyEnabled:
                Parent.AddPoints(data.User, data.UserName, AddAmount)
        else:
            RemoveAmount = Parent.GetRandom(MySet.RCurrencyMin, MySet.RCurrencyMax)
            message = MySet.Died.format(data.UserName, MySet.Cost, Parent.GetCurrencyName(), RemoveAmount, MySet.TimeoutLength)
            SendResp(data, message)

            if MySet.TimeoutEnabled:
                message = m_Timeout.format(data.UserName, MySet.TimeoutLength)
                SendResp(data, message)
            if MySet.RCurrencyEnabled:
                Parent.RemovePoints(data.User, data.UserName, RemoveAmount)

        AddCooldown(data)

def Tick():
    """Required tick function"""

#---------------------------------------
# [Optional] Usage functions
#---------------------------------------
def SendResp(data, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)
    Message = Message.replace("$permission", MySet.Permission)


    Parent.SendStreamMessage(Message)

def IsFromValidSource(data):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord() and not data.IsFromYoutube():
        if not data.IsWhisper():
            return True
    return False

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
                SendResp(data, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, message)
        return True
    return False

def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, message)
        return False
    return True

def NotEnoughResp(data):
    """Send message about not having enough currency"""
    currency = Parent.GetCurrencyName()
    notEnough = MySet.NotEnoughResponse.format(data.UserName, currency, MySet.Command)

    SendResp(data, notEnough)

def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
