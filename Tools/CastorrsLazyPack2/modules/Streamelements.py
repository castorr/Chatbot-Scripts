# pylint: disable=invalid-name
""" parameters"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Variables import ViewersApi, ViewsApi, MxViewersApi

class Streamelements():
    """Parse StreamElements parameters"""
    def __init__(self, parent, myset):
        self.parent = parent
        self.myset = myset


    def parameters(self, parseString, userid, username):
        """Parse parameters from StreamElements"""
        if "${user}" in parseString:
            parseString = parseString.replace("${user}", userid)

        if "${user.name}" in parseString:
            parseString = parseString.replace("${user.name}", username)

        if "${user.points}" in parseString:
            parseString = parseString.replace("${user.points}", str(self.parent.GetPoints(userid)))

        if "${user.points_rank}" in parseString:
            parseString = parseString.replace("${user.points_rank}", "$pointspos")

        if "${user.time_online}" in parseString:
            parseString = parseString.replace("${user.time_online}", str(self.parent.GetHours(userid)))

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
            parseString = parseString.replace("${pointsname}", self.parent.GetCurrencyName())

        if "${channel}" in parseString:
            parseString = parseString.replace("${channel}", self.parent.GetChannelName())

        if "${channel.viewers}" in parseString:
            if self.myset.service == "Twitch":
                link = ViewersApi.replace("$mychannel", self.parent.GetChannelName())
            elif self.myset.service == "Mixer":
                link = MxViewersApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("${channel.viewers}", returnValue)

        if "${channel.views}" in parseString:
            if self.myset.service == "Twitch":
                link = ViewsApi.replace("$mychannel", self.parent.GetChannelName())
                returnValue = self.GetApiData(link)
            elif self.myset.service == "Mixer":
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

    def GetApiData(self, link):
        """Convert string to dict from the api"""
        response = self.parent.GetRequest(link, {})
        response = ast.literal_eval(response)
        return response['response']
