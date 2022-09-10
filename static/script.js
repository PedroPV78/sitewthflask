const button = document.querySelector("#aa")

button.addEventListener("click", () => {
	Notification.requestPermision().then(perm => {
		if (perm === "granted") {
			new Notification("aaa");
		}
	});
});
