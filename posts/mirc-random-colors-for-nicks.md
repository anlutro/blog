# mIRC - random colors for nicks
pubdate: 2012-06-25 12:00:00

STEP 1: Press ALT+R in mIRC, click the variables tab and paste the following:

	%colors 2 3 4 5 6 7 8 9 10 11 12 13 14 15
	%currentcolor 2

STEP 2: Click the remote tab and paste this:

	on ^*:text:*:#:{
	  if ($cnick($nick).color == $color(normal text)) { 
	    .cnick $nick $gettok(%colors,$calc(%currentcolor),32)
	    if (%currentcolor == $gettok(%colors,0,32)) { 
	      set %currentcolor 1
	    }
	    else {
	      inc %currentcolor
	    }
	  }
	}

If you only want nick colors to apply for people in certain channels, replace # with a list of channels separated by a comma. Example:

	on ^*:text:*:#raziel,#qlreddit:{
	  ...
	}
STEP 3: Press ALT+B in mIRC, click the nick colors tab and check "Enable nick colors"