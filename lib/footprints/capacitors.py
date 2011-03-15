#!/usr/bin/env python

def cap(dia, spacing, polar, pindia):
    r = dia/2
    x = spacing/2
    thickness = pindia*5/3
    clearance = 1000
    print 'Element["" "" "C?" "" 0 0 %i %i 0 100 ""]' % (dia/3, dia/3)
    print '('
    
    print '\tElementArc [0 0 %i %i 0 360 700]' % (r, r)
    print '\tPin [%i 0 %i %i %i %i "1" "1" "square"]' \
          % (-x, thickness, clearance, thickness+clearance/2, pindia*11/10)
    print '\tPin [%i 0 %i %i %i %i "2" "2" ""]' \
          % (x, thickness, clearance, thickness+clearance/2, pindia*11/10)
    if polar:
        b = -x
        l = 1000
        print '\tElementLine[%i %i %i %i 700]' % (b-l, b, b+l, b)
        print '\tElementLine[%i %i %i %i 700]' % (b, b-l, b, b+l)
        print '\tElementLine[%i %i %i %i 700]' % (-b-l, b, -b+l, b)
    
    print ')'


if __name__ == '__main__':
    cap(dia=19600, spacing=7874, polar=True, pindia=3000)
