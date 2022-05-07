function signOut() {
	var sign_out = confirm("Вы точно хотите выйти из аккаунта?");
	if (sign_out == true) {
		window.location.href = '/account/sign_out/';
	}
}