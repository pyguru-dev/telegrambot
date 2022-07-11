function sendRequestToServer(request, link, data, func) {
	request.open('POST', link, true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = func;
	request.send(data);
}