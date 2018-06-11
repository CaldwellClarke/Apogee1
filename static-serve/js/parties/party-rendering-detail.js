function loadPartyDetailContainer(partyContainerID, fetchOneId){
  alert(1);
  renderPartyDetail(partyContainerID, fetchOneId);
  addStarFunctionality();
  addJoinFunctionality();
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
      price = '<p class="text-muted" name="min_bid">' + type_icon + ' $' + partyValue.minimum_bid + 
      ' <small class="text-muted"> bid to beat</small></p>'
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
        '<p class="text-muted" name="num_joined">' + partyValue.joins + ' <small class="text-muted">Joined</small></p>' +
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
        '<p class="text-muted" name="num_curr_winners">' + partyValue.num_curr_winners + 
        ' <small class="text-muted">Spots taken</small></p>' +
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
          document.getElementsByName("num_joined")[0].innerHTML = data.num_joined + ' <small class="text-muted">Joined</small>'
        }
        if(partyType == 2){
          document.getElementsByName("min_bid")[0].innerHTML = bid_icon + ' $' + data.min_bid + ' <small class="text-muted">bid to beat</small>'
        }
        if(partyType == 3){
          document.getElementsByName("num_curr_winners")[0].innerHTML = 
          data.num_curr_winners + ' <small class="text-muted">Spots taken</small>'
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

