#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Extra parameters including a bunch from other bots"""
#---------------------------------------
# Libraries and references
#---------------------------------------
from collections import deque
import codecs
import winsound
import ast
import sys
import os
import re
import ctypes
import json
import datetime
import time
import urllib
import clr
sys.path.append(os.path.join(os.path.dirname(__file__), "Modules"))
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import WebBrowser, Form, DockStyle
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "CLP "
Creator = "Castorr91"
Version = "1.3"
Description = "Right click -> insert api key | Extra parameters!"
Website = "https://www.twitch.tv/castorr91"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.3
    - Updated due to v2 having compatibility issues for some users
    - Added $label(textfile)
    - Removed $sessionfollows
    - Removed $lastfollow

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
    os.startfile(os.path.join(os.path.dirname(__file__), "sounds"))

def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    os.startfile(os.path.join(os.path.dirname(__file__), "README.txt"))

def OpenFilesFolder():
    """Opens the built in files folder"""
    os.startfile(os.path.join(os.getcwd(), "Services\\" + MySet.service + "\\Files\\"))

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

    global labellocation
    labellocation = os.path.join(os.getcwd(), "Services\\" + MySet.service + "\\Files\\")

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

def EnqueueAudioFile(audiofile):
    """Adds an audio file from the audio folder to the play queue. """
    fullpath = os.path.join(AudioFilesPath, audiofile)
    AudioPlaybackQueue.append(fullpath)
#---------------------------------------
# [Optional] Parse functions
#---------------------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    """Parse function"""
    if MySet.nightbot:
        parseString = Nightbot(parseString, userid, targetid, message)

    if MySet.streamelements:
        parseString = Streamelements(parseString, userid, username)

    if MySet.deepbot:
        parseString = Deepbot(parseString, userid, targetid, message)

    if MySet.phantombot:
        parseString = Phantombot(parseString, userid, username, targetid, targetname, message)

    if MySet.wizebot:
        parseString = Wizebot(parseString)

    parseString = NewParameters(parseString, userid, username, targetid, targetname, message)

    parseString = CustomParameters(parseString, userid, targetid, message)

    return parseString

def CustomParameters(parseString, userid, targetid, message):
    """Custom versions of built in parameters"""
    if "$ctime" in parseString:
        myTime = time.strftime(MySet.time, time.localtime(time.time()))
        parseString = parseString.replace("$ctime", myTime)

    if "$cdate" in parseString:
        myDate = datetime.datetime.now().strftime(MySet.date)
        parseString = parseString.replace("$cdate", myDate)

    if "$cranduser" in parseString:
        api = RandUserApi.replace("$mychannel", Parent.GetChannelName().lower())
        link = api.format(MySet.excluded)
        returnValue = GetApiData(link)
        parseString = parseString.replace("$cranduser", returnValue)

    if "$ctarget" in parseString:
        parseString = parseString.replace("$ctarget", targetid.replace("@", ""))

    if "$chours" in parseString:
        if len(message) > 1:
            parseString = parseString.replace("$chours", str(int(Parent.GetHours(targetid))))
        else:
            parseString = parseString.replace("$chours", str(int(Parent.GetHours(userid))))

    #end of customparameters function
    return parseString

