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
            self.OnlyLive = False
            self.Command = "!redeem"
            self.ignoreredeem = True
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
        self.parent = parent

    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        parent = self.parent
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        self.parent = parent
        if self.CheckSoundFiles() != "":
            MessageBox = ctypes.windll.user32.MessageBoxW
            winsound.MessageBeep()
            returnvalue = MessageBox(0, u"Some soundfiles could not be found."
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

    def CheckSoundFiles(self):
        """Check soundfiles before saving"""
        global soundslist
        soundslist = ""
        for x in range(1, 11):
            fullpath = os.path.join(AudioFilesPath, getattr(self, "r{0}Sound".format(x)))
            if not os.path.isfile(fullpath) and getattr(self, "r{0}PS".format(x)) and getattr(self, "r{0}Enabled".format(x)):
                soundslist += (getattr(self, "r{0}".format(x)) + " - reward{0}".format(x) + "- " + getattr(self, "r{0}Sound".format(x)) + "\r\n")
                self.parent.Log("lista", fullpath)
        return soundslist
