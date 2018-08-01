// this is the notification rendering section. it operates similarly to 
      // the party container function
      function loadNotificationContainer(notifContainerID) {
        // VARIABLES
         // this is the set of notifications in the api
        let notifList = [];
        // this links to the following page in the api
        let nextNotifUrl;
        // this is the selector for where we're putting the notification info
        let notifContainer;
        if (notifContainerID){
          notifContainer = $('#' + notifContainerID)
        } else {
          notifContainer = $('#notif-container')
        }
        // url that allows us to get the api data. second is the default
        // data url should be defined in the container specified in the HTML
        let initialUrl = notifContainer.attr('data-url') || '/api/notifications/';

        // TRIGGER FUNCTIONS
        // this changes the seen boolean on each notification on a mouseover
        $(document.body).on('mouseover', '#notif-display', function(e){
          e.preventDefault()
          let this_ = $(this)
          // tells us if the notification has been seen
          let seen = this_.attr('seen-id')
          // gets the notification id for ajax
          let notif_id = this_.attr('data-id')
          // only toggle the color and call to the api is it hasnt been seen yet
          if (seen == 'false'){
            this_.removeClass('grey-background')
            // api endpoint
            let notifUrl = '/api/notifications/' + notif_id 
            // ajax is what actually accesses the API
            $.ajax({
              method: 'GET',
              url: notifUrl,
              success: function(data){
                // this changes the seen attribute so the method doesnt keep triggering
                this_.attr('seen-id', 'true')
              }, 
              error: function(data){
                console.log('error')
                console.log(data)
              }
            })
          }
        })

        // RENDERING FUNCTIONS
        // this is the formatting for thumbnails
        function formatNotification(notifValue){
          // VARIABLES
          let card_highlight = '';
          let seen = 'true'
          // sets the seen vs unseen display parameters
          if (notifValue.seen == false){
            card_highlight = 'grey-background'
            seen = 'false'
          }

          // NOTIFICATION TEXT
          let notif_text = ''
          let link_url = 'href="/events/' + notifValue.party  
          // this sets the text for the 5 notification types
          if (notifValue.action == 'owner_event_close'){
            notif_text = 'Your event, <strong>' + notifValue.party_title + '</strong>, has closed.'
          } else if (notifValue.action == 'owner_reminder'){
            notif_text = 'Your event, <strong>' + notifValue.party_title + '</strong>, starts in 10 minutes!'
          } else if (notifValue.action == 'fan_reminder'){
            notif_text = '<strong>' + notifValue.party_title + '</strong>, with <strong>' + notifValue.party_owner + 
            '</strong>, begins in 10 minutes!'
          } else if (notifValue.action == 'fan_win'){
            notif_text = "You're going to <strong>" + notifValue.party_title + '</strong> with <strong>' + 
            notifValue.party_owner + '</strong> on <strong>' + notifValue.party_time + '</strong>'
          } else if (notifValue.action == 'fan_outbid'){
            notif_text = 'Your bid on <strong>' + notifValue.party_title + '</strong> with <strong>' + 
            notifValue.party_owner + '</strong> is no longer high enough to win.'
          }
          // if there isnt a party anymore, dont delete the notification, just say its gone
          // also get rid of the link to it
          if (notifValue.party_title == null) {
            notif_text = "This event has been deleted."
            link_url = ''
          }
          // the card alows you to click to move to the event it displays
          let container = 
          '<a class="text-dark" ' + link_url +  
          '" style="text-decoration: none;">' +
            '<div class="card mb-2 ' + card_highlight + '" id="notif-display" seen-id=' 
            + seen + ' data-id="' + notifValue.id + '">' +
              '<div class="card-body">' +
                notif_text +
              '</div>' +
            '</div>' + 
          '</a>' 
          
          // just return it immediately
          return container
        }

        // this adds the html to the div we want it in. 
        function parseNotifications(){
          // fetch fills the notificationsList
          if (notifList == 0) {
            notifContainer.text('No notifications :(')
          } else {
            for (let notifIndex = 0; notifIndex < notifList.length; notifIndex++) {
              let notifValue = notifList[notifIndex]
              let notifFormattedHtml = formatNotification(notifValue)
              notifContainer.append(notifFormattedHtml)
            }
          }
        }

        // this calls to the API and gets the party data for the thumbnails
        // the url input is for the loadmore
        function fetchNotifications(url){
          let fetchUrl;
          // if there isnt a url passed, its the first api page
          if (!url) {
            fetchUrl = initialUrl
          } else {
            fetchUrl = url
          }
          $.ajax({
            url: fetchUrl, 
            method: 'GET', 
            success: function(data){
              // the .results is required because of our pagination
              // it sets a new datagrouping outside of the data we're using
              // to describe what the call retrieved
              notifList = data.results
              // if there are more pages in the API, the loadmore appears
              if (data.next) {
                nextNotifUrl = data.next
              } else {
                $('#loadmore').css('display', 'none')
              }
              // it then calls the parse to format them and updates the usernames and 
              // and hashtags
              parseNotifications()
            }, 
            error: function(data){
              console.log('error')
              console.log(data)
            }
          })
        }

        // this calls the fetch methods and starts the chain above
        fetchNotifications()
        

        // this handles our loadmore button
        // it binds a function to any click on something with a loadmore ID
        $('#loadmore').click(function(event){
          event.preventDefault()

          // assuming there are more events, get and show them
          if (nextNotifUrl) {
            fetchNotifications(nextNotifUrl)
          }
        })
      }