def Deepbot(parseString, userid, targetid, message):
    """Parse deepbot parameters"""
    if "@user@" in parseString:
        parseString = parseString.replace("@user@", userid)

    if "@viewers@" in parseString:
        if MySet.service == "Twitch":
            api = ViewersApi.replace("$mychannel", Parent.GetChannelName())
        elif MySet.service == "Mixer":
            api = MxViewersApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(api)
        parseString = parseString.replace("@viewers@", returnValue)

    if "@time@" in parseString:
        my_time = time.strftime("%I:%M %p", time.localtime(time.time()))
        parseString = parseString.replace("@time@", my_time)

    if "@time24@" in parseString:
        my_time = time.strftime("%H:%M", time.localtime(time.time()))
        parseString = parseString.replace("@time24@", my_time)

    if "@title@" in parseString:
        parseString = parseString.replace("@title@", "$mystatus")

    if "@pointsname@" in parseString:
        parseString = parseString.replace("@pointsname@", Parent.GetCurrencyName())

    if "@target@" in parseString:
        parseString = parseString.replace("@target@", targetid)

    if "@pointstolevelup@" in parseString:
        parseString = parseString.replace("@pointstolevelup@", "$nxtrankreq")

    if "@randomuser@" in parseString:
        parseString = parseString.replace("@randomuser@", "$randuser")

    if "@points@" in parseString:
        parseString = parseString.replace("@points@", "$points")

    if "@intpoints@" in parseString:
        parseString = parseString.replace("@intpoints@", "$pointstext")

    if "@hrstolevelup@" in parseString:
        parseString = parseString.replace("@hrstolevelup@", "$nxtrankreq")

    if "@hours@" in parseString:
        parseString = parseString.replace("@hours@", "$hours")

    if "@getcounter@" in parseString:
        parseString = parseString.replace("@getcounter@", "[PARAMETER ERROR: for getcounter to work properly you need to replace the getcounter with $checkcount(!command) in the command]")

    if "@game@" in parseString:
        parseString = parseString.replace("@game@", "$mygame")

    if "@followers@" in parseString:
        parseString = parseString.replace("@followers@", "$followercount")

    if "@counter@" in parseString:
        parseString = parseString.replace("@counter@", "[PARAMETER ERROR: for counter to work properly you need to replace the counter with $count in the command]")

    if "@followdate@" in parseString:
        if MySet.service == "Twitch":
            api = FollowdateApi.replace("$mychannel", Parent.GetChannelName())
            if len(message) > 1:
                link = api.format(targetid)
            else:
                link = api.format(userid)
            returnValue = GetApiData(link)
        elif MySet.service == "Mixer":
            returnValue = "[Followdate is currently not supported for Mixer]"
        parseString = parseString.replace("@followdate@", returnValue)

    if "@subs@" in parseString:
        parseString = parseString.replace("@subs@", "$subcount")

    if "@customapi@" in parseString:
        parseString = parseString.replace("@customapi@", "[ERROR: customapi needs to be replaced with the built in readapi]")

    #end of deepbotfunction
    return parseString

