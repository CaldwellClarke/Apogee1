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

