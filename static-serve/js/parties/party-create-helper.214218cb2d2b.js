// this function checks to see if lottery had been selected as the event type 
// if it has, it makes the max_entrants piece visible. otherwise, its hidden.
// it only gets called on the create event page.
function check_event_type(type) {
  // if the event is a lottery
  if(type == 1) {
    // the id tells us where our change is supposed to occur
    // this unhides the max entrants field
    $('#div_id_max_entrants').prop('hidden', false);
    // this hides the minimum bid field
    $('#div_id_minimum_bid').prop('hidden', true);
    // this sets the text for the num winners field
    $("#div_id_num_possible_winners").children('label').text('Number of possible winners*');
    // this sets the text for cost
    $("#div_id_cost").children('label').text('Cost ($)*');
  // if the event is an auction
  } else if (type == 2) {
    // this hides the max entrants field
    $('#div_id_max_entrants').prop('hidden', true);
    // this hides the minimum bid field
    $('#div_id_minimum_bid').prop('hidden', false);
    // this sets the text for the num winners field
    $("#div_id_num_possible_winners").children('label').text('Number of possible winners*');
     // this sets the text for cost
    $("#div_id_cost").children('label').text('Starting Bid ($)*');
  // if the event is a buy
  } else {
    // this hides the max entrants field
    $('#div_id_max_entrants').prop('hidden', true);
    // this hides the minimum bid field
    $('#div_id_minimum_bid').prop('hidden', true);
    // this sets the text for the num winners field
    $("#div_id_num_possible_winners").children('label').text('Number of purchases available*');
     // this sets the text for cost
    $("#div_id_cost").children('label').text('Cost ($)*');
  }
}