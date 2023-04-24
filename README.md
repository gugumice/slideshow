# slideshow
Art project#2
Slide viewer using pygame.
usage: PyGame image kiosk [-h] [-v] [-r x,y] [-i mins] [-d secs] filename
-v makes buttons visible and displays grid on top of picture
-r displays slides in custom screen resolution
-i Time (mins) slideshow returns to first pict
-d debounce time (secs) screen buttons are blocked after action. This prevents touchscreen from scrolling too fast.

json playlist format
button name can be any but it should be unique within slide
{
    "current_picture.jpg": [
        {
            "button_name": {
                "xpos": 10,
                "ypos": 10,
                "width": 1900,
                "height": 1080,
                "pict": "picture_to_show.jpg"
             }
        }
    ]
}
