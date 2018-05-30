#####################
#  Gamble Minigame  #
#####################

Description: Allow users to gamble currency. High numbers will win. Options for win chance, max bet, min bet, cooldown, responses etc. in UI
Made By: Castorr91
Website: https://www.twitch.tv/castorr91

#####################
#     Versions      #
#####################
2.1.7   - Jackpot now saves and reloads properly

2.1.6   - Fixed username showing as userid for certain messages

2.1.5   - Fixed $permissioninfo
        - Added no currency response

2.1.4	- Fixed jackpot not resetting completely without reload

2.1.3	- Removed lots of return statements
	- Removed lots of comments
	- Addex mixer support

2.1.2	- Fixed permissions

2.1.1	- Increased readability for functions
	- Fixed non-ascii characters for jackpot
	- Fixed revlo advanced
2.1.0   
	- Fixed payouts for Revlo Advanced
        - Fixed Max Bet ammount for Single Number
        - Added functions for the different outcomes
        - Added functions to handle all checks
        - Added button to copy index.html filepath to clipboard
        - Fixed automatic reloading on save
        - Fixed usernames for youtube


2.0.10
	- Fixed SaveSettings is not defined error
	- Fixed jackpot not successfully updating

2.0.9
	- Fixed non ascii characters

2.0.8
	- Hotfix

2.0.7
	- Fixed triplewin

2.0.6
       - Updated to work with youtube
       - Jackpot now also returns the value gambled if won

2.0.5   
       - Fixed cost for random game mode!

2.0.4   
       - Code cleanup, improved usage stability

2.0.3   
       - Fixed max roll value

2.0.2
       - Fixed negative gamble value
       - Changed version numbering
       - Fixed revlo gamemode default min roll value

2.0.1.0
       - Updated to work with Streamlabs Chatbot
       - Added sound and messageboxes upon restoring settings
       - Removed Custom ui group since it was not used at all

2.0.0.9
       - Added more usage options (twitch whisper, twitch both, discord whisper, discord both, whisper both & all)

2.0.0.8
       - Fixed cooldown messages

2.0.0.7
       - Fixed double posting when checking jackpot
       - Fixed typo in UI
       

2.0.0.6
       - Added usage options for discord, twitch or chat both
       - Cleaned up code

2.0.0.5
       - Jackpot is now saved between reloads
       - Added jackpot.txt in the script folder that holds current jackpot size
       - Added option in UI to set jackpot size directly
       - Added button in UI to open README.txt

2.0.0.4
       - Fixed gambling with amount <- broken in 2.0.0.3

2.0.0.3
       - Fixed gamble all

2.0.0.2
       - Fixed Random game mode

2.0.0.1
       - Fixed cooldown for Percentage game mode

2.0.0.0
       - Added game modes
           - Revlo - Uses revlo default values and payouts
           - Revlo Advanced - 3 intervals (lose, win, tripple) with customizable settings
           - Random - Numbers don't matter at all.
                      Set your win chance, win multiplicator and min, max values for the roll.
           - Percentage - Rolls will give a payout in percentage bonus equal to the roll value.
                          0 roll = lost all currency, 100 = doubled currency
           - Single Number - Set a single number that is the winner

       - Added restore default settings button in UI
       - Added option to ignore cooldown for broadcaster
       - Added option to force all in for viewers
       - Added option to change the word used to go all in
       - Added option to enable jackpot mode where each loss adds to the jackpot
               Users can check current jackpot if enabled
       - Cleaned up the code

1.2.0.1 
    - Fixed problem with cooldowns
    - Added min bet option

1.2.0.0
    - Rewrote code from scratch. Easier to follow, shorter lines.
    - Added Max bet option
    - Fixed textboxes info 

1.1.0.2 
    - Added max bet setting
    - cleaned up some code

1.1.0.1 
    - Updated to work with AnkhBot 1.0.2.1 and later

1.1.0.0 
    - Cleaned up code a lot! Fixed probability calculations. 
    - Fixed a bug where users couldn't bet the amount of points they had
    - Added option to only have the command active when stream is live
    - Added checking if variable 1 is a number or not

1.0.1.0 
    - Bug fix, default values with no settings file present

1.0.0.0 
    - Initial release

#####################
#      Usage        #
#####################

!gamble <amount>
Gambles selected amount

!gamble all
Gambles all your points

!gamble
Shows information on how to gamble

!gamble jackpot
Shows the current jackpot value
###################################
# All my scripts can be found in  #
#      the AnkhBot discord        #
#   https://discord.gg/Xv9dzD9    #
###################################