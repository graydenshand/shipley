function Clock() {
	this.get_time = function() {
		var now = new Date();
		var day = now.getDay();
		var date = now.getDate();
		var h = now.getHours();
		if (h === 0) {
			h = 12;
		}
		if (h > 12) {
			h -= 12
		}
		var m = now.getMinutes();
		var y = now.getFullYear();
		var mo = now.getMonth();
		

		var formatDay = function() {
			var weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
			day = weekdays[day]
			return day
		}

		var formatDate = function() {
			if (date == 1) {
				date += "st"
			}
			else if (date == 2) {
				date += "nd"
			}
			else if (date == 3) {
				date += "rd"
			}
			else {
				date += "th"
			}
			return date
		}

		var formatMonth = function() {
			var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'November', 'December']
			mo = months[mo]
			return mo
		}

		var formatMinutes = function() {
			if (m <= 9) {
				m = "0" + m
			}
			return m
		}
		

		document.getElementById('clock').innerHTML = h + ':' + formatMinutes();
		document.getElementById('date').innerHTML = formatDay() + ', ' + formatMonth() + ' ' + formatDate() ;
	};

	window.setInterval(this.get_time, 100);

};


var clock = new Clock;
