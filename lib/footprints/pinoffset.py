#!/usr/bin/env python

def pingen(dx, dy, startx=0, starty=0):
    x,y = 0, 0
    while 1:
        yield (x+startx, y+starty)
        x, y = x+dx, y+dy

g = pingen(0, 7874, 4700, 30400)
a = [ g.next() for i in range(10)]
g = pingen(0, 7874, 91300, 30400)
b = [ g.next() for i in range(10)]
b.reverse()
pinlist = a + b

c = 1
fmt = 'Pin [%i %i %i %i %i %i "%s" "%i" "%s"]'
thickness = 6000
clearance = 1000
mask = 500
drill = 3200
sflags = []
for i in pinlist:
    rx, ry = i[0], i[1]
    if c==1: sf=["square"]
    else: sf=sflags
    print fmt % (rx, ry, thickness, clearance, mask, drill, c, c, ','.join(sf))
    c += 1
