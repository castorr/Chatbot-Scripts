Commands for Streamer
~~~~~~~~~~~~~~~~~~~~~
!bet start	- Start accepting bets
!bet close	- Stop accepting bets
!bet reset	- Remove all current bets
!bet won	- Stop accepting bets and pay out everyone who bet on a win
!bet lost	- Stop accepting bets and pay out everyone who bet on a loss


Command for Viewers
~~~~~~~~~~~~~~~~~~~
!bet win #	- Place a bet on win for # currencypoints
!bet lose #	- Place a bet on lose for # currencypoints


Websocket Events
~~~~~~~~~~~~~~~~
EVENT_BET_STARTED	- Sent when betting is opened
EVENT_BET_CLOSED	- Sent when betting is closed
EVENT_BET_RESET		- Sent when all bets are cleared
EVENT_NEW_BET_WIN	- Sent when a new bet is placed on win. Comes with: userid, username, betsize, betoption, totalwinbets, totalwinpoints
EVENT_NEW_BET_LOSE	- Sent when a new bet is placed on lose. Comes with: userid, username, betsize, betoption, totallosebets, totallosepoints
EVENT_BET_OUTCOM	- Sent when the streamer decides the winning option. Comes with: Winners(amount), winningoption


Version Info
~~~~~~~~~~~~
1.2 Hotfix
Fixed reset not returning points

1.1 Improvement patch 1

[Added] !win # and !lose # are now available for easier voting

[Added] Option to close betting when !bet won or !bet lose is used. 
This was added to be able to use !bet won or !bet lost and have it automatically pay out the currency, 
clear the bets and leave the betting open with a new countdown towards the timer autoclose.

[Added] Messages to correctly show what the script is doing (reset, close, open)

[Added] Action to take when announcing winning option

1.0 Initial Release