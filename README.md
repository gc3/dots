# dots

Learning python with a personal project to implement a simple game on my mac

## Playing
Just click on dots. If they are the same color and next to each other, you can submit your move and get points. You're done when you run out of move.


## Requirements
- python 3
- wx python UI library ([www](https://www.wxpython.org/), [github](https://github.com/wxWidgets/Phoenix/))

## Run on MacOS
Using [py2app](https://py2app.readthedocs.io/en/latest/index.html), you can run the following command in your code checkout to produce a dots.app/ that MacOS can run as what appears to be a native app.

    python3.10 setup.py py2app --iconfile images/dots.ico -O2
