/*
js for:
userstatistics/templates/userstatistics.statistics_info_list.html
*/
// I am here
/*******************************GLOBAL VARIABLES*******************************/
//starts general_btn, because on rendering of html we want the general tab to be
//selected
let currSelected ="#general_btn";
//var that holds all data from ajax call/StatisticsInfo serializer object
let statistics="";
//used in google charts
let graphWidth=600;
let graphHeight=300;
//Function that is called once html page is accessed
$(document).ready(function(){
	//First render used to grab data via ajax
	//and render data associated with general tab
	firstRender();
	//Button functionality
	addBtnFunctions();
});
/*******************************UTILITY FUNCTIONS******************************/
//Uses button ids to create a function that fills the button's coloring
//and unfill the previously selected button
//and renders statistics associated with each button name
function addBtnFunctions(){
	$('#general_btn').click(function(e){
  		e.preventDefault();
  		fillSelected(this, "#general_btn");
  		renderGeneralStatistics();
  	})
	$('#lottery_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#lottery_btn");
		renderLotteryStatistics();
	})
	$('#bid_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#bid_btn");
		renderBidStatistics();
	})
	$('#buyout_btn').click(function(e){
		e.preventDefault();
		fillSelected(this, "#buyout_btn");
		renderBuyoutStatistics();
	})
}
//Grabs statistics that will be used in future rendering via ajax GET request
//Waits for success, then renders general statistics page
function firstRender(){
	$.ajax({
		url: '/api/statistics', 
		method: 'GET', 
		success: function(data){
			statistics = data[0]
			renderGeneralStatistics();
		}, 
		error: function(data){
			console.log('error');
	}
  })
}
//takes button class, and the id of the pressed button
//removes bootstrap css filled class from the previously selected button
//adds bootstrap css outline class to previously selected button
//Does reverse for button that was passed through
//sets currently selected button (global) to the id of the new button
function fillSelected(button, id){
	$(currSelected).removeClass('btn btn-secondary');
	$(currSelected).addClass('btn btn-outline-secondary');
	$(button).removeClass('btn btn-outline-secondary');
	$(button).addClass('btn btn-secondary');
	currSelected = id;
}
//render chart loads in google tools
//and calls 4 seperate functions to draw each chart type
//4 functions are used, becauser re-using a function draws over
//the previously drawn chart (and we always want 4 distinct charts rendered)
function renderChart(){
	google.charts.load('current', {'packages':['corechart']});
	google.charts.setOnLoadCallback(drawJoinChart);
	google.charts.setOnLoadCallback(drawJoinEventChart);
	google.charts.setOnLoadCallback(drawStarChart);
	google.charts.setOnLoadCallback(drawStarEventChart);
}
/*************************GENERAL STATISTICS FUNCTIONS*************************/
//Function that is called by general button click to render general stats
function renderGeneralStatistics(){
	renderGeneralMaxEarnings();
	renderGeneralTotalEarnings();
	renderGeneralAverageEarnings();
	renderGeneralNumEvents();
	renderChart();

}
//renders average earnings data/text
function renderGeneralAverageEarnings(){
	let general_average_earnings_display = parseFloat(statistics.general_average_earnings).toFixed(2);
	$('#average_earnings_description').text("Average event earnings: ");
	$('#average_earnings_val').text("$"+general_average_earnings_display);
}
//renders total earnings data/text
function renderGeneralTotalEarnings(){
	let total_earnings_display = parseFloat(statistics.total_earnings).toFixed(2);
	$('#total_earnings_description').text("Total event earnings: ");
	$('#total_earnings_val').text("$"+total_earnings_display);
}
//renders max earnings data/text
function renderGeneralMaxEarnings(){
	let max_profit_display = parseFloat(statistics.max_profit).toFixed(2);
	$('#misc_description').text("Max event earnings: ");
	$('#misc_val').text("$"+max_profit_display);
}
//renders number of events data/text
function renderGeneralNumEvents(){
	$('#num_events_description').text("Number of general events: ");
	$('#num_events_val').text(statistics.total_num_events);
}
/*************************LOTTERY STATISTICS FUNCTIONS*************************/
//Function that is called by lottery button click to render lottery stats
function renderLotteryStatistics(){
	renderLotteryTotalEarnings();
	renderLotteryAverageEarnings();
	renderLotteryTotalParticipants();
	renderLotteryNumEvents();
	renderChart();
}
//renders lottery number of events data/text
function renderLotteryNumEvents(){
	$('#num_events_description').text("Number of lottery events: ");
	$('#num_events_val').text(statistics.lottery_num_events);
}
//renders lottery average earnings data/text
function renderLotteryAverageEarnings(){
	let lottery_average_earnings_display = parseFloat(statistics.lottery_average_earnings).toFixed(2);
	$('#average_earnings_description').text("Average lottery earnings: ");
	$('#average_earnings_val').text("$"+lottery_average_earnings_display);
}
//renders lottery total earnings data/text
function renderLotteryTotalEarnings(){
	let lottery_total_earnings_display = parseFloat(statistics.lottery_total_earnings).toFixed(2);
	$('#total_earnings_description').text("Total lottery earnings: ");
	$('#total_earnings_val').text("$"+lottery_total_earnings_display);
}
//renders lottery total participants data/text
function renderLotteryTotalParticipants(){
	 $('#misc_description').text("Total lottery participants: ");
	 $('#misc_val').text(statistics.lottery_total_participants);
}
/***************************BID STATISTICS FUNCTIONS***************************/
//Function that is called by bid button click to render bid stats
function renderBidStatistics(){
	renderBidTotalEarnings();
	renderBidAverageEarnings();
	renderBidMaxBid();
	renderBidNumEvents();
	renderChart()
}
//renders bid number of events data/text
function renderBidNumEvents(){
	$('#num_events_description').text("Number of bid events: ");
	$('#num_events_val').text(statistics.bid_num_events);
}
//renders bid average earnings data/text
function renderBidAverageEarnings(){
	let bid_average_earnings_display = parseFloat(statistics.bid_average_earnings).toFixed(2);
	$('#average_earnings_description').text("Average bid earnings: ");
	$('#average_earnings_val').text("$"+bid_average_earnings_display);
}
//renders bid total earnings data/text
function renderBidTotalEarnings(){
	let bid_total_earnings_display = parseFloat(statistics.bid_total_earnings).toFixed(2);
	$('#total_earnings_description').text("Total bid earnings: ");
	$('#total_earnings_val').text("$"+bid_total_earnings_display);
}
//renders bid max bid data
function renderBidMaxBid(){
	let bid_max_bid_display = parseFloat(statistics.max_bid_event).toFixed(2);
	 $('#misc_description').text("Maximum amount bid: ");
	 $('#misc_val').text('$' + bid_max_bid_display);
}
/**************************BUYOUT STATISTICS FUNCTIONS*************************/
//Function that is called by buyout button click to render buyout stats
function renderBuyoutStatistics(){
	renderBuyoutTotalEarnings();
	renderBuyoutAverageEarnings();
	renderBuyoutRemoveExtra();
	renderBuyoutNumEvents();
	renderChart();
}
//renders buyout average earnings data/text
function renderBuyoutAverageEarnings(){
	let buyout_average_earnings_display = parseFloat(statistics.buyout_average_earnings).toFixed(2);
	$('#average_earnings_description').text("Average buyout earnings: ");
	$('#average_earnings_val').text("$"+buyout_average_earnings_display);
}
//renders buyout total earnings data/text
function renderBuyoutTotalEarnings(){
	let buyout_total_earnings_display = parseFloat(statistics.buyout_total_earnings).toFixed(2);
	$('#total_earnings_description').text("Total buyout earnings: ");
	$('#total_earnings_val').text("$"+buyout_total_earnings_display);
}
//removes the misc data, as buyout does not have any misc data
function renderBuyoutRemoveExtra(){
	 $('#misc_description').text("");
	 $('#misc_val').text("");
}
//renders bid number of events data/text
function renderBuyoutNumEvents(){
	$('#num_events_description').text("Number of buy events: ");
	$('#num_events_val').text(statistics.buyout_num_events);
}
/***************************CHART RENDERING FUNCTIONS**************************/
/*
All drawXChart() functions are the exact same basic structure
the difference between them is that information about the chart is assumed based
on the function name ex: drawJoinChart() will apply to the #join_time div

drawJoinChart() is commented, each other function works in the exact same manner
just different naming variables, divs, and data array
*/
function drawJoinChart() {
	let array;
	let graphTitle = "Join Time";
	let graphDiv = "join_time";
	let graphAction = "Joins";
	//assigns the data array based on currently selected button and function
	if(currSelected=="#general_btn"){
		array = statistics.general_join_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_join_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_join_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_join_time;
	}
	else{
		return;
	}
	//create a new datatable
	var data = new google.visualization.DataTable();
	data.addColumn('timeofday', 'Time');
	data.addColumn('number', graphAction);
	let i;
	let t = "am"
	let time = 12;
	for(i = 0; i<24;i++){
		//row consists of what number row is being worked on based on hour
		//increments (variable i), the time+':00'+t for the name
		//and adding two array slots together for the data
		//as each index of the array demonstrates half hour increments  
		data.addRow([{v: [i, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
		//if 12:00 am 12:00 PM is reached, reset back to 0
		if(time%12==0){
			time=0;
		}
		//if the time just written is 11:00 am or 11:00 PM
		//switch tag of am to pm to its opposite
		if(time%12==11){
			if(t=="pm"){
				t="am";
			}
			else if(t=="am"){
				t="pm";
			}
		}
		time++;
	}
	//add some options to how the graph is formatted, and its dimensions
    var options = {
        title: graphTitle,
        width: graphWidth,
        height: graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {
        }
      };
      //attach grab to div
      var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));
      //draw the graph
      chart.draw(data, options);
}
function drawJoinEventChart() {
	let array;
	let graphTitle = "Join Event Time";
	let graphDiv = "join_event_time";
	let graphAction = "Joins";
	if(currSelected=="#general_btn"){
		array = statistics.general_join_event_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_join_event_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_join_event_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_join_event_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
	data.addColumn('timeofday', 'Time');
	data.addColumn('number', graphAction);
			let i;
	let t = "am"
	let time = 12;
	for(i = 0; i<24;i++){
		data.addRow([{v: [i, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
		if(time%12==0){
			time=0;
		}
		if(time%12==11){
			if(t=="pm"){
				t="am";
			}
			else if(t=="am"){
				t="pm";
			}
		}
		time++;
	}
      var options = {
        title: graphTitle,
        width:graphWidth,
        height:graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {
        }
      };
      var chart = new google.visualization.ColumnChart(
      document.getElementById(graphDiv));
      chart.draw(data, options);
}
function drawStarChart() {
	let array;
	let graphTitle = "Star Time";
	let graphDiv = "star_time";
	let graphAction = "Stars";

	if(currSelected=="#general_btn"){
		array = statistics.general_star_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_star_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_star_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_star_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
	data.addColumn('timeofday', 'Time');
	data.addColumn('number', graphAction);
	let i;
	let t = "am"
	let time = 12;
	for(i = 0; i<24;i++){
		data.addRow([{v: [i, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
		if(time%12==0){
			time=0;
		}
		if(time%12==11){
			if(t=="pm"){
				t="am";
			}
			else if(t=="am"){
				t="pm";
			}
		}
		time++;
	}
  	var options = {
    title: graphTitle,
    width:graphWidth,
    height:graphHeight,
    hAxis: {
      title: 'Time',
      format: 'h:mm a',
      viewWindow: {
        min: [0, 0],
        max: [23, 0]
      }
    },
    vAxis: {

    }
  };

    var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));

    chart.draw(data, options);
}
function drawStarEventChart() {
	let array;
	let graphTitle = "Star Event Time";
	let graphDiv = "star_event_time";
	let graphAction = "Stars";

	if(currSelected=="#general_btn"){
		array = statistics.general_star_event_time;
	}
	else if(currSelected=="#lottery_btn"){
		array = statistics.lottery_star_event_time;
	}
	else if(currSelected=="#buyout_btn"){
		array = statistics.buyout_star_event_time;
	}
	else if(currSelected=="#bid_btn"){
		array = statistics.bid_star_event_time;
	}
	else{
		return;
	}
	var data = new google.visualization.DataTable();
	data.addColumn('timeofday', 'Time');
	data.addColumn('number', graphAction);
	let i;
	let t = "am"
	let time = 12;
	for(i = 0; i<24;i++){
		data.addRow([{v: [i, 0], f: time+':00'+t}, array[i*2]+array[i*2+1]]);
		if(time%12==0){
			time=0;
		}
		if(time%12==11){
			if(t=="pm"){
				t="am";
			}
			else if(t=="am"){
				t="pm";
			}
		}
		time++;
	}

      var options = {
        title: graphTitle,
        width:graphWidth,
        height:graphHeight,
        hAxis: {
          title: 'Time',
          format: 'h:mm a',
          viewWindow: {
            min: [0, 0],
            max: [23, 0]
          }
        },
        vAxis: {

        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById(graphDiv));

      chart.draw(data, options);
}