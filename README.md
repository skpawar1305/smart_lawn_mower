# smart_lawn_mower

This is a Systems Engineering and Embedded Systems Project.
This repository will have all the documents I prepared and the working codes for ESP32 running on Micropython (WebServer) and Arduino

The Mower is just a prototype and not an actual grass cutting mower having randowm motion, but capable of avoiding obstacles and staying within the Boundary area.

Requirements document is prepared referring Volere Template.
Various SysUML diagrams are included.

Mower can be scheduled using any Web Browser and will reach back to its home position (charging station) once it reaches its stop time or the battery is low.
WebServer has Current clock time of Germany and it also shows the current weather status of the set location through openweathermap API.

It also sends notification to the phone when it's picked up in running condition to PushBullet app through WebHooks API.
