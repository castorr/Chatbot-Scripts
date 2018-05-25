#############################
#    Castorr's Lazy Pack    #
#############################

Description: Extra $parameters and !sr info when missing id/url
Made By: Castorr91
Website: https://www.twitch.tv/castorr91

#############################
#         Versions          #
#############################
    1.1.2
	- Added option to select service in settings
	- Fixed copy paste error in UI_Config
	- Removed some comments
	- Cleared unnecessary return statements
	- Made API's into variables
	- $followage, $followdate, $avatar no longer needs () with username
	- Fixed @time@ and @time24@
	- Added $chours
	- Added $default

    1.1.1
	- Hotfix to solve issues with $torand, (pointtouser), (touser), (age), $age, $(touser), $setctt
    1.1.0
	- Fixed use of more than one parameter at once
	- Added usercooldown to !sr and !songrequest
	- Parsing is now using less built in parameters
	- Added options to disable parameters from other bots
	- Removed (1) to (9) because they broke built in parameters
	- Improved compability for gif links


    1.0.14
	- Fixed api's using $mychannel
	- Removed $touser as it's built in now

    1.0.13
	- Updated to work with Youtube
	- $ctt and $setctt now support url shortener

    1.0.12
	- Added buttons for twitch % streamlabs links
	- Fixed twitter usernames
	- Tweaked UI typos

    1.0.1.1
	- $touser now ignores @
	- Added $ctarget

    1.0.1.0
	- Changed filesystem to work with Streamlabs Chatbot
        - Changed YouTube username to ID so it works for everyone
	- 

    1.0.0.9
        - Fixed $setctt and $age
        - Added example commands to readme.txt

    1.0.0.8
        - Updated to work with Streamlabs Chatbot

    1.0.0.7
        - Fixed $(querystring)

    1.0.0.6
        - Added $sound parameter
        - Added $gif parameter
        - Added index.html for overlay
        - Added volume setting in UI for sound levels

    1.0.0.5
        - Added $torand parameter

    1.0.0.4
        - Bugfix for $ctime and $cdate

    1.0.0.3
        - Added $sessionfollows
        - Added $lastfollow
        - Added WizeBot parameters

    1.0.0.2
        - Added $ctt parameter
        - Added $setctt parameter

    1.0.0.1
        - Added StreamElements parameters
        - Added Deepbot parameters
        - Added Phantombot parameters
        - Fixed $urban parameter
        - Added $age parameter

    1.0.0.0 
        - Initial release

#############################
#      New  Parameters      #
#############################

Completely new parameters, most of them are doable through api calls.

$weather(LOCATION)      - Shows the weather for the location
$followage		    - Shows how long the user have been following your channel, if no target is picked it check users
$followdate	   	- shows what date the user followed your channel, if no target is picked it check users
$avatar         - Returns a link to the users twitch avatar in 300x300 pixels
$touser         - Works as $target if one is given, and $user if not
$cviewers        - Shows the current amount of viewers for your channel
$views          - Shows the total amount of views your channel has
$subemotes      - Shows all the sub emotes for your channel
$bttvemotes     - Shows all the BTTV emotes you got in the channel
$ffzemotes      - Shows all the FFZ emotes you got in the channel
$latestyt       - Links your latest YouTube video
$latesttweet    - Your latest tweet - uses the settings set in the UI
$age            - Shows the time of creation for the twitch account specified, if no target is picked it check users
$ctt            - Posts the click to tweet link based on the set link.
$setctt         - Sets the link used for $ctt
$sessionfollows - Show amount of follows for current session
$lastfollow     - Returns name of last follower
$torand         - Returns target and random user if no target is present
$sound(FILE.FORMAT)     - Plays the sound, file must be name.fileformat and be placed in the sounds folder. Example: $sound(Test.mp3)
$gif(<LINK>,<DURATION>) - Shows the gif linked in the index.html for <DURATION> seconds, link can also be the full filepath including fileformat (c:/users/castorr/desktop/test.gif)
$default(MESSAGE)	- Shows the MESSAGE if no argument was put after the command, if there is an argument this parameter doesn't show at all


#############################
#     Example Commands      #
#############################


