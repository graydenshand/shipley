$( function() {
	$( "#datepicker" ).datepicker();
 });

document.getElementById("addTeamMember").style.visibility = "hidden";
document.getElementById("removeTeamMember").style.visibility = "hidden";
document.getElementById("addAssignment").style.display = "none";

function toggleAddTeamMemberForm() {
	if (document.getElementById("addTeamMember").style.visibility == "hidden") {
		document.getElementById("teamForms").style.display = "inline"
		document.getElementById("addTeamMember").style.visibility = "visible";
	} else if (document.getElementById("addTeamMember").style.visibility == "visible") {
		if (document.getElementById("removeTeamMember").style.visibility == "hidden") {
			document.getElementById("addTeamMember").style.visibility = "hidden";
			document.getElementById("teamForms").style.display = "none";
		} else if (document.getElementById("removeTeamMember").style.visibility == "visible") {
			document.getElementById("addTeamMember").style.visibility = "hidden"
		};
	};
};

function toggleRemoveTeamMemberForm() {
	if (document.getElementById("removeTeamMember").style.visibility == "hidden") {
		document.getElementById("teamForms").style.display = "inline"
		document.getElementById("removeTeamMember").style.visibility = "visible";
	} else if (document.getElementById("removeTeamMember").style.visibility == "visible") {
		if (document.getElementById("addTeamMember").style.visibility == "hidden") {
			document.getElementById("removeTeamMember").style.visibility = "hidden";
			document.getElementById("teamForms").style.display = "none";
		} else if (document.getElementById("addTeamMember").style.visibility == "visible") {
			document.getElementById("removeTeamMember").style.visibility = "hidden"
		};
	};
};

function toggleAddAssignment() {
	if (document.getElementById("addAssignment").style.display == "none") {
		document.getElementById("addAssignment").style.display = "inline";
	} else {
		document.getElementById("addAssignment").style.display = "none";
	};
};

function submitForm(id) {
	document.getElementById(id).submit();
}

document.getElementById('assignmentSelector').onchange = function() {
	submitForm('assignmentToggle');
}

