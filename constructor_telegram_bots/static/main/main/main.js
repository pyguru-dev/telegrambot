var intervalId;
var check = 0;

intervalId = setInterval(
	function() {
		check += 1;

		const screenWidth = window.screen.width;
		const containerSiteUsersElementHeight = document.querySelector('.container#siteUsers').clientHeight + 4;
		var containerSiteUsersElementTop;

		if (userAuth) {
			if (screenWidth >= 320 && screenWidth < 768) {
				containerSiteUsersElementTop = 235;
			}
		} else {
			if (screenWidth >= 320 && screenWidth < 768) {
				containerSiteUsersElementTop = 185;
			}
		}
		if (screenWidth >= 768 && screenWidth < 1000) {
			containerSiteUsersElementTop = 99;
		}
		if (screenWidth >= 1000) {
			containerSiteUsersElementTop = 124;
		}

		var totalTopForcontainerSiteInfoElement = containerSiteUsersElementTop + containerSiteUsersElementHeight;

		if (screenWidth >= 320 && screenWidth < 768) {
			totalTopForcontainerSiteInfoElement += 15;
		}
		if (screenWidth >= 768 && screenWidth < 1000) {
			totalTopForcontainerSiteInfoElement += 20;
		}
		if (screenWidth >= 1000) {
			totalTopForcontainerSiteInfoElement += 25;
		}

		var containerSiteInfoElement = document.querySelector('.container#siteInfo');
		containerSiteInfoElement.style = 'top: ' + totalTopForcontainerSiteInfoElement + 'px;';

		if (check >= 5) {
			clearInterval(intervalId);
		}
	}, 100
)