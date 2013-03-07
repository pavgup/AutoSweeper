#-------------------------------------------------------------------------------
# Name:        Auto Sweeper
# Purpose:     Frustration reduction.  Minesweeper zen.
#
# Author:      Pavan Gupta
#
# Created:     06/03/2013
# Copyright (c) 2013 Pavan Gupta (pg8p@virginia.edu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-------------------------------------------------------------------------------

"""
The bounding box takes the top left and bottom right coordinates of the
minesweeper window to bound the screen shot.  Remember, this looks for the
the minesweeper window to be as small as in size as possible in expert
mode and to be located flush against the top left part of your screen.
"""

import ImageGrab
import os
import time
import win32api
import win32con
import random

# Important Globals
mines = [[-1 for x in xrange(16)] for x in xrange(30)] # tile definitions
mwid = 18 # width of tile in pixels
mhgt = 18 # height of tiles in pixels
thlf = 9 # convenient half heigh/width of tile (code should read easily!)
wypad = 0 # distance of window from top of screen
wxpad = 0 # distance of window from left of screen
ypad = wypad+80 # pixels from top of window to first tile boundary
xpad = wxpad+38 # pixels from left of window to first tile boundary
refTiles = [[(-1,-1,-1) for x in xrange(16)] for x in xrange(30)] # ref tile colors
numGames = 5

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    # print("Left Clicked")

def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(.1)
    # print("Right Clicked")

def midClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,0,0)
    # print("Mid Clicked")

def moveMouse(x,y):
    win32api.SetCursorPos((x,y))
    #print("Moved Mouse to (" + str(x) + "," + str(y) + ")")


def grabRefTileColors():
    boundingBox = (wxpad+0,wypad+0,wxpad+616,wypad+409);
    mineWin = ImageGrab.grab(boundingBox)
    print("Grabbing minesweeper ref definitions...")
    for x in xrange(30):
        for y in xrange(16):
            moveMouse(xpad+thlf+mwid*x,ypad+thlf+mwid*y) # move mouse to top left tile (for looks)
            refTiles[x][y] = mineWin.getpixel((xpad+thlf+mwid*x,ypad+thlf+mwid*y))

def grabMinesweeperWindow():
    moveMouse(xpad+thlf,ypad+thlf) # move mouse to first tile position
    time.sleep(.1)
    boundingBox = (wxpad+0,wypad+0,wxpad+616,wypad+409);
    mineWin = ImageGrab.grab(boundingBox)
    # mineWin.save('D:\data\Dropbox\AutoSweeper\\mine' + str(int(time.time())) + '.png','PNG')

    print("Grabbing minesweeper tile definitions...")
    for x in xrange(30):
        for y in xrange(16):
            mines[x][y] = returnTileDefinition(mineWin,x,y)
            moveMouse(xpad+thlf+mwid*x,ypad+thlf+mwid*y) # move mouse to top left tile (for looks)

    return mineWin

