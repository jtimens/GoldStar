function canUseStorage()
{
	if(typeof(Storage)!=="undefined")
	{
		return true;
	}
	else
	{
		alert("Your browser does not support local storage.");
		return false;
	}
}
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
function login()
{
	if (canUseStorage())
	{
		var em = document.getElementById('txtemail').value;
		$.getJSON('/api/user', function(jdata){
			var i = 0;
			var rv = false;
			if (jdata.objects.length == 0)
			{
				alert("no users.");
			}
			else
			{
				for(i=0;i<jdata.objects.length;++i)
				{
					var jsonEmail = jdata.objects[i].email;
					if (em.toLowerCase() == jsonEmail.toLowerCase())
					{
						rv = true;
						sessionStorage.userID = jdata.objects[i].id;
					}
				}
				if(rv)
				{
					//document.getElementById("madeaccount").style.display = "none";
					window.location = "main.html";
				}	
				else
					alert("Email not found.");
			}
		})
	}
	else
	{
		alert("Update your browser to use this site.");
	}
	
}
function userLogout()
{
	sessionStorage.clear();
	window.location = 'index.html';
}
function toggleLoginView(id)
{
	document.getElementById("index1").style.display = 'none';
	document.getElementById("index2").style.display = 'none';
	
	e = document.getElementById(id);
	
	if (e.id == "login1")
		document.getElementById("index2").style.display = 'block';
	if (e.id == "login2")
		document.getElementById("index1").style.display = 'block';
}
function toggleView(id)
{
	document.getElementById("gold1").style.display = 'none';
	document.getElementById("gold2").style.display = 'none';
	document.getElementById("gold3").style.display = 'none';
	
	e = document.getElementById(id).id;
	
	if (e == "gg")
	{
		document.getElementById("gold1").style.display = 'block';
		resetView();
	}
	else if (e == "ms")
		document.getElementById("gold2").style.display = 'block';
	else if (e == "as")
		document.getElementById("gold3").style.display = 'block';
	else
		window.location = 'main.html';
}
function toggleInnerView(id)
{
	
	e = document.getElementById(id);
	
	if (e.id == "btnshow1")
	{
		document.getElementById("tbl1").style.display = 'block';
		document.getElementById("give1").style.display = 'block';
	}
	else if (e.id == "btnshow2" || e.id == "btnhide2")
	{
		if (e.id == "btnshow2")
		{
			document.getElementById("btnhide2").style.display = 'block';
			document.getElementById("tbl2").style.display = 'block';
			e.style.display = 'none';
		}
		else
		{
			document.getElementById("btnshow2").style.display = 'block';
			document.getElementById("tbl2").style.display = 'none';
			e.style.display = 'none';
		}	
	}
	else if (e.id == "btnshow3" || e.id == "btnhide3")
	{
		if (e.id == "btnshow3")
		{
			document.getElementById("btnhide3").style.display = 'block';
			document.getElementById("tbl3").style.display = 'block';
			e.style.display = 'none';
		}
		else
		{
			document.getElementById("btnshow3").style.display = 'block';
			document.getElementById("tbl3").style.display = 'none';
			e.style.display = 'none';
		}	
	}
	else
		window.location = 'main.html';
}
function giveGoldStar(id)
{
	e = document.getElementById(id);
	
	if (e.id == "innergive1")
		document.getElementById("give2").style.display = 'block';
	if (e.id == "innergive2")
		document.getElementById("give3").style.display = 'block';
	if (e.id == "innergive3")
	{
		window.location = "results.html";
	}
}
function resetView()
{
	document.getElementById("give3").style.display = 'none';
	document.getElementById("give2").style.display = 'none';
	document.getElementById("give1").style.display = 'none';
	document.getElementById("tbl1").style.display = 'none';
}
function postJSON(id, num)
{
	document.getElementById("enabled").style.display = "none";
	document.getElementById("disabled").style.display = "block";
	if (num == 0)
	{
		var fn = document.getElementById("FName").value; 
		var ln = document.getElementById("LName").value; 
		var em = document.getElementById("Email").value; 
		var userData = '{"firstName":"'+fn+'","lastName":"'+ln+'","email":"'+em+'"}';
		$.ajax({
			type: "POST",
			url: "/api/user",
			data: userData,
			contentType: "application/json",
			dataType: "json",
			complete: function(data){
				document.getElementById("enabled").style.display = "block";
				document.getElementById("disabledf").style.display = "none";
			},
			success: function(data, textStatus, jqXHR){
				alert("Account creation successful!  Please log in to continue.");
				window.location = "index.html";
			},
			error: function(xhr, status, error) {
				alert("Error: " + error);
			}
		});		
	}
	else if (num == 1)
	{
		var e = document.getElementById("select1");
		var e1 = e.options[e.selectedIndex].value;
		e = document.getElementById("select2");
		var e2 = e.options[e.selectedIndex].value;
		var e3 = document.getElementById("select3").value;
		var userData = '{"description":"'+e3+'","category":"'+e2+'","issuer_id":"'+sessionStorage.userID+'","owner_id":"'+e1+'"}';
		$.ajax({
			type: "POST",
			url: "/api/star",
			data: userData,
			contentType: "application/json",
			dataType: "json",
			complete: function(data){
				 giveGoldStar("innergive3");}
			});
	}
}
function getJSON(num)
{
	if (num == 0)
	{
		$.getJSON('/api/user', function(jdata)
		{
			var i = 0
			for(i=0;i<jdata.objects.length;++i)
			{
				if (sessionStorage.userID == jdata.objects[i].id)
				{
					$('#jsondump').html('Hello '+jdata.objects[i].firstName+'!<br />');
					$('#jsondump').append('Is this not displaying your name? <a onclick="userLogout()" href="#">Click here to switch users</a>');
				}
				$('#select1').append('<option value="'+jdata.objects[i].id+'">'+jdata.objects[i].firstName+' '+jdata.objects[i].lastName+'</option>');
			}
		})
	}
	if (num == 1) //shouldnt be accessible now because the button disappears when the page loads.
	{
	}
}
function limitText(limitField, limitNum)
{
	e = document.getElementById(limitField);
	if (e.value.length > limitNum)
		e.value = e.value.substring(0, limitNum);
}
function showselect(id)
{
	var e = document.getElementById(id);
	alert(e.options[e.selectedIndex].value);
}







