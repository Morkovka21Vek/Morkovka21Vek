#!/bin/sh
picom&
flameshot&
xscreensaver -nosplash&
setxkbmap -layout us,ru -option grp:caps_toggle
#setxkbmap -option altwin:backspace
xmodmap -e "keysym Alt_R = BackSpace"
dunst&
