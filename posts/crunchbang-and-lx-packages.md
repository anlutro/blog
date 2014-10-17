# Crunchbang and lx* packages

I've been running Crunchbang as my main linux distribution for a while now, and have had a really good time with it. Recently I stumbled upon a problem, and thought I'd just put my solution out there.

I installed a package named lxinput, which is used to configure mouse speed/acceleration as well as some other input settings. lxinput is part of the LXCD desktop environment, but works and looks great on crunchbang's openbox. lxinput needs lxsession to work, and unfortunately, lxsession seems to put itself as the default session manager, overwriting openbox. The result was, for me, that after logging in, nothing would happen.

What you need to do is simply reset the session manager to openbox. To do this, we first log in to the linux terminal instead of via the desktop environment. Press ctrl+alt+F1 to get to the TTY, then enter your regular credentials. Enter the command `sudo update-alternatives --config x-session-manager`. You'll get a list of available session managers, lxsession will be selected - enter the number that corresponds to openbox, confirm, and reboot. Things should now work as before.