if( window.WebSocket ){
    //---------------------------------
    //  Variables
    //---------------------------------
    var serviceUrl = "ws://127.0.0.1:3337/streamlabs";
    var socket = new WebSocket(serviceUrl);
    //---------------------------------
    //  Events
    //---------------------------------

    socket.onopen = function()
    {
        // Format your Authentication Information
        var auth = {
            author: "Castorr91",
            website: "https://www.twitch.tv/castorr91",
            api_key: API_Key,
            events: [
                "EVENT_REDEEM",
            ]
        }
        //Send your Data to the server
        socket.send(JSON.stringify(auth));
    };

    socket.onerror = function(error)
    {
        //Something went terribly wrong... Respond?!
        console.log("Error: " + error);
    }

    socket.onmessage = function (message)
    {
        var jsonObject = JSON.parse(message.data);

        if(jsonObject.event == "EVENT_REDEEM")
        {
            //parse jason data
            var MySet = JSON.parse(jsonObject.data);

            //show gif
            document.getElementById("myimg").src=MySet.link;
            document.getElementById("mytext").innerHTML=MySet.text;


            setTimeout(function() {
                document.getElementById("myimg").src="";
                document.getElementById("mytext").innerHTML="";
             }, MySet.duration);
        }
    }
    socket.onclose = function ()
    {
        //  Connection has been closed by you or the server
        console.log("Connection Closed!");
    }
}

