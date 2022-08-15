git:
	git add .
	git commit -m "$m"
	git push

update:
	git pull
	sudo systemctl pythonflask restart