def NewParameters(parseString, userid, username, targetid, targetname, message):
    """Parse new parameters"""
    if "$default" in parseString:
        result = RegDefault.search(parseString)
        if result:
            fullparameter = result.group(0)
            defaultmessage = result.group("string")
            if len(message) < 2:
                parseString = defaultmessage
            else:
                parseString = parseString.replace(fullparameter, "")

    if "$weather(" in parseString:
        if MySet.imperial:
            parseString = parseString.replace("$weather(", WeatherApi.format("imperial"))
        else:
            parseString = parseString.replace("$weather(", WeatherApi.format("metric"))

    if "$followage" in parseString:
        if MySet.service == "Twitch":
            link = FollowageApi.replace("$mychannel", Parent.GetChannelName())
        elif MySet.service == "Mixer":
            link = MxFollowageApi.replace("$mychannel", Parent.GetChannelName())
        if len(message) < 2:
            link = link.format(userid)
        else:
            link = link.format(targetid)
        parseString = parseString.replace("$followage", GetApiData(link))

    if "$followdate" in parseString:
        if MySet.service == "Twitch":
            link = FollowdateApi.replace("$mychannel", Parent.GetChannelName())
            if len(message) < 2:
                link = link.format(userid)
            else:
                link = link.format(targetid)
            returnValue = GetApiData(link)
        elif MySet.service == "Mixer":
            returnValue = "[Followdate is currently not supported for Mixer]"

        parseString = parseString.replace("$followdate", returnValue)

    if "$viewers" in parseString:
        if MySet.service == "Twitch":
            link = ViewersApi.replace("$mychannel", Parent.GetChannelName())
        elif MySet.service == "Mixer":
            link = MxViewersApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(link)
        parseString = parseString.replace("$viewers", returnValue)

    if "$views" in parseString:
        if MySet.service == "Twitch":
            link = ViewsApi.replace("$mychannel", Parent.GetChannelName())
            returnValue = GetApiData(link)
        elif MySet.service == "Mixer":
            returnValue = "[Currently views parameter isn't available for mixer]"
        parseString = parseString.replace("$views", returnValue)

    if "$avatar" in parseString:
        if MySet.service == "Twitch":
            link = AvatarApi
        elif MySet.service == "Mixer":
            link = MxAvatarApi
        if len(message) > 1:
            link = link.format(targetname)
        else:
            link = link.format(username)
        returnValue = GetApiData(link)
        returnValue = returnValue.replace("https://mixer.com/_latest/assets/images/main/avatars/default.jpg", "[Avatar not found]")
        parseString = parseString.replace("$avatar", returnValue)

    if "$subemotes" in parseString:
        link = SubEmotesApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(link)
        parseString = parseString.replace("$subemotes", returnValue)

    if "$bttvemotes" in parseString:
        link = BTTVEmotesApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(link)
        parseString = parseString.replace("$bttvemotes", returnValue)

    if "$ffzemotes" in parseString:
        link = FFZEmotesApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(link)
        parseString = parseString.replace("$ffzemotes", returnValue)

    if "$latestyt" in parseString:
        if MySet.ytuser == "":
            parseString = parseString.replace("$latestyt", "[Error: Youtube channel id not found]")
        else:
            link = LastYTApi.__add__(MySet.ytuser)
            returnValue = GetApiData(link)
            parseString = parseString.replace("$latestyt", returnValue)

    if "$latesttweet" in parseString:
        api = LastTweetApi.__add__(MySet.twitteruser)
        if MySet.norts:
            api = api.__add__("&no_rts")
        if MySet.tweeturl:
            api = api.__add__("&url")
        if MySet.tweetshort:
            api = api.__add__("&shorten")
        if MySet.tweethowlong:
            api = api.__add__("&howlong")
        returnValue = GetApiData(api)
        parseString = parseString.replace("$latesttweet", returnValue)

    if "$urban(" in parseString:
        parseString = parseString.replace("$urban(", UrbanApi)

    if "$age" in parseString:
        if MySet.service == "Twitch":
            link = AgeApi
        elif MySet.service == "Mixer":
            link = MxAgeApi
        if len(message) > 1:
            link = link.format(targetname)
        else:
            link = link.format(username)
        returnValue = GetApiData(link)
        parseString = parseString.replace("$age", returnValue)

    if "$ctt" in parseString:
        link = MySet.ctt.replace("$mychannel", Parent.GetChannelName())
        urlEnd = urllib.quote_plus(link)
        url = "https://twitter.com/intent/tweet?text=".__add__(urlEnd)
        if MySet.tweetshort:
            url = "http://tinyurl.com/api-create.php?url={0}".format(url)
        returnValue = GetApiData(url)
        parseString = parseString.replace("$ctt", returnValue)

    if "$setctt" in parseString:
        if len(message) > 1:
            MySet.ctt = message
            Settings.save(MySet, settingsfile)
            url_end = urllib.quote_plus(MySet.ctt)
            url = "https://twitter.com/intent/tweet?text=".__add__(url_end)
            if MySet.tweetshort:
                url = "http://tinyurl.com/api-create.php?url={0}".format(url)
                returnValue = GetApiData(url)
            parseString = parseString.replace("$setctt", returnValue)
        else:
            parseString = parseString.replace("$setctt", MySet.cttfailed)

    if "$label(" in parseString:
        result = RegLabel.search(parseString)
        if result:
            fullparam = result.group(0)
            labelfile = result.group("file")
            fullpath = labellocation + labelfile
            if fullpath and os.path.isfile(fullpath):
                parseString = parseString.replace(fullparam, GetTextFileContent(fullpath))
            else:
                parseString = parseString.replace(fullparam, "[ERROR: Labels file not found]")

    if "$torand" in parseString:
        if len(message) > 1:
            parseString = parseString.replace("$torand", targetname)
        else:
            parseString = parseString.replace("$torand", "$randuser")

    if "$sound" in parseString:
        result = RegSound.search(parseString)
        if result:
            fullSound = result.group(0)
            Soundfile = result.group("file")
            fullpath = os.path.join(AudioFilesPath, Soundfile)
            if fullpath and os.path.isfile(fullpath):
                EnqueueAudioFile(Soundfile)
                parseString = parseString.replace(fullSound, "")
            else:
                parseString = parseString.replace(fullSound, "[ERROR: Soundfile not found]")

    if "$gif" in parseString:

        result = RegGif.search(parseString)
        if result:
            fullGif = result.group(0)
            GifLink = result.group("link")

            gifDuration = int(result.group("duration"))
            f = {"duration": gifDuration*1000, "link": GifLink}
            Parent.BroadcastWsEvent("EVENT_GIF", json.dumps(f, encoding='utf-8-sig'))

            parseString = parseString.replace(fullGif, "")
        else:
            parseString = parseString.replace("$gif", "[ERROR: Seems like you have a space in the () or forgot to set a time]")

    if "$cdummy" in parseString:
        if len(message) > 1:
            parseString = ""
        else:
            parseString = parseString.replace("$cdummy", "")

    #end of NewParameters function
    return parseString

