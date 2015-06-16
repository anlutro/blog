local:
	russell generate --title="Andreas' Blog" --url="file:///home/andreas/documents/blog/public"

remote:
	russell generate --title="Andreas' Blog" --url="http://www.lutro.me"

upload:
	rsync -rvce ssh --perms --chmod=Dg+s,ug+w,Fo-w,+X ./public/ lutro.me:/var/www/lutro.me
