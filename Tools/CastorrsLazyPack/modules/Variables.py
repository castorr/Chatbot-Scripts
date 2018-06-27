#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Variables"""
from collections import deque
import os
import re
import ctypes

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
UrbanApi = "$readapi(http://api.scorpstuff.com/urbandictionary.php?term="
WeatherApi = "$readapi(http://api.scorpstuff.com/weather.php?units={0}&city="

#Regex
RegGif = re.compile(r"(?:\$gif\([\ ]*(?P<link>[^\"\']+)"
                    r"[\ ]*\,[\ ]*(?P<duration>[^\"\']*)[\ ]*\))", re.U)
RegSound = re.compile(r"(?:\$sound\([\ ]*(?P<file>[^\"\']+)[\ ]*\))", re.U)
RegDefault = re.compile(r"\$default\((?P<string>.*?)\)", re.U)
RegQuery = re.compile(r"(?:\$\(querystring[\ ]*(?P<string>[^\"\']+)[\ ]*\))", re.U)
