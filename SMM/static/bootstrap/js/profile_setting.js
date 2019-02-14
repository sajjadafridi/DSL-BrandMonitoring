var index = 'profile_tab';
//  Define friendly data store name
var dataStore = window.sessionStorage;

function toogleProfileSettingsBar() {
	document.getElementById("profileSettingsBar").classList.toggle('active');
}

function myProfileTabClick() {
	document.getElementById("myProfileTab").style.color = "darkgreen";
	document.getElementById("myProfileArea").style.display = "block";
	document.getElementById("changePasswordTab").style.color = "darkgray";
	document.getElementById("changePasswordArea").style.display = "none";
	document.getElementById("deleteAccountTab").style.color = "darkgray";
	document.getElementById("deleteAccountArea").style.display = "none";

	dataStore.setItem(index, 'myProfileTabClick')
}

function changePasswordTabClick() {
	document.getElementById("changePasswordTab").style.color = "darkgreen";
	document.getElementById("changePasswordArea").style.display = "block";
	document.getElementById("myProfileTab").style.color = "darkgray";
	document.getElementById("myProfileArea").style.display = "none";
	document.getElementById("deleteAccountTab").style.color = "darkgray";
	document.getElementById("deleteAccountArea").style.display = "none";

	dataStore.setItem(index, 'changePasswordTabClick')
}

function deleteAccountTabClick() {
	document.getElementById("deleteAccountTab").style.color = "darkgreen";
	document.getElementById("deleteAccountArea").style.display = "block";
	document.getElementById("myProfileTab").style.color = "darkgray";
	document.getElementById("myProfileArea").style.display = "none";
	document.getElementById("changePasswordTab").style.color = "darkgray";
	document.getElementById("changePasswordArea").style.display = "none";
	dataStore.setItem(index, 'deleteAccountTabClick')
}

function loadImage() {
	var file = document.getElementById("id_profile_image").files[0];
	var reader = new FileReader();
	reader.onloadend = function () {
		document.getElementById('profileImagePlaceHolder').style.backgroundImage = "url(" + reader.result + ")";
	}
	if (file) {
		reader.readAsDataURL(file);
		$('#profileImagePlaceHolder').attr('src', '');
		$('#profileImagePlaceHolder').css("background-size", 200 + "px " + 200 + "px");

	} else {}
}


var modalConfirm = function (callback) {

	$("#deleteAccountbtn").on("click", function () {
		$("#mi-modal").modal('show');
	});

	$("#modal-btn-yes").on("click", function () {
		callback(true);
		$("#mi-modal").modal('hide');
	});

	$("#modal-btn-no").on("click", function () {
		callback(false);
		$("#mi-modal").modal('hide');
	});
};

modalConfirm(function (confirm) {
	if (confirm) {
		$("#result").html("Confirm");
	} else {
		//Acciones si el usuario no confirma
		$("#result").html("No Confirm");
	}
});
var oldIndex;
$(document).ready(function () {
	oldIndex = dataStore.getItem(index);
	if (oldIndex == null) {
		oldIndex = 'myProfileTabClick';
	}
	eval(oldIndex + "()");
});