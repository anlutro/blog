# Volume in Debian distros (Crunchbang, Ubuntu...)
pubdate: 2013-08-20 12:00:00

I've had this problem with my old Lenovo ThinkPad with every Linux installation. When I installed CrunchBang (a great disto, by the way) I had it again and had forgotten how to fix it. Amazingly, by googling around I found **my own old blog with a post on how to fix it** from all the way back to Ubuntu 9.10. I decided to re-write it a bit and host it here.

With virtually every Debian distribution I've used, my ThinkPad R61 (6 years old and still going strong) has had sound issues. The volume controls have been extremely uneven, there's been lots of distorted sound with anything over 15% etc. Trying to find the solution to this, I opened the command-line sound mixer that Debian distributions use:

	alsamixer

Here, it's possible to tell exactly what is happening to your system volumes and you can more easily identify what is causing the problems. You may have to select a different sound card (press F6) to see all the details. In my case, I've had several different problems and solutions over the years - in one of the early Ubuntu distros I had to lock PCM at 47% (0dB gain), and nowadays I just make sure to lock Master at 95%. This will vary from computer to computer, so mess around but try to figure out which one you need to lock.

By default, the ALSA mixer will try to "merge" a bunch of these channels when you try to control volume. This means it will first try to increase one channel, then another, then a third until everything is max. This is not always what you want. Open the following file in your favorite text editor with sudo - I use nano:

	sudo nano /usr/share/pulseaudio/alsa-mixer/paths/analog-output.conf.common

In the file, look for something like this:

	[Element Master]
	switch = mute
	volume = merge

	[Element PCM]
	switch = mute
	volume = merge

The documentation in the same file tells you that “merge” means “merge it into the device volume slider”. This is what you want to change. By now you should know which channel you want to lock - for this channel, change "merge" to "ignore". Now, open alsamixer again and adjust the ignored channels volume until you feel your normal volume controls work fine.

Done!