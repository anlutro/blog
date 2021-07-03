gen_cmd = .venv/bin/russell generate
serve_cmd = .venv/bin/russell serve
ghp_cmd = .venv/bin/ghp-import
rsync_dest = lutro.me:/var/www/lutro.me
rsync_args = -rivc -e ssh ./dist/ --delete-after --filter='P assets/*'


default: local

clean:
	rm -rf dist/*

assets:
	mkdir -p dist
	rsync -r assets/ dist/assets

local: clean assets
	${gen_cmd} --root-url="//localhost:8000"

serve:
	${serve_cmd}

remote: clean assets
	${gen_cmd} --root-url="//www.lutro.me"

github-pages:
	${gen_cmd} --root-url="//anlutro.github.io"
	${ghp_cmd} -m "auto-commit from command: make ghp-import" dist

upload: remote
	rsync ${rsync_args} ${rsync_dest}

upload-dryrun: remote
	rsync --dry-run ${rsync_args} ${rsync_dest}

.PHONY: assets
