{
	let num = 0;

	function checkRequestResponse(func) {
		return function() {
			num ++;

			if (num > 2) {
				num = 0;

				return func();
			}
		}
	}
}