def Nightbot(parseString, userid, targetid, message):
    """Parse nightbot parameters if enabled"""

    if "$(user)" in parseString:
        parseString = parseString.replace("$(user)", userid)

    if "$(touser)" in parseString:
        if len(message) > 1:
            parseString = parseString.replace("$(touser)", targetid)
        else:
            parseString = parseString.replace("$(touser)", userid)

    if "$(weather " in parseString:
        parseString = parseString.replace("$(weather ", WeatherApi)

    if "$(urlfetch " in parseString:
        parseString = parseString.replace("$(urlfetch ", "$readapi(")

    if "$(count)" in parseString:
        tempString = ("[PARAMETER ERROR: for count to work properly you need to replace $(count) with $count in the command]")
        parseString = parseString.replace("$(count)", tempString)

    if "$(channel)" in parseString:
        parseString = parseString.replace("$(channel)", Parent.GetChannelName())

    if "$(query)" in parseString:
        parseString = parseString.replace("$(query)", "$msg")

    if "$(querystring)" in parseString:
        QueryString = urllib.quote_plus(message)
        parseString = parseString.replace("$(querystring)", QueryString)

    if "$(time " in parseString:
        parseString = parseString.replace("$time ", "$readapi(https://beta.decapi.me/misc/time?timezone=")

    #end of nightbot function
    return parseString

def Phantombot(parseString, userid, username, targetid, targetname, message):
    """Parse PhantomBot parameters!"""
    if "(sender)" in parseString:
        parseString = parseString.replace("(sender)", username)

    if "(@sender)" in parseString:
        parseString = parseString.replace("(@sender)", "@" + username)

    if "(touser)" in parseString:
        if len(message) > 1:
            parseString = parseString.replace("(touser)", targetid)
        else:
            parseString = parseString.replace("(touser)", userid)

    if "(pointtouser)" in parseString:
        if len(message) > 1:
            parseString = parseString.replace("(pointtouser)", targetname + " ->")
        else:
            parseString = parseString.replace("(pointtouser)", username + " ->")

    if "(currenttime)" in parseString:
        parseString = parseString.replace("(currenttime)", "$time")

    if "(#)" in parseString:
        parseString = parseString.replace("(#)", "$randnum(0,101)")

    if "(random)" in parseString:
        parseString = parseString.replace("(random)", "$randuser")

    if "(pointname)" in parseString:
        parseString = parseString.replace("(pointname)", Parent.GetCurrencyName())

    if "(uptime)" in parseString:
        parseString = parseString.replace("(uptime)", "$uptime")

    if "(game)" in parseString:
        parseString = parseString.replace("(game)", "$mygame")

    if "(status)" in parseString:
        parseString = parseString.replace("(status)", "$mystatus")

    if "(viewers)" in parseString:
        if MySet.service == "Twitch":
            api = ViewersApi.replace("$mychannel", Parent.GetChannelName())
        elif MySet.service == "Mixer":
            api = MxViewersApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(api)
        parseString = parseString.replace("(viewers)", returnValue)

    if "(follows)" in parseString:
        parseString = parseString.replace("(follows)", "$followercount")

    if "(count)" in parseString:
        parseString = parseString.replace("(count)", "[PARAMETER ERROR: for count to work properly you need to replace it with the built in count]")

    if "(senderrank)" in parseString:
        parseString = parseString.replace("(senderrank)", "$rank")

    if "(readfile " in parseString:
        parseString = parseString.replace("(readfile ", "$readline(")

    if "(readfilerand " in parseString:
        parseString = parseString.replace("(readfilerand ", "$readrandline(")

    if "(echo)" in parseString:
        parseString = parseString.replace("(echo)", "$msg")

    if "(titleinfo)" in parseString:
        parseString = parseString.replace("(titleinfo)", "Current title: $mystatus Uptime: $uptime")

    if "(gameinfo)" in parseString:
        parseString = parseString.replace("(gameinfo)", "Current game: $mygame Playtime: $uptime")

    if "(channelname)" in parseString:
        parseString = parseString.replace("(channelname)", Parent.GetChannelName())

    if "(subscribers)" in parseString:
        parseString = parseString.replace("(subscribers)", "$subcount")

    if "(age)" in parseString:
        if MySet.service == "Twitch":
            link = AgeApi
        elif MySet.service == "Mixer":
            link = MxAgeApi
        if len(message) < 2:
            link = link.format(userid)
        else:
            link = link.format(targetid)
        parseString = parseString.replace("(age)", GetApiData(link))
    return parseString

