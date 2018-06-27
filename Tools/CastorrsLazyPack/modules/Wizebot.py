# pylint: disable=invalid-name
""" parameters"""
import ast
from Variables import ViewersApi, MxViewersApi

class Wizebot():
    """Parse  parameters"""
    def __init__(self, parent, myset):
        self.parent = parent
        self.myset = myset

    def parameters(self, parseString):
        """Parse WizeBot parameters"""
        if "$(channel_name)" in parseString:
            parseString = parseString.replace("$(channel_name)", self.parent.GetChannelName())

        if "$(random_viewer)" in parseString:
            parseString = parseString.replace("$(random_viewer)", "$randuser")

        if "$random(" in parseString:
            parseString = parseString.replace("$random(", "$randnum(")

        if "$(current_game)" in parseString:
            parseString = parseString.replace("$(current_game)", "$mygame")

        if "$(current_viewers)" in parseString:
            if self.myset.service == "Twitch":
                api = ViewersApi.replace("$mychannel", self.parent.GetChannelName())
            elif self.myset.service == "Mixer":
                api = MxViewersApi.replace("$mychannel", self.parent.GetChannelName())
            returnValue = self.GetApiData(api)
            parseString = parseString.replace("$(current_viewers)", returnValue)

        if "$(follow_count)" in parseString:
            parseString = parseString.replace("$(follow_count)", "$followercount")

        if "$(sub_count)" in parseString:
            parseString = parseString.replace("$(sub_count)", "$subcount")

        #end of wizebot function
        return parseString

    def GetApiData(self, link):
        """Convert string to dict from the api"""
        response = self.parent.GetRequest(link, {})
        response = ast.literal_eval(response)
        return response['response']
