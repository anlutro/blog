gen_cmd = .venv/bin/russell generate
serve_cmd = .venv/bin/russell serve
rsync_dest = lutro.me:/var/www/lutro.me
rsync_args = -rivc -e ssh ./dist/ --delete-after --filter='P assets/*'


default: local

clean:
	rm -rf dist/*

assets:
	mkdir -p dist
	rsync -r assets/ dist/assets

local: clean assets
	$(gen_cmd) --root-url="//localhost:8000"

serve:
	$(serve_cmd)

remote: clean assets
	$(gen_cmd) --root-url="//www.lutro.me"

upload: remote
	rsync $(rsync_args) $(rsync_dest)

upload-dryrun: remote
	rsync --dry-run $(rsync_args) $(rsync_dest)

.PHONY: assets
