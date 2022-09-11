function signOut(nickname) {
	var signOutAnswer = confirm("Вы точно хотите выйти из аккаунта?");
	if (signOutAnswer == true) {
		window.location.href = '/account/sign_out/' + nickname + '/';
	}
}