function loadPartyDetailContainer(partyContainerID, fetchOneId){
  renderPartyDetail(partyContainerID, fetchOneId);
  addStarFunctionality();
}

function loadPartyListContainer(partyContainerID){
  renderPartyList(partyContainerID);
  addStarFunctionality();
}

function renderPartyList(partyContainerID){
  // this is the set of events in the api
   let query = getParameterByName('q');
  let partyList = [];
  // this links to the following page in the api
  let nextPartyUrl;
  // this is the selector for where we're putting the party info
  let partyContainer;
  if (partyContainerID){
    partyContainer = $('#' + partyContainerID)
  } else {
    partyContainer = $('#party-container')
  }
  // url that allows us to get the api data. second is the default
  // data url should be defined in the container specified in the HTML
  let initialUrl = partyContainer.attr('data-url') || '/api/events/';
  // these are repeatedly used, so they've been converted to variables
  // some should eventually be references to a dictionary
  let star_active = '<i class="fa fa-star yellow-color" aria-hidden="true"></i>';
  let star_inactive = '<i class="fa fa-star grey-color" aria-hidden="true"></i>';
  let free = 'FREE';
  let joined = '';
  let joined_lottery = 'Entry Purchased';
  let joined_bid = 'Bid submitted';
  let joined_buy = 'Event Purchased';
  let lottery_icon = '<i class="fas fa-ticket-alt grey-color" data-toggle="tooltip" data-placement="top" title="Lottery"></i>';
  let bid_icon = '<i class="fas fa-gavel grey-color" data-toggle="tooltip" data-placement="top" title="Auction"></i>';
  let buy_icon = '<i class="fa fa-donate grey-color" data-toggle="tooltip" data-placement="top" title="Buy Now"></i>';
  let closed_icon = '<i class="fas fa-ban grey-color"></i>';

  fetchParties();
  $('#loadmore').click(function(event){
    event.preventDefault()

    // assuming there are more events, get and show them
    if (nextPartyUrl) {
      fetchParties(nextPartyUrl)
    }
  })

  // this calls to the API and gets the party data for the thumbnails
  function fetchParties(url){
    let fetchUrl;

    // if there isnt a url passed, its the first api page, 
    // which is just events from following
    if (!url) {
      fetchUrl = initialUrl
    } else {
      fetchUrl = url
    }
    // actual call to api
    $.ajax({
      url: fetchUrl, 
      data: {
        'q': query
      },
      method: 'GET', 
      success: function(data){
        // the .results is required because of our pagination
        // it sets a new datagrouping outside of the data we're using
        // to describe what the call retrieved
        partyList = data.results

        // if there are more pages in the API, the loadmore appears
        if (data.next) {
          nextPartyUrl = data.next
        } else {
          $('#loadmore').css('display', 'none')
        }
        // it then calls the parse to format them and updates the usernames and 
        // and hashtags
        parseParties()
        updateHashLinks()
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  }

  function parseParties(){
    // partylist should be filled with parties from the fetch call
    if (partyList == 0) {
      partyContainer.text('No events :(')
    } else {
      // make global variable, make responsive
      handSize = 3
      // this iterates through the number of hands in the party list, 
      // then through the number of cards per hand, then formats the 
      // party and adds it to the HTML. each hand is its own div
      for (let deck = 0; deck < partyList.length; deck += handSize) {
        let deckHTML = '<div class="card-deck mb-4">'
        for (let card = 0; card < handSize; card++) {
          let cardIndex = deck + card
          if (cardIndex < partyList.length) {
            let partyValue = partyList[cardIndex]
            let partyFormattedHtml = formatParty(partyValue)
            deckHTML = deckHTML + partyFormattedHtml
          }
        }
        deckHTML = deckHTML + '</div>'
        partyContainer.append(deckHTML)
      }
    }
  }


  function formatParty(partyValue){
    // this sets the star color depending on whether or not 
    // its been starred by the request user
    let verb = star_inactive
    if (partyValue.did_star){
      verb = star_active
    }

    // this sets the text version of the price
    let price = '$' + partyValue.cost
    if (partyValue.cost == 0) {
      price = free
    }
    if (partyValue.event_type == 2){
      price = '$' + partyValue.minimum_bid
    }

    // this checks the event type and sets the correct icon
    let type_icon = ''
    if (partyValue.event_type == 1) {
      type_icon = lottery_icon
    } else if (partyValue.event_type == 2) {
      type_icon = bid_icon
    } else if (partyValue.event_type == 3) {
      type_icon = buy_icon
    }

    // adds small closed icon if event is closed. the tooltip explains the icon
    let closed_display = ''
    if (!partyValue.is_open) {
      closed_display = '<span class="float-right" data-toggle="tooltip" data-placement="top" title="Event Closed">' + closed_icon + '</span>'
    }

    // this is the thumbnail formatting. its built on the
    // card model from bootstrap. it has a top image, a body section 
    // for the title and description, and a footer for name, time, 
    // event type, and star
    let container =  
    '<div class="card" style="max-width: 16rem;">' + 
      '<a class="text-dark" href="/events/' + partyValue.id + '" style="text-decoration: none;">' +
        '<img class="card-img-top" src="' + partyValue.thumbnail_url + '" alt="not here">' + 
      '</a>' +
      '<div class="card-body">' + 
        '<a class="text-dark" href="/events/' + partyValue.id + '" style="text-decoration: none;">' +
          '<h5 class="card-title">' + partyValue.short_title + closed_display + '</h5>' + 
          '<p class="card-text"><span class="description">' + partyValue.short_description + '</span></p>' + 
        '</a>' +
      '</div>' + 
      '<div class="card-footer">' + 
        '<small class="text-muted">With ' + 
          '<a class="text-dark" href="' + partyValue.user.url + '">'+ partyValue.user.username + '</a>' + 
          '<span class="float-right">' + price + ' ' + type_icon + '</span>' +
          '<br>' + partyValue.party_time_display + 
        '</small>' + 
        '<span class="float-right">' + 
          '<a href="#" class="starBtn text-dark" data-id="' + partyValue.id + '">' + verb + '</a>' + 
        '</span>' + 
      '</div>' + 
    '</div>'
    // just return it immediately
    return container
  }

  function updateHashLinks(){
    // this is where the actual title and description are held
    // the span allows up to properly id the hashtags in the description
    // it will not highlight anf link a hashtag in the title
    $('.description').each(function(data){
      let hashtagRegex = /(^|\s)#([\w\d-]+)/g // pulls hashtags
      let usernameRegex = /(^|\s)@([\w\d-]+)/g // pulls user mentions
      let currentHtml = $(this).html()
      let newText;
      // the regex returns stuff before and after
      // the replace puts the tag in and then makes a link for the text
      newText = currentHtml.replace(hashtagRegex, '$1<a class="text-dark" href="/tags/$2/">#$2</a>')
      newText = newText.replace(usernameRegex, '$1<a class="text-dark" href="/profiles/$2/">@$2</a>')
      $(this).html(newText)
    })
  }
}




function renderPartyDetail(partyContainerID, fetchOneId){
  // this is the set of events in the api
  let partyList = [];
  // this links to the following page in the api
  let nextPartyUrl;
  // this is the selector for where we're putting the party info
  let partyContainer;
  if (partyContainerID){
    partyContainer = $('#' + partyContainerID)
  } else {
    partyContainer = $('#party-container')
  }
  // url that allows us to get the api data. second is the default
  // data url should be defined in the container specified in the HTML
  let initialUrl = partyContainer.attr('data-url') || '/api/events/';
  // these are repeatedly used, so they've been converted to variables
  // some should eventually be references to a dictionary
  let star_active = '<i class="fa fa-star yellow-color" aria-hidden="true"></i>';
  let star_inactive = '<i class="fa fa-star grey-color" aria-hidden="true"></i>';
  let free = 'FREE';
  let joined = '';
  let joined_lottery = 'Entry Purchased';
  let joined_bid = 'Bid submitted';
  let joined_buy = 'Event Purchased';
  let lottery_icon = '<i class="fas fa-ticket-alt grey-color" data-toggle="tooltip" data-placement="top" title="Lottery"></i>';
  let bid_icon = '<i class="fas fa-gavel grey-color" data-toggle="tooltip" data-placement="top" title="Auction"></i>';
  let buy_icon = '<i class="fa fa-donate grey-color" data-toggle="tooltip" data-placement="top" title="Buy Now"></i>';
  let closed_icon = '<i class="fas fa-ban grey-color"></i>';
  fetchSingle(fetchOneId);
  addJoinFunctionality();

 // this allows search along hashtags. its called upon creation
  // could be useful for categorization
  function updateHashLinks(){
    // this is where the actual title and description are held
    // the span allows up to properly id the hashtags in the description
    // it will not highlight anf link a hashtag in the title
    $('.description').each(function(data){
      let hashtagRegex = /(^|\s)#([\w\d-]+)/g // pulls hashtags
      let usernameRegex = /(^|\s)@([\w\d-]+)/g // pulls user mentions
      let currentHtml = $(this).html()
      let newText;
      // the regex returns stuff before and after
      // the replace puts the tag in and then makes a link for the text
      newText = currentHtml.replace(hashtagRegex, '$1<a class="text-dark" href="/tags/$2/">#$2</a>')
      newText = newText.replace(usernameRegex, '$1<a class="text-dark" href="/profiles/$2/">@$2</a>')
      $(this).html(newText)
    })
  }
  function formatSingle(partyValue){
    // sets the star color
    let star_verb = star_inactive
    if (partyValue.did_star){
      star_verb = star_active
    }
    // this contains the pieces that every event has at the top. title, name, time, star, desc, etc.
    let detail_header = '<div class="row mt-3">' +
      '<div class="col-sm-4">' +  
        '<img class="img-fluid rounded mx-auto" src="' + partyValue.thumbnail_url + '" alt="not here">' + 
      '</div>' +
      '<div class="col-sm-8">' +
        '<h1 style="word-wrap: break-word;">' + partyValue.title + 
          '<span class="float-right">' + 
            '<a href="#" class="starBtn text-dark" data-id="' + partyValue.id + '">' + star_verb + '</a>' + 
          '</span>' + 
        '</h1>' +
        '<small class="text-muted">With ' + 
          '<a class="text-dark" href="' + partyValue.user.url + '">'+ partyValue.user.username + '</a> On ' + partyValue.party_time_display + 
        '</small><br>' + 
        '<p class="lead mt-4" style="word-wrap: break-word;">' + partyValue.description + '</p>' + 
      '</div>' +
    '</div>'

    // selects event type icon 
    let type_icon = ''
    let join = ''
    if (partyValue.event_type == 1) {
      type_icon = lottery_icon
      join = "Enter Lottery"
      joined = joined_lottery
    } else if (partyValue.event_type == 2) {
      type_icon = bid_icon
      join = "Submit a Bid"
      joined = joined_bid
    } else if (partyValue.event_type == 3) {
      type_icon = buy_icon
      join = "Buy Event"
      joined = joined_buy
    }

    // this sets the price text
    let price = '<p class="text-muted">' + type_icon + ' $' + partyValue.cost + '</p>' 
    if (partyValue.cost == 0) {
      price = '<p class="text-muted">' + type_icon + ' ' + free + '</p>' 
    } if (partyValue.event_type == 2) {
      price = '<p class="text-muted">' + type_icon + ' $<span name="min_bid">' + partyValue.minimum_bid + 
      '</span><small class="text-muted"> bid to beat</small></p>'
    }
    // only displays the time until close if the event is still open
    let timeuntil = ''
    if (partyValue.is_open) {
      timeuntil = '<p class="text-muted">' + partyValue.timeuntil + 
      ' <small class="text-muted"> until close</small></p>'
    }
    // if there is no max entrants, it doesnt display
    let max_entrants = '<p class="text-muted">' + partyValue.max_entrants + 
      ' <small class="text-muted">Max entrants</small></p>'
    if (partyValue.max_entrants == null) {
      max_entrants = '<p class="text-muted">Unlimited<small class="text-muted"> entrants</small></p>'
    }
    // changes the winners display on buy event
    let possible_winners = '<p class="text-muted">' + partyValue.num_possible_winners + 
    ' <small class="text-muted">Winners possible</small></p>'
    if (partyValue.event_type == 3) {
      possible_winners = '<p class="text-muted">' + partyValue.num_possible_winners + 
      ' <small class="text-muted">Spots total</small></p>'
    }
    // this sets the bid input so that owners dont see it
    let bid_input = ''
    if (!partyValue.is_owner) {
      bid_input = '<form id= "bid-submit" method="GET">'+
      '<div class="col-sm-12" id="div_bid_amount">'+
      '<input type="number" step="0.01" id="bid_amount" name="bid_amount" ' + '{{ request.GET.bid_amount }}' + '">'+
      '</div>'+
      '</form>'+
      '<div class="col-sm-20">'+
      '<input type="hidden" name="party_id" value="' + partyValue.id + '">'+
      '</div>'
    }
    // this sets the display of the join button
    let join_verb = ''
    if (!partyValue.is_owner){
        join_verb = '<button type="button" class="btn btn-outline-secondary btn-block m-3 joinBtn joinDisplay" data-id="' 
        + partyValue.id + '" event-id="'+partyValue.event_type+'">' + join + '</button>'
      if (partyValue.did_join) {
        join_verb = '<button type="button" class="btn btn-outline-secondary btn-block m-3 joinBtn joinDisplay disabled" data-id="' 
        + partyValue.id + '" disabled>' + joined + '</button>'
      }
    } 

    // replaces the join button with a closed message if the event is over
    if (!partyValue.is_open) {
      join_verb = '<p class="mx-auto lead text-center text-muted">This Event Has Ended</p>'
    }

    // this displays the winners if they've been selected
    let winner = ''
    if (partyValue.winner_names.length > 0) {
      winner = '<div class="row mt-3"><h1 class="mx-auto"> ' + partyValue.winner_names + 
      ' is the winner!</h1></div>'
    }
   

    // this formats the event on the detail page. it has a thumbnail on the top 
    // left, the title and star on the top right, the name, time, and full 
    // description, below. below that is the price, type, and the join button
    if(partyValue.event_type == 1){
       let container = detail_header +
    '<div class="row mt-3">' + 
      '<div class="col-sm-12">' + 
        price + 
      '</div>' +
      '<div class="col-sm-12">' + 
        timeuntil +
      '</div>' +
      '<div class="col-sm-12">' + 
        '<p class="text-muted"><span name="num_joined">' + partyValue.joins + '</span> <small class="text-muted">Joined</small></p>' +
      '</div>' +
      '<div class="col-sm-12">' + 
        max_entrants + 
      '</div>' +
      '<div class="col-sm-12">' + 
        possible_winners + 
      '</div>' +
    '</div>' +
    '<div class="row">' + join_verb + '</div>' + winner 

    return container
    }

    if(partyValue.event_type == 2){
      let container = detail_header +
    '<div class="row mt-3">' + 
      '<div class="col-sm-12">' + 
        price + 
      '</div>' +
      '<div class="col-sm-12">' + 
        timeuntil +
      '</div>' +
      '<div class="col-sm-12">' + 
        possible_winners + 
      '</div>' +
    '</div>' +
    bid_input +
    '<div class="row">' + join_verb + '</div>' + winner 

    return container
    }
    
    if(partyValue.event_type == 3){
       let container = detail_header +
    '<div class="row mt-3">' + 
      '<div class="col-sm-12">' + 
        price + 
      '</div>' +
      '<div class="col-sm-12">' + 
        timeuntil +
      '</div>' +
      '<div class="col-sm-12">' + 
        '<p class="text-muted"><span name="num_curr_winners">' + partyValue.num_curr_winners + 
        '</span> <small class="text-muted">Spots taken</small></p>' +
      '</div>' +
      '<div class="col-sm-12">' + 
        possible_winners + 
      '</div>' +
    '</div>' +
    '<div class="row">' + join_verb + '</div>' + winner 

    return container
    }
   
  }

  function parseSingle(){
    let partyValue = partyList[0]
    let partyFormattedHtml = formatSingle(partyValue)
    partyContainer.append(partyFormattedHtml) 
  }
 // this accesses the event data for a single detail event
  function fetchSingle(fetchOneId){
    // leading slash appends it to the base url. 
    // no leading slash sends it to the url of the page its on
    // which would be /events/id/api/events/id 
    let fetchDetailUrl = '/api/events/' + fetchOneId + '/'
    // actual call to api
    $.ajax({
      url: fetchDetailUrl, 
      method: 'GET', 
      success: function(data){
        console.log(data)
        partyList = data.results
        parseSingle()
        updateHashLinks()
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  }



function addJoinFunctionality(){
  $(document.body).on("click", '.joinBtn', function(e){
    e.preventDefault()

    let this_ = $(this)
    // selector for the button. makes sure we have the event id 
    let partyID = this_.attr('data-id')
    let partyType = this_.attr('event-id')
    console.log("The party is "+partyType)
    // api endpoint
    let joinedUrl;
    if(partyType == 1 || partyType == 3){
      joinedUrl = '/api/events/' + partyID + '/join/'
    }
    else{
      let bid = document.getElementsByName("bid_amount")[0].value
      joinedUrl = '/api/events/' + partyID + '/join/'+ bid
    }
    
    // ajax accesses the api
    $.ajax({
      method: 'GET',
      url: joinedUrl,

      success: function(data){
        if(partyType == 1){
          document.getElementsByName("num_joined")[0].innerHTML = data.num_joined 
        }
        if(partyType == 2){
          document.getElementsByName("min_bid")[0].innerHTML = data.min_bid 
        }
        if(partyType == 3){
          document.getElementsByName("num_curr_winners")[0].innerHTML = 
          data.num_curr_winners 
        }
        if(data.error_message!=""){
          alert(data.error_message)
        }
        if(data.error_message == ''){
          this_.prop('disabled', true)
          this_.text(joined)
        }
        console.log(this_)
        console.log(data.min_bid)
        // the api handles updating the database 
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  })
}


}




// this is the favorite function. It wil be instrumental in enabling 
// users to track events as they progress.
// its built to trigger on click for any button with the correct class
function addStarFunctionality(){
  $(document.body).on("click", '.starBtn', function(e){
    e.preventDefault()
    let this_ = $(this)
    // selector for the button. makes sure we're starring the correct button
    let partyID = this_.attr('data-id')
    // api endpoint
    let starredUrl = '/api/events/' + partyID + '/star/'
    // ajax is what actually accesses the API
    $.ajax({
      method: 'GET',
      url: starredUrl,
      success: function(data){
        // the api handles updating the database and the method below
        // updates the color, so nothing happens on success
      }, 
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  })
// this controls the display color of the favorite button
// its linked to a different class to ensure nothing wierd happens 
// with the click trigger
  $(document.body).on("click", '.fa-star', function(e){
    e.preventDefault()
    let this_ = $(this)
    // one of these classes is activated by the formatting below, 
    // so the two toggles are never on at the same time
    this_.toggleClass('grey-color')
    this_.toggleClass('yellow-color')
  })
}

function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}