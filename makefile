git:
	git add .
	git commit -m "$m"
	git push

update:
	git fetch
	git pull
	sudo systemctl restart nginx
	sudo supervisorctl reload
