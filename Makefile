src = .
target = dist
title = "Andreas' Blog"
cmd = russell generate $(src) $(target) --title=$(title)

local:
	$(cmd) --url="file:///home/andreas/documents/blog/public"

remote:
	$(cmd) --url="http://www.lutro.me"

upload:
	rsync -rvce ssh ./public/ lutro.me:/var/www/lutro.me
