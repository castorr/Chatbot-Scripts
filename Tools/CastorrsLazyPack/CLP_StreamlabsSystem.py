#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Extra parameters including a bunch from other bots"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import os
import winsound
import ast
import sys
import clr
sys.path.append(os.path.join(os.path.dirname(__file__), "Modules"))
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import WebBrowser, Form, DockStyle
from Settingsmodule import Settings
from Variables import *
from Nightbot import Nightbot
from Deepbot import Deepbot
from Wizebot import Wizebot
from Streamelements import Streamelements
from Phantombot import Phantombot
from Newparameters import New
from Customparameters import Custom
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "CLP"
Creator = "Castorr91"
Version = "1.2.0"
Description = "Right click -> insert api key | Extra parameters!"
Website = "https://www.twitch.tv/castorr91"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.2.0
    - Complete code overhaul
    - Fixed several parameters
        - $chours
        - $followage
        - $followdate

Version infomation for older versions
   can be found in the readme.txt
"""
#---------------------------------------
# [Optional] Settings functions
#---------------------------------------
def ReloadSettings(jsonData):
    """Reload settings on Save"""
    global MySet
    MySet.reload(jsonData)

#---------------------------------------
# [Optional] UI buttons
#---------------------------------------
def SetDefaults():
    """Set default settings function"""
    global MySet
    winsound.MessageBeep()

    returnValue = MessageBox(0, u"You are about to restore the default settings. "
                                "Are you sure you want to continue?"
                             , u"Restore settings?", 4)
    if returnValue == MB_YES:
        MySet = Settings()
        MySet.save(settingsfile)

        returnValue = MessageBox(0, u"Settings successfully restored!"
                                 , u"Restored", 0)

def timeHelp():
    """Opens a information box with all variables available for date and time formatting"""
    MessageBox(0, "\r\n %a - Locale’s abbreviated weekday name."
                  "\r\n %A - Locale’s full weekday name."
                  "\r\n %b - Locale’s abbreviated month name."
                  "\r\n %B - Locale’s full month name."
                  "\r\n %c - Locale’s appropriate date and time representation."
                  "\r\n %d - Day of the month as a decimal number [01,31]."
                  "\r\n %H - Hour (24-hour clock) as a decimal number [00,23]."
                  "\r\n %I - Hour (12-hour clock) as a decimal number [01,12]."
                  "\r\n %j - Day of the year as a decimal number [001,366]."
                  "\r\n %m - Month as a decimal number [01,12]."
                  "\r\n %M - Minute as a decimal number [00,59]."
                  "\r\n %p - Locale’s equivalent of either AM or PM."
                  "\r\n %S - Second as a decimal number [00,61]."
                  "\r\n %U - Week number of the year (Sunday as the first day of the week) as a "
                  "\r\n\tdecimal number [00,53]. All days in a new year preceding the first "
                  "\r\n\tSunday are considered to be in week 0."
                  "\r\n %w - Weekday as a decimal number [0(Sunday),6]."
                  "\r\n %W - Week number of the year (Monday as the first day of the week) as a "
                  "\r\n\tdecimal number [00,53]. All days in a new year preceding the first "
                  "\r\n\tMonday are considered to be in week 0."
                  "\r\n %x - Locale’s appropriate date representation."
                  "\r\n %X - Locale’s appropriate time representation."
                  "\r\n %y - Year without century as a decimal number [00,99]."
                  "\r\n %Y - Year with century as a decimal number."
                  "\r\n %z - Time zone offset indicating a positive/negative time difference from"
                  "\r\n\tUTC/GMT of the form +HHMM or -HHMM, where H represents "
                  "\r\n\tdecimal hour digits and M represents decimal minute digits [-23:59, "
                  "\r\n\t+23:59]."
                  "\r\n %Z - Time zone name (no characters if no time zone exists)."
                  "\r\n %% - A literal '%' character.", "Available format options", 0)

def OpenSoundsFolder():
    """Open specific sound folder"""
    os.startfile(AudioFilesPath)

def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

def OpenFilesFolder():
    """Opens the built in files folder"""
    location = os.path.join(os.getcwd(), "Services\\" + MySet.service + "\\Files\\")
    os.startfile(location)

def ControlC():
    """Copy index.html filepath to clipboard"""
    indexPath = os.path.dirname(os.path.abspath(__file__)) + "\\index.html"
    command = 'echo ' + indexPath.strip() + '| clip'
    os.system(command)

#---------------------------------------
# [Optional] UI buttons (websites)
#---------------------------------------
def SL():
    """Open Streamlabs homepage"""
    OpenLink("https://www.streamlabs.com/")

def Ideas():
    """Open Streamlabs feature suggestions website"""
    OpenLink("https://ideas.streamlabs.com/")

def Bits():
    """Open twitch bits acceptable use policy"""
    OpenLink("https://www.twitch.tv/p/legal/bits-acceptable-use/")

def Blog():
    """Opens twitch blog in default browser"""
    OpenLink("https://blog.twitch.tv/")

def IRLFAQ():
    """Open twitch IRL FAQ"""
    link = "https://help.twitch.tv/customer/portal/articles/2672652-irl-faq"
    OpenLink(link)

def HelpCenter():
    """Open twitch help center"""
    OpenLink("https://help.twitch.tv/")

def LocateYTID():
    """Function to find YouTube Channel ID!"""
    f = Form()
    f.Text = "YouTube Advanced Account Settings"
    f.Width = 630
    f.Height = 630
    wb = WebBrowser()
    wb.ScriptErrorsSuppressed = True
    wb.Navigate("https://www.youtube.com/account_advanced")
    wb.Dock = DockStyle.Fill
    f.Controls.Add(wb)
    f.ShowDialog()

def TGuidelines():
    """Open Twitch Community Guidelines"""
    link = "https://www.twitch.tv/p/legal/community-guidelines/"
    OpenLink(link)

def Twitter():
    """Open the users Twitter link!"""
    OpenLink("https://twitter.com/" + MySet.twitteruser)

def OpenLink(link):
    """Open links through buttons in UI"""
    os.system("explorer " + link)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global MySet
    MySet = Settings(settingsfile)

def Tick():
    """Required tick function"""
    if AudioPlaybackQueue:
        if Parent.PlaySound(AudioPlaybackQueue[0], MySet.volume*0.01):
            AudioPlaybackQueue.popleft()

def Execute(data):
    """Required Execute Data function"""
    if data.IsChatMessage() and MySet.srenabled:
        global Service
        Service = data.Service
        if not (Parent.GetUserCooldownDuration(ScriptName, "!sr", data.User) or Parent.GetUserCooldownDuration(ScriptName, "!songrequest", data.User)):

            commandCheck = data.GetParam(0).lower() == "!sr" or data.GetParam(0).lower() == "!songrequest"
            if commandCheck and data.GetParamCount() < 2:

                if data.IsWhisper():
                    Parent.SendStreamWhisper(data.User, MySet.srmessage.format(data.UserName))
                    Parent.AddUserCooldown(ScriptName, "!sr", data.User, 100)
                    Parent.AddUserCooldown(ScriptName, "!songrequest", data.User, 100)

                else:
                    Parent.SendStreamMessage(MySet.srmessage.format(data.UserName))
                    Parent.AddUserCooldown(ScriptName, "!sr", data.User, 100)
                    Parent.AddUserCooldown(ScriptName, "!songrequest", data.User, 100)

#---------------------------------------
# [Optional] Additional functions
#---------------------------------------
def EnqueueAudioFile(audiofile):
    """ Adds an audio file from the audio folder to the play queue. """
    fullpath = os.path.join(AudioFilesPath, audiofile)
    AudioPlaybackQueue.append(fullpath)

def GetTextFileContent(textfile):
    """Grabs content from textfile"""
    try:
        with codecs.open(textfile, encoding="utf-8-sig", mode="r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        return ""

def GetApiData(link):
    """Convert string to dict from the api"""
    response = Parent.GetRequest(link, {})
    response = ast.literal_eval(response)
    return response['response']

#---------------------------------------
# [Optional] Parse functions
#---------------------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    """Parse function"""
    if MySet.nightbot:
        nightbot = Nightbot(Parent)
        parseString = nightbot.parameters(parseString, userid, targetid, message)

    if MySet.streamelements:
        streamelements = Streamelements(Parent, MySet)
        parseString = streamelements.parameters(parseString, userid, username)

    if MySet.deepbot:
        deepbot = Deepbot(Parent, MySet)
        parseString = deepbot.parameters(parseString, userid, targetid, message)

    if MySet.phantombot:
        phantombot = Phantombot(Parent, MySet)
        parseString = phantombot.parameters(parseString, userid, username, targetid, targetname, message)

    if MySet.wizebot:
        wizebot = Wizebot(Parent, MySet)
        parseString = wizebot.parameters(parseString)

    new = New(Parent, MySet)
    parseString = new.parameters(parseString, userid, username, targetid, targetname, message)

    custom = Custom(Parent, MySet)
    parseString = custom.parameters(parseString, userid, targetid, message)

    return parseString