def Streamelements(parseString, userid, username):
    """Parse parameters from StreamElements"""
    if "${user}" in parseString:
        parseString = parseString.replace("${user}", userid)

    if "${user.name}" in parseString:
        parseString = parseString.replace("${user.name}", username)

    if "${user.points}" in parseString:
        parseString = parseString.replace("${user.points}", str(Parent.GetPoints(userid)))

    if "${user.points_rank}" in parseString:
        parseString = parseString.replace("${user.points_rank}", "$pointspos")

    if "${user.time_online}" in parseString:
        parseString = parseString.replace("${user.time_online}", str(Parent.GetHours(userid)))

    if "${user.time_online_rank}" in parseString:
        parseString = parseString.replace("${user.time_online_rank}", "$hourspos")

    if "${sender}" in parseString:
        parseString = parseString.replace("${sender}", userid)

    if "${source}" in parseString:
        parseString = parseString.replace("${source}", userid)

    if "${title}" in parseString:
        parseString = parseString.replace("${title}", "$mystatus")

    if "${status}" in parseString:
        parseString = parseString.replace("${status}", "$mystatus")

    if "${game}" in parseString:
        parseString = parseString.replace("${game}", "$mygame")

    if "${pointsname}" in parseString:
        parseString = parseString.replace("${pointsname}", Parent.GetCurrencyName())

    if "${channel}" in parseString:
        parseString = parseString.replace("${channel}", Parent.GetChannelName())

    if "${channel.viewers}" in parseString:
        if MySet.service == "Twitch":
            link = ViewersApi.replace("$mychannel", Parent.GetChannelName())
        elif MySet.service == "Mixer":
            link = MxViewersApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = self.GetApiData(link)
        parseString = parseString.replace("${channel.viewers}", returnValue)

    if "${channel.views}" in parseString:
        if MySet.service == "Twitch":
            link = ViewsApi.replace("$mychannel", Parent.GetChannelName())
            returnValue = self.GetApiData(link)
        elif MySet.service == "Mixer":
            returnValue = "[Currently this parameter isn't available for mixer]"
        parseString = parseString.replace("${channel.views}", returnValue)

    if "${channel.followers}" in parseString:
        parseString = parseString.replace("${channel.followers}", "$followercount")

    if "${channel.subs}" in parseString:
        parseString = parseString.replace("${channel.subs}", "$subcount")

    if "${random.chatter}" in parseString:
        parseString = parseString.replace("${random.chatter}", "$randuser")

    if "${uptime}" in parseString:
        parseString = parseString.replace("${uptime}", "$uptime")

    if "${count" in parseString:
        parseString = parseString.replace("${count", "[PARAMETER ERROR: for count to work properly you need to replace ${count} with $count in the command]")

    if "${getcount" in parseString:
        parseString = parseString.replace("${getcount", "[PARAMETER ERROR: for count to work properly you need to replace ${getcount} with $checkcount(COMMAND_NAME) in the command]")

    #end of streamlemenets function
    return parseString

