# pylint: disable=invalid-name
"""Settings module for the redeem script"""
import codecs
import os
import json
import ctypes
import winsound
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "..", "sounds")

class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, parent, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')
        else: #set variables if no custom settings file is found
            self.onlylive = False
            self.command = "!redeem"
            self.ignoreredeem = False
            self.volume = 50
            self.usage = "Stream Chat"
            self.stf = True
            self.textline = "{0} - {1} - {2} {3} - {4}"
            self.notenough = "{0} -> you don't have the {1} {2} required to redeem this reward."
            self.notavailable = "{0} -> {1} isn't an available reward"
            self.info = "{0} -> you have to define a reward to redeem!"
            self.listbase = "Right now you can redeem: "
            self.notperm = "{0} -> you don't have permission to redeem this reward. permission is: [{1} / {2}]"
            self.listcost = True
            self.usecd = True
            self.oncooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.onusercooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.castercd = True
            self.r1enabled = True
            self.r1 = "follow"
            self.r1cost = 100
            self.r1sm = True
            self.r1message = "{0} spent {1} {2} to redeem a follow on twitch"
            self.r1bws = True
            self.r1localgif = False
            self.r1giflink = "https://media3.giphy.com/avatars/100soft/WahNEDdlGjRZ.gif"
            self.r1duration = 5
            self.r1text = ""
            self.r1ps = True
            self.r1sound = "test.mp3"
            self.r1permission = "Everyone"
            self.r1permissioninfo = ""
            self.r1cooldown = 0
            self.r1usercooldown = 10
            self.r2enabled = False
            self.r2 = ""
            self.r2cost = 100
            self.r2sm = False
            self.r2message = ""
            self.r2bws = False
            self.r2localgif = False
            self.r2giflink = "insert gif link"
            self.r2duration = 5
            self.r2text = ""
            self.r2ps = True
            self.r2sound = "insert sound file"
            self.r2permission = "Everyone"
            self.r2permissioninfo = ""
            self.r2cooldown = 5
            self.r2usercooldown = 10
            self.r3enabled = False
            self.r3 = ""
            self.r3cost = 100
            self.r3sm = False
            self.r3message = ""
            self.r3bws = False
            self.r3localgif = False
            self.r3giflink = "insert gif link"
            self.r3duration = 5
            self.r3text = ""
            self.r3ps = True
            self.r3sound = "insert sound file"
            self.r3permission = "Everyone"
            self.r3permissioninfo = ""
            self.r3cooldown = 5
            self.r3usercooldown = 10
            self.r4enabled = False
            self.r4 = ""
            self.r4cost = 100
            self.r4sm = False
            self.r4message = ""
            self.r4bws = False
            self.r4localgif = False
            self.r4giflink = "insert gif link"
            self.r4duration = 5
            self.r4text = ""
            self.r4ps = True
            self.r4sound = "insert sound file"
            self.r4permission = "Everyone"
            self.r4permissioninfo = ""
            self.r4cooldown = 5
            self.r4usercooldown = 10
            self.r5enabled = False
            self.r5 = ""
            self.r5cost = 100
            self.r5sm = False
            self.r5message = ""
            self.r5bws = False
            self.r5localgif = False
            self.r5giflink = "insert gif link"
            self.r5duration = 5
            self.r5text = ""
            self.r5ps = True
            self.r5sound = "insert sound file"
            self.r5permission = "Everyone"
            self.r5permissioninfo = ""
            self.r5cooldown = 5
            self.r5usercooldown = 10
            self.r6enabled = False
            self.r6 = ""
            self.r6cost = 100
            self.r6sm = False
            self.r6message = ""
            self.r6bws = False
            self.r6localgif = False
            self.r6giflink = "insert gif link"
            self.r6duration = 5
            self.r6text = ""
            self.r6ps = True
            self.r6sound = "insert sound file"
            self.r6permission = "Everyone"
            self.r6permissioninfo = ""
            self.r6cooldown = 5
            self.r6usercooldown = 10
            self.r7enabled = False
            self.r7 = ""
            self.r7cost = 100
            self.r7sm = False
            self.r7message = ""
            self.r7bws = False
            self.r7localgif = False
            self.r7giflink = "insert gif link"
            self.r7duration = 5
            self.r7text = ""
            self.r7ps = True
            self.r7sound = "insert sound file"
            self.r7permission = "Everyone"
            self.r7permissioninfo = ""
            self.r7cooldown = 5
            self.r7usercooldown = 10
            self.r8enabled = False
            self.r8 = ""
            self.r8cost = 100
            self.r8sm = False
            self.r8message = ""
            self.r8bws = False
            self.r8localgif = False
            self.r8giflink = "insert gif link"
            self.r8duration = 5
            self.r8text = ""
            self.r8ps = True
            self.r8sound = "insert sound file"
            self.r8permission = "Everyone"
            self.r8permissioninfo = ""
            self.r8cooldown = 5
            self.r8usercooldown = 10
            self.r9enabled = False
            self.r9 = ""
            self.r9cost = 100
            self.r9sm = False
            self.r9message = ""
            self.r9bws = False
            self.r9localgif = False
            self.r9giflink = "insert gif link"
            self.r9duration = 5
            self.r9text = ""
            self.r9ps = True
            self.r9sound = "insert sound file"
            self.r9permission = "Everyone"
            self.r9permissioninfo = ""
            self.r9cooldown = 5
            self.r9usercooldown = 10
            self.r10enabled = False
            self.r10 = ""
            self.r10cost = 100
            self.r10sm = False
            self.r10message = ""
            self.r10bws = False
            self.r10localgif = False
            self.r10giflink = "insert gif link"
            self.r10duration = 5
            self.r10text = ""
            self.r10ps = True
            self.r10sound = "insert sound file"
            self.r10permission = "Everyone"
            self.r10permissioninfo = ""
            self.r10cooldown = 5
            self.r10usercooldown = 10
        self.parent = parent

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        parent = self.parent
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        self.parent = parent
        if self.ChecksoundFiles() != "":
            messageBox = ctypes.windll.user32.MessageBoxW
            winsound.MessageBeep()
            returnvalue = messageBox(0, u"Some soundfiles could not be found."
                                        "\r\nMake sure the name is correct and that "
                                        "the file is located in the sounds folder"
                                        "\r\nThe following rewards got invalid soundfiles:\r\n{0}"
                                        "\r\nDo you want to open the sounds folder?".format(soundslist)
                                     , u"File not found", 4)
            if returnvalue == 6:
                os.startfile(AudioFilesPath)

    def Save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            self.parent.Log(ScriptName, "Failed to save settings to file.")

    def ChecksoundFiles(self):
        """Check soundfiles before saving"""
        global soundslist
        soundslist = ""
        for x in range(1, 11):
            fullpath = os.path.join(AudioFilesPath, getattr(self, "r{0}sound".format(x)))
            if not os.path.isfile(fullpath) and getattr(self, "r{0}ps".format(x)) and getattr(self, "r{0}enabled".format(x)):
                soundslist += (getattr(self, "r{0}".format(x)) + " - reward{0}".format(x) + "- " + getattr(self, "r{0}sound".format(x)) + "\r\n")
                self.parent.Log("lista", fullpath)
        return soundslist
