#!/bin/bash

WM_DESKTOP=$(xdotool getwindowfocus)

if [ $WM_DESKTOP == "2097251" ]; then

	echo "i3"

elif [ $WM_DESKTOP != "1883" ]; then

	WM_CLASS=$(xprop -id $(xdotool getactivewindow) WM_CLASS | awk 'NF {print $NF}' | sed 's/"/ /g')
	WM_NAME=$(xprop -id $(xdotool getactivewindow) WM_NAME | cut -d '=' -f 2 | awk -F\" '{ print $2 }')

	if [ $WM_CLASS == 'Code' ]; then

		echo "%{F#000000}Visual Studio Code%{u-}"

    elif [ $WM_CLASS == 'Google-chrome' ]; then

		echo "%{F#000000}Google Chrome%{u-}"

    elif [ $WM_CLASS == 'discord' ]; then

		echo "%{F#000000}Discord%{u-}"

	else

		echo "%{F#000000}$WM_NAME%{u-}"

	fi

fi