# pylint: disable=invalid-name
"""Nightbot parameters"""
from Variables import WeatherApi

class Nightbot():
    """Parse nightbot parameters if enabled"""
    def __init__(self, parent):
        self.parent = parent

    def parameters(self, parseString, userid, targetid, message):
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
            parseString = parseString.replace("$(channel)", self.parent.GetChannelName())

        if "$(query)" in parseString:
            parseString = parseString.replace("$(query)", "$msg")

        if "$(querystring)" in parseString:
            QueryString = urllib.quote_plus(message)
            parseString = parseString.replace("$(querystring)", QueryString)

        if "$(time " in parseString:
            parseString = parseString.replace("$time ", "$readapi(https://beta.decapi.me/misc/time?timezone=")

        #end of nightbot function
        return parseString
