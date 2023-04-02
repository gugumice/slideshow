# slideshow
Art project#2
I found a solution.

Note that Ilitek touchscreen detects as two input device, so you must set "MatchIsTouchscreen" option.
This will rotate touchscreen to 90 degrees.
Code: Select all

/usr/share/X11/xorg.conf.d/90-rotate-touch.conf

Section "InputClass"
Identifier "ILITEK ILITEK-TP"
MatchProduct "ILITEK ILITEK-TP"
MatchIsTouchscreen "on"
Option "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"
EndSection
