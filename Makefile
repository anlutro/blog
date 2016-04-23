cmd = ./run.py

clean:
	rm -rf dist/*

css:
	mkdir -p dist/assets
	sassc sass/main.sass > dist/assets/style.css

local:
	$(cmd) --root-url="file:///$$PWD/dist"

remote:
	$(cmd) --root-url="//www.lutro.me"

upload: css remote
	rsync -rvc -e ssh ./dist/ lutro.me:/var/www/lutro.me \
		--delete-after --filter='P assets/*'
