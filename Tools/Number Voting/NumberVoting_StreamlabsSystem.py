#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Number voting"""

#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import ctypes
import winsound

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Number Voting"
Website = "https://www.twitch.tv/castorr91"
Creator = "Castorr91"
Version = "0.9"
Description = "Let chat vote with numbers in chat"

#---------------------------------------
# Versions
#---------------------------------------
""" Releases (open README.txt for full release notes)
0.9 - Beta testing
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
            self.AllowMulti = False
            self.Min = 1
            self.Max = 100
            self.CloseOnReset = False
            self.SendMessages = True
            self.Opened = "ItsBoshyTime The poll is now OPEN! Go ahead and vote by typing the number in chat ItsBoshyTime "
            self.Closed = "ItsBoshyTime The poll is now CLOSED! ItsBoshyTime "
            self.Reset = "ItsBoshyTime The poll has been cleared! ItsBoshyTime "
            self.NoVotes = "No votes were registered!"
            self.Result = "And the winner is: {0} with {1} votes!"

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
        MySet = Settings()
        MySet.Save(settingsFile)

        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

def ReloadSettings(jsondata):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsondata)

    global wordDict
    voteoptions = range(MySet.Min, MySet.Max+1)
    wordDict = dict((str(values), 0) for values in voteoptions)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    global MySet
    global wordDict
    global voted
    global PollStatus
    global voteoptions

    MySet = Settings(settingsFile)

    voteoptions = range(MySet.Min, MySet.Max+1)

    #create a dict from numbers in voteoptions with a value of 0
    wordDict = dict((str(values), 0) for values in voteoptions)

    voted = []
    PollStatus = False

def Execute(data):
    """Required Execute data function"""
    global PollStatus
    if PollStatus and data.IsChatMessage():
        vote = data.GetParam(0)

        try:
            int(vote)
        except ValueError:
            return

        try:
            int(wordDict[vote])

        except ValueError:
            return

        if vote in wordDict:
            if not MySet.AllowMulti:
                if data.User in voted:
                    return

                wordDict[vote] += 1
                voted.append(data.User)

            else:
                wordDict[vote] += 1
                return

def Tick():
    """Required tick function"""

#---------------------------------------
# [Optional] UI Buttons
#---------------------------------------
def Clear():
    """Reset vote count and who voted"""
    returnValue = MessageBox(0, u"You are about to reset the vote, "
                                "are you sure you want to contine?"
                             , u"Reset poll?", 4)

    if returnValue == MB_YES:
        global wordDict
        global voted

        wordDict = dict((str(values), 0) for values in voteoptions)
        voted = []

        if MySet.SendMessages:
            Parent.SendStreamMessage(MySet.Reset)

    if MySet.CloseOnReset:
        global PollStatus
        PollStatus = False

        if MySet.SendMessages:
            Parent.SendStreamMessage(MySet.Closed)

def Start():
    """Opens the voting"""
    if not PollStatus:
        returnValue = MessageBox(0, u"Poll is now opening, is that ok?"
                                 , u"Open poll?", 1)

        if returnValue == 1:
            global PollStatus
            PollStatus = True

            if MySet.SendMessages:
                Parent.SendStreamMessage(MySet.Opened)

    else:
        returnValue = MessageBox(0, u"Poll is already open!"
                                 , u"Poll open", 0)

def Stop():
    """Stop the voting"""
    if PollStatus:
        returnValue = MessageBox(0, u"Poll is now closing, is that ok?"
                                 , u"Poll closed", 1)

        if returnValue == MB_YES:
            global PollStatus
            PollStatus = False

            if MySet.SendMessages:
                Parent.SendStreamMessage(MySet.Closed)

    else:
        returnValue = MessageBox(0, u"Poll is already closed!"
                                 , u"Poll already closed", 0)

def Winner():
    """Show the winner and remove it from the list of valid votes"""
    global winamount
    winamount = 0
    winners = ''

    for key, val in wordDict.items():
        if val > winamount:
            winners = key
            winamount = val

        elif val == winamount:
            winners += ' ' + key

    if winamount == 0:
        if MySet.SendMessages:
            Parent.SendStreamMessage(MySet.NoVotes)

        returnValue = MessageBox(0, MySet.NoVotes, u"Winner", 0x00000020L | 0)
        return

    winners = sorted(winners.split(), key=int)
    winners = " ".join(str(x) for x in winners)

    if MySet.SendMessages:
        Parent.SendStreamMessage(MySet.Reset.format(winners, str(winamount)))

    returnValue = MessageBox(0, Myset.Result.format(winners, str(winamount) + "\r\n Do you want to rest votes?")
                             , u"Winner", 0x00000020L | 4)

    if returnValue == MB_YES:
        global wordDict
        global voted
        wordDict = dict((str(values), 0) for values in voteoptions)
        voted = []

        if MySet.SendMessages:
            Parent.SendStreamMessage(MySet.Reset)

        if MySet.CloseOnReset:
            global PollStatus
            PollStatus = False

            if MySet.SendMessages:
                Parent.SendStreamMessage(MySet.Closed)

def Unload():
    """Triggers when the bot closes / script is reloaded"""
    if PollStatus and MySet.SendMessages:
        Parent.SendStreamMessage(MySet.Closed)
