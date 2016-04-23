# mIRC - retake nick automatically
pubdate: 2012-06-25 12:00:00 +0100
tags: mIRC
public: false

Retake nick automatically

This script was written for a guy who kept disconnecting from IRC and hated having to manually change back to his main nick when his old user finally got dropped from the server.

	raw 433:*:{
	  if ($2 == $mnick) {
	    .notify on
	    .notify $mnick
	  }
	}
	on *:unotify:{
	  if ($nick == $mnick) {
	    .notify -r $mnick
	    .timer.cn 1 1 nick $mnick
	  }
	}