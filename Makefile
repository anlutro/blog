cmd = ./run.py

default: local css

clean:
	rm -rf dist/*

css:
	mkdir -p dist/assets
	sassc sass/main.sass > dist/assets/style.css

local: clean css
	$(cmd) --root-url="file:///$$PWD/dist"

remote: clean css
	$(cmd) --root-url="//www.lutro.me"

upload: remote
	rsync -rvc -e ssh ./dist/ lutro.me:/var/www/lutro.me \
		--delete-after --filter='P assets/*'
