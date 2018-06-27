# pylint: disable=invalid-name
""" parameters"""
import sys
import os
import ast
import urllib
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Settingsmodule import Settings
from Variables import *

class New():
    """Parse new parameters"""
    def __init__(self, parent, myset):
        self.parent = parent
        self.myset = myset

    def parameters(self, parseString, userid, username, targetid, targetname, message):
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
            if self.myset.imperial:
                parseString = parseString.replace("$weather(", WeatherApi.format("imperial"))
            else:
                parseString = parseString.replace("$weather(", WeatherApi.format("metric"))

        if "$followage" in parseString:
            if self.myset.service == "Twitch":
                link = FollowageApi.replace("$mychannel", self.parent.GetChannelName())
            elif self.myset.service == "Mixer":
                link = MxFollowageApi.replace("$mychannel", self.parent.GetChannelName())
            if len(message) < 2:
                link = link.format(userid)
            else:
                link = link.format(targetid)
            parseString = parseString.replace("$followage", self.GetApiData(link))

        if "$followdate" in parseString:
            if self.myset.service == "Twitch":
                link = FollowdateApi.replace("$mychannel", self.parent.GetChannelName())
                if len(message) < 2:
                    link = link.format(userid)
                else:
                    link = link.format(targetid)
                returnValue = self.GetApiData(link)
            elif self.myset.service == "Mixer":
                returnValue = "[Followdate is currently not supported for Mixer]"

            parseString = parseString.replace("$followdate", returnValue)

        if "$viewers" in parseString:
            if self.myset.service == "Twitch":
                link = ViewersApi.replace("$mychannel", self.parent.GetChannelName())
            elif self.myset.service == "Mixer":
                link = MxViewersApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("$viewers", returnValue)

        if "$views" in parseString:
            if self.myset.service == "Twitch":
                link = ViewsApi.replace("$mychannel", self.parent.GetChannelName())
                returnValue = self.GetApiData(link)
            elif self.myset.service == "Mixer":
                returnValue = "[Currently views parameter isn't available for mixer]"
            parseString = parseString.replace("$views", returnValue)

        if "$avatar" in parseString:
            if self.myset.service == "Twitch":
                link = AvatarApi
            elif self.myset.service == "Mixer":
                link = MxAvatarApi
            if len(message) > 1:
                link = link.format(targetname)
            else:
                link = link.format(username)
            returnValue = self.GetApiData(link)
            returnValue = returnValue.replace("https://mixer.com/_latest/assets/images/main/avatars/default.jpg", "[Avatar not found]")
            parseString = parseString.replace("$avatar", returnValue)

        if "$subemotes" in parseString:
            link = SubEmotesApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("$subemotes", returnValue)

        if "$bttvemotes" in parseString:
            link = BTTVEmotesApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("$bttvemotes", returnValue)

        if "$ffzemotes" in parseString:
            link = FFZEmotesApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("$ffzemotes", returnValue)

        if "$latestyt" in parseString:
            if self.myset.ytuser == "":
                parseString = parseString.replace("$latestyt", "[Error: Youtube channel id not found]")
            else:
                link = LastYTApi.__add__(self.myset.ytuser)
                returnValue = self.GetApiData(link)
                parseString = parseString.replace("$latestyt", returnValue)

        if "$latesttweet" in parseString:
            api = LastTweetApi.__add__(self.myset.twitteruser)
            if self.myset.norts:
                api = api.__add__("&no_rts")
            if self.myset.tweeturl:
                api = api.__add__("&url")
            if self.myset.tweetshort:
                api = api.__add__("&shorten")
            if self.myset.tweethowlong:
                api = api.__add__("&howlong")
            returnValue = self.GetApiData(api)
            parseString = parseString.replace("$latesttweet", returnValue)

        if "$urban(" in parseString:
            parseString = parseString.replace("$urban(", UrbanApi)

        if "$age" in parseString:
            if self.myset.service == "Twitch":
                link = AgeApi
            elif self.myset.service == "Mixer":
                link = MxAgeApi
            if len(message) > 1:
                link = link.format(targetname)
            else:
                link = link.format(username)
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("$age", returnValue)

        if "$ctt" in parseString:
            link = self.myset.ctt.replace("$mychannel", self.parent.GetChannelName())
            urlEnd = urllib.quote_plus(link)
            url = "https://twitter.com/intent/tweet?text=".__add__(urlEnd)
            if self.myset.tweetshort:
                url = "http://tinyurl.com/api-create.php?url={0}".format(url)
            returnValue = self.GetApiData(url)
            parseString = parseString.replace("$ctt", returnValue)

        if "$setctt" in parseString:
            if len(message) > 1:
                self.myset.ctt = message
                Settings.save(self.myset, settingsfile)
                url_end = urllib.quote_plus(self.myset.ctt)
                url = "https://twitter.com/intent/tweet?text=".__add__(url_end)
                if self.myset.tweetshort:
                    url = "http://tinyurl.com/api-create.php?url={0}".format(url)
                    returnValue = self.GetApiData(url)
                parseString = parseString.replace("$setctt", returnValue)
            else:
                parseString = parseString.replace("$setctt", self.myset.cttfailed)

        if "$sessionfollows" in parseString:
            sessionFollows = self.GetTextFileContent(followFile)
            parseString = parseString.replace("$sessionfollows", sessionFollows)

        if "$lastfollow" in parseString:
            lastFollow = self.GetTextFileContent(lastfollowFile)
            parseString = parseString.replace("$lastfollow", lastFollow)

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
                self.parent.BroadcastWsEvent("EVENT_GIF", json.dumps(f, encoding='utf-8-sig'))

                parseString = parseString.replace(fullGif, "")
            else:
                parseString = parseString.replace("$gif", "[ERROR: Seems like you have a space in the () or forgot to set a time]")

        #end of NewParameters function
        return parseString

    def GetApiData(self, link):
        """Convert string to dict from the api"""
        response = self.parent.GetRequest(link, {})
        response = ast.literal_eval(response)
        return response['response']

    def GetTextFileContent(self, textfile):
        """Grabs content from textfile"""
        try:
            with codecs.open(textfile, encoding="utf-8-sig", mode="r") as f:
                return f.readline().strip()
        except FileNotFoundError:
            return ""