$weather(LOCATION)      - https://gyazo.com/4fcac95d7d53e21f12626ac81012156a
$followage		- 
$followdate		- 
$avatar      		- 
$touser                 - https://gyazo.com/7d6e92ff518d6a50408fa4045837533e
$viewers                - https://gyazo.com/d5b2326f27942e96004e3c0de6a7c418
$views                  - https://gyazo.com/6bf432a42acb0370e6efe5aadec94b26
$subemotes              - https://gyazo.com/8547dc9c51e289592ba1879b6e76f891
$bttvemotes             - https://gyazo.com/165fa45bc2fc8fe87f349ed87a72e066
$ffzemotes              - https://gyazo.com/93aff00a158696f0785fd3ca938cf51b
$latestyt               - https://gyazo.com/dcc686bd7ff6f37b4d71b6fec33e2788
$latesttweet            - https://gyazo.com/bca763e4a4dd67038763eac065b1a796
$age                    - https://gyazo.com/5eb6f9ca70abf167d43d86716b442fed
$ctt                    - https://gyazo.com/4e56c5ced386b2068b83e82c804460ce
$setctt                 - https://gyazo.com/af080c409e7b0b2cb86aaa03efcf39cc
$sessionfollows         - https://gyazo.com/a2710f2b0acac6317e9c72c06b96f183
$lastfollow             - https://gyazo.com/01d308e6bf46500f340eb49f524816aa
$torand                 - https://gyazo.com/ba07e41cecddd874fc62f48b46d31f46
$sound(FILE.FORMAT)     - https://gyazo.com/cb2924f03ae3533f2b669153ff1fb5ee
$gif(<LINK>,<DURATION>) - https://gyazo.com/664d446be9cafaea2b50f64c3b54a2e2

#############################
#   Modified  Parameters    #
#############################

Customizable version of parameters already existing in the bot.

$ctime          - Like $time but using the format set in the UI
$cdate          - Like $date but using the format set in the UI
$cranduser      - Like $randuser but allows for exclusions, added in the UI
$ctarget	- Works just like $target but ignores @ infront of usernames
$chours		- Return the amount of hours for user or target as a whole number without comma period or space

#############################
#    Nightbot Parameters    #
#############################

Parameters used in nightbot, doesn't offer anything new.
These are added mainly to allow copy pasting commands.

$(user)
$(touser)
$(query)
$(querystring)
$(weather LOCATION)
$(urlfetch API)
$(time TIMEZONE)

#############################
# StreamElements Parameters #
#############################

Parameters used in StreamElements, doesn't offer anything new.
These are added mainly to allow copy pasting commands or from importing

${user}
${user.name}
${user.points}
${user.points_rank}
${user.time_online}
${user.time_online_rank}
${sender}
${source}
${title}
${status}
${game}
${pointsname}
${channel}
${channel.viewers}
${channel.views}
${channel.followers}
${channel.subs}
${random.chatter}
${uptime}

#############################
#    Deepbot Parameters     #
#############################

Parameters used in Deepbot, doesn't offer anything new.
These are added mainly to allow copy pasting commands or from importing

@user@
@viewers@
@time@
@time24@
@title@
@pointsname@
@target@
@pointstolevelup@
@randomuser@
@points@
@intpoints@
@hrstolevelup@
@hours@
@getcounter@
@game@
@followers@
@counter@
@followdate@
@subs@
@customapi@

#############################
#   Phantombot Parameters   #
#############################

Parameters used in Phantombot, doesn't offer anything new.
These are added mainly to allow copy pasting commands or from importing.

(sender)
(@sender)
(touser)
(pointtouser)
(currenttime)
(#)
(1) - (9)
(random)
(pointname)
(uptime)
(game)
(status)
(viewers)
(follows)
(count)
(senderrank)
(readfile FILEPATH/FILE.txt)
(readfilerand FILEPATH/FILE.txt)
(echo)
(titleinfo)
(gameinfo)
(channelname)
(subscribers)
(age)

#############################
#    Wizebot  Parameters    #
#############################

$(channel_name)
$(random_viewer)
$random(min,max)
$(current_game)
$(current_viewers)
$(todayFollow)
$(last_follow_name)
$(session_followers)
$(follow_count)
$(sub_count)

#########################################
#    All my scripts can be found in     #
#    the Streamlabs Chatbot discord     #
# https://discordapp.com/invite/J4QMG5m #
#########################################