def returnTileDefinition(mineWin,x,y):

    if(mineWin.getpixel((xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((3+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((2+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((-3+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((2+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((xpad+thlf+mwid*x,-3+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((1+3+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((1+1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((1+2+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((1+-3+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((1+2+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,-3+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((3+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((2+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((-3+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((2+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((xpad+thlf+mwid*x,-3+1+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((-1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((-1+3+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((-1+1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((-1+2+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((-1+-3+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((-1+2+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,-3+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((3+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((2+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((-3+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((2+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((xpad+thlf+mwid*x,-3+-1+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((1+3+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((1+1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((1+2+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((1+-3+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((1+2+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,-3+1+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((-1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((-1+3+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((-1+1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((-1+2+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((-1+-3+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((-1+2+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,1+ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,-3+1+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((1+3+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((1+1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((1+2+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((1+-3+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((1+2+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((1+xpad+thlf+mwid*x,-3+-1+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9


    if(mineWin.getpixel((-1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (64, 80, 190)):
        print "Found a 1"
        return 1
    elif(mineWin.getpixel((-1+3+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (28,106,0)):
        print "Found a 2"
        return 2
    elif(mineWin.getpixel((-1+1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (172, 6, 8)):
        print "Found a 3"
        return 3
    elif(mineWin.getpixel((-1+2+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (0, 0, 132)):
        print "Found a 4"
        return 4
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (125, 1, 0)):
        print "Found a 5"
        return 5
    elif(mineWin.getpixel((-1+-3+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (3, 124, 124)):
        print "Found a 6"
        return 6
    elif(mineWin.getpixel((-1+2+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (170, 5, 8)):
        print "Found a 7"
        return 7
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,-1+ypad+thlf+mwid*y)) == (163, 6, 4)):
        print "Found a 8"
        return 8
    elif(mineWin.getpixel((-1+xpad+thlf+mwid*x,-3+-1+ypad+thlf+mwid*y)) == (253, 1, 0)):
        print "Found a flag"
        return 9

    elif(mineWin.getpixel((xpad+thlf+mwid*x,ypad+thlf+mwid*y)) == (247, 251, 253)):
        print "WHOA WHOA WHOA, FOUND A QUESTION MARK!?"
        exit()


    elif(mineWin.getpixel((xpad+thlf+mwid*x,ypad+thlf+mwid*y)) != refTiles[x][y]):
        print "Found an empty box"
        return 10


    else:
        #print "Found something I didn't understand..."
        return -1


def valsAroundTile(x,y,val):
    totalFlags = 0;

    if(x+1 < 30):
        if(mines[x+1][y] == val):
            totalFlags += 1

    if(y+1 < 16):
        if(mines[x][y+1] == val):
            totalFlags += 1

    if(y+1 < 16 and x+1 < 30):
        if(mines[x+1][y+1] == val):
            totalFlags += 1

    if(x-1 >= 0):
        if(mines[x-1][y] == val):
            totalFlags += 1
        if(y+1 < 16):
            if(mines[x-1][y+1] == val):
                totalFlags += 1

    if(y-1 >= 0):
        if(mines[x][y-1] == val):
            totalFlags += 1
        if(x+1 < 30):
            if(mines[x+1][y-1] == val):
                totalFlags += 1

    if(y-1 >= 0 and x-1 >=0):
        if(mines[x-1][y-1] == val):
            totalFlags += 1

    return totalFlags

def flagUnknowns(x,y):
    if(x+1 < 30):
        if(mines[x+1][y] == -1):
            moveMouse(xpad+thlf+mwid*(x+1),ypad+thlf+mwid*y)
            rightClick()
            mines[x+1][y] = 9

    if(y+1 < 16):
        if(mines[x][y+1] == -1):
            moveMouse(xpad+thlf+mwid*x,ypad+thlf+mwid*(y+1))
            rightClick()
            mines[x][y+1] = 9

    if(y+1 < 16 and x+1 < 30):
        if(mines[x+1][y+1] == -1):
            moveMouse(xpad+thlf+mwid*(x+1),ypad+thlf+mwid*(y+1))
            rightClick()
            mines[x+1][y+1] = 9

    if(x-1 >= 0):
        if(mines[x-1][y] == -1):
            moveMouse(xpad+thlf+mwid*(x-1),ypad+thlf+mwid*y)
            rightClick()
            mines[x-1][y] = 9
        if(y+1 < 16):
            if(mines[x-1][y+1] == -1):
                moveMouse(xpad+thlf+mwid*(x-1),ypad+thlf+mwid*(y+1))
                rightClick()
                mines[x-1][y+1] = 9

    if(y-1 >= 0):
        if(mines[x][y-1] == -1):
            moveMouse(xpad+thlf+mwid*x,ypad+thlf+mwid*(y-1))
            rightClick()
            mines[x][y-1] = 9
        if(x+1 < 30):
            if(mines[x+1][y-1] == -1):
                moveMouse(xpad+thlf+mwid*(x+1),ypad+thlf+mwid*(y-1))
                rightClick()
                mines[x+1][y-1] = 9

    if(y-1 >= 0 and x-1 >=0):
        if(mines[x-1][y-1] == -1):
            moveMouse(xpad+thlf+mwid*(x-1),ypad+thlf+mwid*(y-1))
            rightClick()
            mines[x-1][y-1] = 9

def guessPick():
    randFinished = 1
    while(randFinished == 1):
        x = random.randrange(0,30)
        y = random.randrange(0,15)
        if(mines[x][y] == -1):
            randFinished = 0
            moveMouse(xpad+thlf+mwid*x,ypad+thlf+mwid*y)
            leftClick()
            time.sleep(.1)
            leftClick()
            time.sleep(.1)
            boundingBox = (wxpad+0,wypad+0,wxpad+616,wypad+409);
            mineWin = ImageGrab.grab(boundingBox)
            if(mineWin.getpixel((400,200)) == (240, 240, 240)):
                print "Bad news. We lost."
                moveMouse(442,288)
                leftClick()

    return 1

def startSweeping():
    global numGames
    #grabRefTileColors() # empty tiles are easy to find when checking refs
    moveMouse(xpad+thlf,ypad+thlf) # move mouse to first tile position
    leftClick() # to select the window
    leftClick() # to start with the first mine
    grabMinesweeperWindow() # initialize mine array with data from first click

    # Now lets start clearing the minefield!
    for l in xrange(20):
        for x in xrange(30):
            for y in xrange(16):
                if(mines[x][y] != -1 and mines[x][y] < 9):
                    moveMouse(xpad+thlf+mwid*x,ypad+thlf+mwid*y)
                    numFlag = valsAroundTile(x,y,9)
                    numUnknownTiles = valsAroundTile(x,y,-1)
                    if numFlag < mines[x][y]:
                        if(mines[x][y]-numFlag == numUnknownTiles):
                            print "I have the same set of mines and unknonws.."
                            print "I need "+str(mines[x][y])+" mines"
                            print "I have "+str(numFlag)+" flags"
                            print "I have "+str(numUnknownTiles)+" unknown tiles"
                            flagUnknowns(x,y)
                            #time.sleep(.1)
                            grabMinesweeperWindow()
                        else:
                            print "I dont know what to do"
                    else:
                        print "I HAVE A TILE SATISFIED!"
                        if(numUnknownTiles > 0):
                            midClick()
                            time.sleep(.1)
                            grabMinesweeperWindow()



    if(guessPick() == 1):
        startSweeping()
    elif(numGames > -5000):
        numGames = numGames - 1
        startNewGame()



def startNewGame():
    moveMouse(30,41)
    leftClick()
    moveMouse(68,63)
    leftClick()
    moveMouse(148,166)
    time.sleep(.5)
    leftClick()
    time.sleep(1)
    startSweeping()


def main():
    #startSweeping()
    #grabMinesweeperWindow()
    pass

if __name__ == '__main__':
    main()
