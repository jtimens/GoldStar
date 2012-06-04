
//global varibles
var _currentTab;

//on doc ready
$(function()
{
	//sets _currentTab to default value
	if (_currentTab == null)
	{
		_currentTab = "myStars";
	}

	//load objects
	loadCurrentStars();

});

function loadCurrentStars()
{
	if (_currentTab == "myStars")
	{
		console.log("loading myStars");
		loadStars("myStarList");	
	}
	else if (_currentTab == "event")
	{
		console.log("loading event");
		loadStars("eventStarList");	
	}
	if (_currentTab == "leader")
	{
		console.log("loading leader");
		//loadStars();	
	}
	
	
}
//bind events to tab change
//sets current tab
$('a[data-toggle="tab"]').on('shown', function (e) {
    //console.log(e.target) // activated tab
   // console.log(e.relatedTarget) // previous tab

    var currentTab = e.target.toString();
    if (currentTab.indexOf("myStars")  >= 0 )
    {
    	//console.log("myStars");
    	_currentTab = "myStars";
    }
    else if (currentTab.indexOf("event")  >= 0 )
    {
    	//console.log("event");
    	_currentTab = "event";
    }
    else if (currentTab.indexOf("leader")  >= 0 )
    {
    	//console.log("leader");
    	_currentTab = "leader";
    }
    loadCurrentStars();
});

function loadStars(divToFill)
{
			console.log("filling " + divToFill);
			//getJson of stars here
			for (var i=0; i < 10; i++)
			{
			var itemHTML = '';
				itemHTML += '<div class="well" style="height:4em; margin-bottom:0;">'				
				itemHTML += 	'<div style="float:left; width:80%;">'
				itemHTML += 	'	<img class="pull-left" width="40" height="40" style="padding-right:1em;" src="../static/img/goldstar.png" />'
				itemHTML += 		'<span font-size:1.2em;><a href="#">Person One</a> Influenced <a href="#" >Person Two</a></span> <br/>'
				itemHTML += 		'<span style="font-size:1.0em;">at <a href="#" >#MosEisley</a></span><br/>'
				itemHTML += 		'<span style="font-size:0.8em">13 minutes ago </span> <br/>'
				itemHTML += 	'</div>'
				itemHTML += 	'<a href="#">'
				itemHTML += 		'<div style="float:right; height:100%; width:20%;position:relative;">'
				itemHTML += 				'<div class="iconDiv">'
				itemHTML += 				'	<i class="icon-chevron-right pull-right"></i>'
				itemHTML += 			'	</div>	'					
				itemHTML += 		'</div>	'	
				itemHTML += 	'</a>'
				itemHTML += '</div>	'		
				itemHTML += 	'<div style="clear:both"></div>'
				$("#"+divToFill).append(itemHTML);
			}		
}

//modal functionality
function showModal()
{
	$('#myModal').modal('show');
}
