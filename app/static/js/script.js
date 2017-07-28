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
		var pass = $("#pass").val();
		var passCheck = $("#confirm-password").val();

		if (pass != passCheck) {
			console.log("not equal!");
		}
		else {
			$.ajax({
				type: 'POST',
				url: '/register',
				datatype: 'json',
				data: {
					'username': username,
					'pass': pass,
					'email': email
				},
				success: function(response) {
					document.write(response);
				},
				error: function() {
					console.log("didn't work");
				}
			});
		}
	});

	$("#login-submit").click(function() {
		var username = $("#username").val();
		var pass = $("#password").val();

		$.ajax({
			type: 'POST',
			url: '/login',
			datatype: 'json',
			data: {
				'username': username,
				'pass': pass
			},
			success: function(response) {
				console.log(response);
				if (response == "didnt work") shakeForm();
			},
			error: function() {
				console.log("ajax error");
			}
		});
	})

});
