cmd = .venv/bin/python ./run.py
rsync_dest = lutro.me:/var/www/lutro.me
rsync_args = -rvc -e ssh ./dist/ --delete-after --filter='P assets/*'


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
	rsync $(rsync_args) $(rsync_dest)

upload-dryrun: remote
	rsync --dry-run $(rsync_args) $(rsync_dest)

.PHONY: assets
