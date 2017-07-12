cmd = .venv/bin/python ./run.py


default: local

clean:
	rm -rf dist/*

assets:
	rsync -r assets/ dist/assets

local: clean assets
	$(cmd) --root-url="file:///$$PWD/dist"

remote: clean assets
	$(cmd) --root-url="//www.lutro.me"

upload: remote
	rsync -rvc -e ssh ./dist/ lutro.me:/var/www/lutro.me \
		--delete-after --filter='P assets/*'

.PHONY: assets
