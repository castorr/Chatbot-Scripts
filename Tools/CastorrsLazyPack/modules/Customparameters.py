# pylint: disable=invalid-name
""" parameters"""
import sys
import os
import ast
import time
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Variables import RandUserApi



class Custom():
    """Custom versions of built in parameters"""
    def __init__(self, parent, myset):
        self.parent = parent
        self.myset = myset

    def parameters(self, parseString, userid, targetid, message):
        """Custom versions of built in parameters"""
        if "$ctime" in parseString:
            myTime = time.strftime(self.myset.time, time.localtime(time.time()))
            parseString = parseString.replace("$ctime", myTime)

        if "$cdate" in parseString:
            myDate = datetime.datetime.now().strftime(self.myset.date)
            parseString = parseString.replace("$cdate", myDate)

        if "$cranduser" in parseString:
            api = RandUserApi.replace("$mychannel", self.parent.GetChannelName())
            link = api.format(self.myset.excluded)
            returnValue = self.GetApiData(link)
            parseString = parseString.replace("$cranduser", returnValue)

        if "$ctarget" in parseString:
            parseString = parseString.replace("$ctarget", target.replace("@", ""))

        if "$chours" in parseString:
            if len(message) > 1:
                parseString = parseString.replace("$chours", str(int(self.parent.GetHours(targetid))))
            else:
                parseString = parseString.replace("$chours", str(int(self.parent.GetHours(userid))))

        #end of customparameters function
        return parseString

    def GetApiData(self, link):
        """Convert string to dict from the api"""
        response = self.parent.GetRequest(link, {})
        response = ast.literal_eval(response)
        return response['response']
