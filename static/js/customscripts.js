function redirect(id)
{
	var page;
	page = document.getElementById(id).id;
	if (page == "giveGoldStar")
		window.location = "giveGold.html";
	else if (page == "myGoldStars")
		window.location = "myGoldStar.html";
	else if (page == "awardedStars")
		window.location = "awardedStar.html";
	else
		window.location = "main.html";
}
function toggleView(id)
{
	
	document.getElementById("gold1").style.display = 'none';
	document.getElementById("gold2").style.display = 'none';
	document.getElementById("gold3").style.display = 'none';
	
	e = document.getElementById(id).id;
	
	if (e == "gg")
		document.getElementById("gold1").style.display = 'block';
	else if (e == "ms")
		document.getElementById("gold2").style.display = 'block';
	else if (e == "as")
		document.getElementById("gold3").style.display = 'block';
	else
		window.location = 'main.html';
}
function toggleInnerView(id)
{
	document.getElementById("goldb2").style.display = 'none';
	document.getElementById("goldc2").style.display = 'none';
	
	e = document.getElementById(id);
	
	if (e.id == "golda")
		alert("You selected " +e+ ".");
	else if (e.id == "goldb")
		document.getElementById("goldb2").style.display = 'block';
	else if (e.id == "btnshow3")
	{
		document.getElementById("tbl3").style.display = 'block';
		e.style.display = 'none';
		toggleBtnShow(e);
	}
	else
		window.location = 'main.html';
}