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