# pylint: disable=invalid-name
"""Deepbot parameters"""
import time
import sys
import os
import ast
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Variables import FollowdateApi, ViewersApi, MxViewersApi

class Deepbot():
    """Parse deepbot parameters"""
    def __init__(self, parent, myset):
        self.parent = parent
        self.myset = myset

    def parameters(self, parseString, userid, targetid, message):
        """Parse deepbot parameters"""
        if "@user@" in parseString:
            parseString = parseString.replace("@user@", userid)

        if "@viewers@" in parseString:
            if self.myset.service == "Twitch":
                api = ViewersApi.replace("$mychannel", self.parent.GetChannelName())
            elif self.myset.service == "Mixer":
                api = MxViewersApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(api)
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
            parseString = parseString.replace("@pointsname@", self.parent.GetCurrencyName())

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
            if self.myset.service == "Twitch":
                api = FollowdateApi.replace("$mychannel", self.parent.GetChannelName())
                if len(message) > 1:
                    link = api.format(targetid)
                else:
                    link = api.format(userid)
                returnValue = self.GetApiData(link)
            elif self.myset.service == "Mixer":
                returnValue = "[Followdate is currently not supported for Mixer]"
            parseString = parseString.replace("@followdate@", returnValue)

        if "@subs@" in parseString:
            parseString = parseString.replace("@subs@", "$subcount")

        if "@customapi@" in parseString:
            parseString = parseString.replace("@customapi@", "[ERROR: customapi needs to be replaced with the built in readapi]")

        #end of deepbotfunction
        return parseString

    def GetApiData(self, link):
        """Convert string to dict from the api"""
        response = self.parent.GetRequest(link, {})
        response = ast.literal_eval(response)
        return response['response']