def Wizebot(parseString):
    """Parse WizeBot parameters"""

    if "$(channel_name)" in parseString:
        parseString = parseString.replace("$(channel_name)", Parent.GetChannelName())

    if "$(random_viewer)" in parseString:
        parseString = parseString.replace("$(random_viewer)", "$randuser")

    if "$random(" in parseString:
        parseString = parseString.replace("$random(", "$randnum(")

    if "$(current_game)" in parseString:
        parseString = parseString.replace("$(current_game)", "$mygame")

    if "$(current_viewers)" in parseString:
        if MySet.service == "Twitch":
            api = ViewersApi.replace("$mychannel", Parent.GetChannelName())
        elif MySet.service == "Mixer":
            api = MxViewersApi.replace("$mychannel", Parent.GetChannelName())
        returnValue = GetApiData(api)
        parseString = parseString.replace("$(current_viewers)", returnValue)

    if "$(follow_count)" in parseString:
        parseString = parseString.replace("$(follow_count)", "$followercount")

    if "$(sub_count)" in parseString:
        parseString = parseString.replace("$(sub_count)", "$subcount")

    #end of wizebot function
    return parseString

#---------------------------------------
# Variables
#---------------------------------------
settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")
tweetFile = os.path.join(os.path.dirname(__file__), "tweet.txt")
AudioFilesPath = os.path.join(os.path.dirname(__file__), "sounds")
AudioPlaybackQueue = deque()
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6

#Twitch APIs
AgeApi = "https://decapi.me/twitch/creation?user={0}"
AvatarApi = "https://decapi.me/twitch/avatar/{0}"
BTTVEmotesApi = "https://decapi.me/bttv/emotes/$mychannel"
FFZEmotesApi = "https://decapi.me/ffz/emotes/$mychannel"
FollowageApi = "https://beta.decapi.me/twitch/followage/$mychannel/{0}"
FollowdateApi = "https://beta.decapi.me/twitch/followed/$mychannel/{0}"
RandUserApi = "https://decapi.me/twitch/random_user/$mychannel?exclude={0}"
SubEmotesApi = "https://decapi.me/twitch/subscriber_emotes/$mychannel"
ViewersApi = "https://decapi.me/twitch/viewercount/$mychannel"
ViewsApi = "https://decapi.me/twitch/total_views/$mychannel"

#Mixer APIs
MxAgeApi = "http://mixer.api.scorpstuff.com/joineddate.php?user={0}&timezone=UTC"
MxAvatarApi = "http://mixer.api.scorpstuff.com/avatar.php?user={0}"
MxFollowageApi = "http://mixer.api.scorpstuff.com/followed.php?caster=$mychannel&follower={0}"
MxViewersApi = "http://mixer.api.scorpstuff.com/viewercount.php?caster=$mychannel"

#Misc APIs
LastTweetApi = "https://decapi.me/twitter/latest?name="
LastYTApi = "https://decapi.me/youtube/latest_video?id="
UrbanApi = "$readapi(http://jwd.me/twitch/api/urban-dictionary.php?q="
WeatherApi = "$readapi(http://api.scorpstuff.com/weather.php?units={0}&city="

#Regex
RegGif = re.compile(r"(?:\$gif\([\ ]*(?P<link>[^\"\']+)"
                    r"[\ ]*\,[\ ]*(?P<duration>[^\"\']*)[\ ]*\))", re.U)
RegSound = re.compile(r"(?:\$sound\([\ ]*(?P<file>[^\"\']+)[\ ]*\))", re.U)
RegDefault = re.compile(r"\$default\((?P<string>.*?)\)", re.U)
RegQuery = re.compile(r"(?:\$\(querystring[\ ]*(?P<string>[^\"\']+)[\ ]*\))", re.U)
RegLabel = re.compile(r"(?:\$label\([\ ]*(?P<file>[^\"\']+)[\ ]*\))", re.U)

#---------------------------------------
# Settings class
#---------------------------------------
class Settings():
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsfile=None):
        if settingsfile and os.path.isfile(settingsfile):
            with codecs.open(settingsfile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file is found
            self.service = "Twitch"
            self.nightbot = True
            self.streamelements = True
            self.deepbot = True
            self.phantombot = True
            self.wizebot = True
            self.time = "%H:%M:%S"
            self.date = "%d/%m-%Y"
            self.excluded = ""
            self.srmessage = "{0} in order to request a song you need to add a song/video ID, url or a search term"
            self.srenabled = True
            self.imperial = False
            self.volume = 50
            self.ytuser = ""
            self.twitteruser = ""
            self.norts = True
            self.tweeturl = True
            self.tweetshort = True
            self.tweethowlong = True
            self.ctt = "Come join me over at https://www.twitch.tv/$mychannel"
            self.cttfailed = "Failed to update click to tweet link!"

    # Reload settings on save through UI
    def reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            pass
