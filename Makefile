default: local serve

clean:
	rm -rf dist/*

dist/assets: assets
	mkdir -p dist
	cp -r assets/ dist/

local: clean dist/assets
	uv run russell generate --root-url="//localhost:8000"

remote: clean dist/assets
	uv run russell generate --root-url="//www.lutro.me"

cloudflare-pages:
	pipx install uv
	$(MAKE) remote
	cp cloudflare-redirects dist/_redirects

serve:
	uv run russell serve
