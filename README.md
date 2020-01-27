# Porn_Matrix
This is a Python 3 server application for viewing porn streams in a grid on your browser. It loads videos based on provided search parameters. If no search terms are provided, it chooses from a list of my favorite porn stars. :)

It is a Flask python app with a vanilla JavaScript frontend. I craft a bing video search string and scrape the results for video links, then pass them into youtube_dl to get a direct link to the video file, which is sent to the browser frontend and loaded into a video container.

[donate if you enjoy my work :)](https://paypal.me/deracoslon)

![Sample image](https://i.imgur.com/n3HoJpk.png)

# Run / Build

[I use Windows and I just want an exe](https://github.com/pornmatrix/Porn_Matrix/releases)

Intall prereqs

> pip install -r requirements.txt

Keep up to date, particularly for youtube_dl

> pip install -r requirements.txt --update

If you have issues installing cx_freeze on python 3.7, try this - thanks Slurgie from the bodybuilding.com forums

> pip install --upgrade git+https://github.com/anthony-tuininga/cx_Freeze.git@master

Run it, it will automatically open a browser window

> python porn_matrix.py

Change port

> python porn_matrix.py 8080

Build to build folder, run exe - works the same as above

> python build_to_exe.py build

Run exe from build folder and change port

> porn_matrix.exe 8080

# Hotkeys:
```
F11 = fullscreen

m = toggle mute
h = toggle help
c = toggle controls
+/- = adjust volume 5%

left arrow = go back 30s
right arrow = go forward 30s
down arrow = move to beginning
up arrow = move to end
p or pause = toggle pause/play

enter = toggle search
r = load search results for all videos
1-9 = load search results in one
```

# Bonus Features:
- Multiple monitor support,
control windows simultaneously with the broadcast api
- Phone support, just go to the server url