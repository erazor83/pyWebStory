pyWebStory
==========

pyWebStory - interactive fiction in python with WebSockets


What it is?
----------
Well, in general this is just a little engine for telling interactive fiction with python. It's not just like reading a book but even more like a simple text-adventure where you can take things, talk to people and somehow influence the plot.

pyWebStory uses HTML5 Websockets and forks a thread for every active user, who'll get it's own runtime objects at the server so it's not just like calling CGI-scripts and store temporary data. The system itself nearly behaves like a desktop application but is meant to run as a server for multiple users.


Why?
----------
So yeah, I played some [RAGS](www.ragsgame.com) games in the past and really liked them. Major issue seems to be the huge size, loading times (for example some games were about hundreds of megabytes and loading and saving took minutes) and even save and load with different game-versions was problematic.

My idea was to combine the flexibility of HTML/JavaScript and Python.


Current state?
----------
I think the communication-basics are in. Websockets, JSON and all this javascript - python communicaton seems to work. You can load and save games. There is a quickload-option. And even some text-tellings are working.

The major work has to be done with:
  * improve and implement the UI (yeah, the current javascript is pretty ugly and badly copy/pasted)
  * implement a cool text-telling engine (currently I'm using MAKO-templates which is fine but not very usefull)
  * add new features like items and so on
  * body description engine to tell how you look


What you need...
----------
  * python 2.7.x
  * simplejson
  * pycherry
  * ws4py
  * pyyaml
  * my version of erazor83/lamegame_cherrypy_authority



For lamegame_cherrypy_authority:
```
cd pyWebStory
git clone https://github.com/erazor83/lamegame_cherrypy_authority
```
How to run...
----------
```
./run.py
```
Fire up your webserver and got to something like http://localhost:8088 .

