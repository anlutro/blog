cmd = russell generate

css:
	sassc sass/main.sass > dist/assets/style.css

local:
	$(cmd) --url="file:///home/andreas/documents/blog/dist"

remote:
	$(cmd) --url="http://www.lutro.me"

upload:
	rsync -rvce ssh ./dist/ lutro.me:/var/www/lutro.me
