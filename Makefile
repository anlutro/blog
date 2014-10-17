local:
	russell generate --title="Andreas' Blog" --url="file:///home/andreas/blog/russell/public"

remote:
	russell generate --title="Andreas' Blog" --url="http://www.lutro.me"

upload:
	rsync -rve ssh --perms --chmod=Dg+s,ug+w,Fo-w,+X ./public/ odin:/var/www/blog.lutro.priv.no
