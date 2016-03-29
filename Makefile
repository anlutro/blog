cmd = ./run.py

css:
	mkdir -p dist/assets
	sassc sass/main.sass > dist/assets/style.css

local:
	$(cmd) --root-url="file:///$$PWD/dist"

remote:
	$(cmd) --root-url="//www.lutro.me"

upload: css remote
	rsync -rvce ssh ./dist/ lutro.me:/var/www/lutro.me
