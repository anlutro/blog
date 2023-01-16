venv_path = .venv
gen_cmd = ${venv_path}/bin/russell generate
serve_cmd = ${venv_path}/bin/russell serve
ghp_cmd = ${venv_path}/bin/ghp-import
rsync_dest = lutro.me:/var/www/lutro.me
rsync_args = -rivc -e ssh ./dist/ --delete-after --filter='P assets/*'


default: local

${venv_path}:
	python -m venv ${venv_path}
	${venv_path}/bin/pip install --upgrade pip setuptools
	${venv_path}/bin/pip install -r requirements.txt -c constraints.txt

clean:
	rm -rf dist/*

assets:
	mkdir -p dist
	rsync -r assets/ dist/assets

local: ${venv_path} clean assets
	${gen_cmd} --root-url="//localhost:8000"

serve: ${venv_path}
	${serve_cmd}

remote: ${venv_path} clean assets
	${gen_cmd} --root-url="//www.lutro.me"

github-pages: ${venv_path} clean assets
	${gen_cmd} --root-url="//anlutro.github.io"
	${ghp_cmd} dist -m "auto-commit from command: make github-pages" --push

# when building in cloudflare, requirements/venv is managed by them
cloudflare-pages: clean assets
	russell generate --root-url="//lutrodotme.pages.dev"
	cp cloudflare-redirects dist/_redirects

upload: remote
	rsync ${rsync_args} ${rsync_dest}

upload-dryrun: remote
	rsync --dry-run ${rsync_args} ${rsync_dest}

.PHONY: assets
