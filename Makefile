run_cmd = .venv/bin/python ./run.py
serve_cmd = .venv/bin/python ./serve.py
rsync_dest = lutro.me:/var/www/lutro.me
rsync_args = -rvc -e ssh ./dist/ --delete-after --filter='P assets/*'


default: local

clean:
	rm -rf dist/*

assets:
	rsync -r assets/ dist/assets

local: clean assets
	$(run_cmd) --root-url="//localhost:8000"

serve:
	$(serve_cmd)

remote: clean assets
	$(run_cmd) --root-url="//www.lutro.me"

upload: remote
	rsync $(rsync_args) $(rsync_dest)

upload-dryrun: remote
	rsync --dry-run $(rsync_args) $(rsync_dest)

.PHONY: assets
