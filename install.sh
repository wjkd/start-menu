#!/bin/sh
if [ $1 = "dockbarx" ]; then
	cp startmenu.png /usr/share/dockbarx/applets/
	cp startmenu-active.png /usr/share/dockbarx/applets/
	cp startmenu.applet /usr/share/dockbarx/applets/
	cp startmenu.py /usr/share/dockbarx/applets/
fi
cp startmenu /usr/local/bin/
cp startmenuctl /usr/local/bin/
