//------SETUP FOR AJAX----------------------------------------------------------
//------------------------------------------------------------------------------
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

$(document).ready(function() {
	function shakeForm() {
		$("#password").css("border", "1px solid #d62929");
   		$("#password").effect("shake");
	}

	// login/register toggle
	$('#loginlink').click(function(e) {
    	$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#registerlink').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#registerlink').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#loginlink').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

	//register user
	$("#register-submit").click(function() {
		var username = $("#user").val();
		var email = $("#email").val();
		var phone = $("#phone").val();
		var pass = $("#pass").val();
		var passCheck = $("#confirm-password").val();

		if (pass != passCheck) {
			$("#confirm-password").css("border", "1px solid #d62929");
			$("#confirm-password").effect("shake");
		}
		else {
			$.ajax({
				type: "POST",
				url: "/register",
				datatype: "json",
				data: {
					"username": username,
					"pass": pass,
					"email": email,
					"phone": phone
				},
				success: function(response) {
					document.write(response);
					window.location.reload(true);
				},
				error: function(response) {
					console.log(response.responseText);
				}
			});
		}
	});

	$("#login-submit").click(function() {
		var username = $("#username").val();
		var pass = $("#password").val();

		$.ajax({
			type: "POST",
			url: "/login",
			datatype: "json",
			data: {
				"username": username,
				"pass": pass
			},
			success: function(response) {
				if (response == "didnt work") shakeForm();
				else { 
					document.write(response);
					window.location.reload(true);
				}
			},
			error: function(response) {
				console.log(response.responseText);
			}
		});
	});

	$("#logout").click(function() {
		$.ajax({
			type: "POST",
			url: "/logout",
			success: function(response) { 
				document.write(response);
				window.location.reload(true);
			},
			error: function(response) {
				console.log(response.responseText);
			}
		});
	});

	$("#artistFill").keyup(function() {
		$("#artistList").empty();
		var name = $("#artistFill").val();
		$.ajax({
			type: "POST",
			datatype: "json",
			url: "/artistLoad",
			data: {"name": name},
			success: function(response) {
                var name1 = response.list[0];
                var name2 = response.list[1];
                var name3 = response.list[2];
                var name4 = response.list[3];
                var name5 = response.list[4];
                var name6 = response.list[5];
                var name7 = response.list[6];
                var name8 = response.list[7];
                var name9 = response.list[8];
                var name10 = response.list[9];
          
                $("#artistList").append("<option id=1>")
                $("#artistList").append("<option id=2>")
                $("#artistList").append("<option id=3>")
                $("#artistList").append("<option id=4>")
                $("#artistList").append("<option id=5>")
                $("#artistList").append("<option id=6>")
                $("#artistList").append("<option id=7>")
                $("#artistList").append("<option id=8>")
                $("#artistList").append("<option id=9>")
                $("#artistList").append("<option id=10>")

                $("#1").val(name1);
                $("#2").val(name2);
                $("#3").val(name3);
                $("#4").val(name4);
                $("#5").val(name5);
                $("#6").val(name6);
                $("#7").val(name7);
                $("#8").val(name8);
                $("#9").val(name9);
                $("#10").val(name10);
			},
			error: function(response) {
				console.log(response.responseText);
			}
		});
	});

	$("#addButt").click(function() {
		var artistName = $("#artistFill").val();
		$.ajax({
			type: "POST",
			url: "/addArtist",
			datatype: "JSON",
			data: {"artistName": artistName},
			success: function(response) {
				console.log(response);
			},
			error: function(response) {
				console.log(response.responseText);
			}
		});
	});

});
























