git:
	git add .
	git commit -m "$m"
	git push

update:
	git pull
	sudo python3 main.py
