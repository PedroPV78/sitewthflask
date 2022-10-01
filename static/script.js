const button = document.querySelector("#aa")

button.addEventListener("click", () => {
	Notification.requestPermission().then(perm => {
		if (perm === "granted") {
			new Notification("aaa");
		}
	});
});
