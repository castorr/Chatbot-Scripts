#####################
#   Redeem Script   #
#####################

Description: Let users spend points on redeeming custom rewards
Made By: Castorr91
Website: https://www.twitch.tv/castorr91

#####################
#       Usage       #
#####################
Castorr91: !redeem follow
Castorrbot: Castorr91 spent 100 points to redeem a follow on instagram
#####################
#     Versions      #
#####################
2.0.0	- Updated version to 

1.2.0	- Rewrote most of the code
	- Added option to exclude "redeem " from command
	- Fixed an issue writing to textfile using non ascii characters

1.1.0	- Alerts now support text below image

1.0.10	- !redeem list now only return redeems that the user can actually redeem rather than all redeems
	- Fixed only using !redeem not returning anything

1.0.9	- Improved overlay stability
	- Fixed default cost value for reward 1

1.0.8   - Added Mixer support
        - Removed ton of return statements
        - Added functions for cleaner code
        - Renamed functions for readability
        - Removed unnecessary repetitions

1.0.7   - Updated to work with Youtube & fixed caster ignore cooldown option

1.0.6   - Code cleanup, improved usage stability added option to save message to file

1.0.5   - Fixed cost handling

1.0.4   - Fixed cooldown management
        - Changed version numbering

1.0.0.3 - Added sounds on errorboxes
        - Cleaned up some code

1.0.0.2 - Fixed to work with Streamlabs Chatbot

1.0.0.1 - Added "target2" for chat response
        - Added messagebox when redeem file is reset successfully

1.0.0.0 - Initial Release



#########################################
#    All my scripts can be found in     #
#         the Chatbot discord           #
# https://discordapp.com/invite/J4QMG5m #
#########################################