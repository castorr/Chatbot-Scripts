# pylint: disable=invalid-name
""" parameters"""
import sys
import os
import ast
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Variables import ViewersApi, MxViewersApi, AgeApi, MxAgeApi


class Phantombot():
    """Parse Phantombot parameters"""
    def __init__(self, parent, myset):
        self.parent = parent
        self.myset = myset

    def parameters(self, parseString, userid, username, targetid, targetname, message):
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
            parseString = parseString.replace("(pointname)", self.parent.GetCurrencyName())

        if "(uptime)" in parseString:
            parseString = parseString.replace("(uptime)", "$uptime")

        if "(game)" in parseString:
            parseString = parseString.replace("(game)", "$mygame")

        if "(status)" in parseString:
            parseString = parseString.replace("(status)", "$mystatus")

        if "(viewers)" in parseString:
            if self.myset.service == "Twitch":
                api = ViewersApi.replace("$mychannel", self.parent.GetChannelName())
            elif self.myset.service == "Mixer":
                api = MxViewersApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(api)
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
            parseString = parseString.replace("(channelname)", self.parent.GetChannelName())

        if "(subscribers)" in parseString:
            parseString = parseString.replace("(subscribers)", "$subcount")

        if "(subscribers)" in parseString:
            parseString = parseString.replace("(subscribers)", "$subcount")

        if "(age)" in parseString:
            if self.myset.service == "Twitch":
                link = AgeApi
            elif self.myset.service == "Mixer":
                link = MxAgeApi
            if len(message) < 2:
                link = link.format(userid)
            else:
                link = link.format(targetid)
            parseString = parseString.replace("(age)", self.GetApiData(link))
        return parseString

    def GetApiData(self, link):
        """Convert string to dict from the api"""
        response = self.parent.GetRequest(link, {})
        response = ast.literal_eval(response)
        return response['response']
