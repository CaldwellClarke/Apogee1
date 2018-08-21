var globalMessageIds = []

function setupChatRoom(){
    // When we're using HTTPS, use WSS too.
    var room_id = Number($('#party-room-id').text())
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/ws/events/?room_id=" + room_id );

    chatsock.onopen = function () {
        console.log("Connected to chat socket");
    }

    chatsock.onclose = function (e) {
        console.log("Disconnected from chat socket", e);
    }

    chatsock.onmessage = function(rawMessage) {
        var message = JSON.parse(rawMessage.data)
        if (!message.error) {
            appendMessage(JSON.parse(message))
        } else {
            alert("Must be logged in to post a message")
        }
    }

    $("#chatform").on("submit", function(event) {
        event.preventDefault()
        var message = {
            command: 'send',
            room_id: room_id,
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
}

function appendMessage(message, prepend) {
        var username = sanitizeHtml(message.username)
        var message = sanitizeHtml(message.message)
        globalMessageIds.push(message)
        var chat = $("#chat")
        var ele = $('<div class="col-xs-12"></div>')

        var messageField = $("<div class='message-container'></div")

        var messageText = $("<p class='message'></p>")
        messageText.append($("<span class='message-username'></span>").text(username + ' : '))
        messageText.append($("<span class='message-message'></span").text(message))

        messageField.append($("<p class='message-timestamp'></p>").text(moment(message.timestamp).local().format('hh:mm a MM-DD')))
        messageField.append(messageText)
        ele.append(messageField)
        
        if (prepend) {
            chat.prepend(ele)
        } else {
            chat.append(ele)
        }
        var chatBox = document.getElementById("chat");
        chatBox.scrollTop = chatBox.scrollHeight;
}

var messagePaginatorGlobal = null

function checkSpawnGetMore(){
    // Check if more messages
    console.log(messagePaginatorGlobal)
    if (messagePaginatorGlobal != null) {
        $("#histLoad").css('display','block')
        $("#histLoad").unbind('click')
        $("#histLoad").click(function(){
            getMessages(messagePaginatorGlobal, function(messages){
                messages.reverse()
                messages.forEach(function(m){
                  appendMessage(m, true)
                });
            })
        })
    } else {
        $("#histLoad").css('display','none')
        return
    }
}

function getMessages(url, callback){
    /*  Gets messages from the api, 
        * num is the number of messages you want
        * skip is the offset from a message
        - setting num to false gets latest */
    var room_id = Number($('#party-room-id').text())
    $.ajax({
        type: "GET",
        url: url || "/api/messages/" + room_id,
    })
    .done(function( data ) {
        messagePaginatorGlobal = data.next
        checkSpawnGetMore()
        callback(data.results.reverse(), true)
    });
}
