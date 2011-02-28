#!/usr/bin/env python
"""
ovals.py - a program for adding oval pin pads to elements
"""

test_element = """
Element["" "Jumper, i.e. single row headers" "" "JUMPER5" 147000 18000 11000 -5000 3 100 ""]
(
	Pin[0 0 6000 3000 6600 3800 "1" "1" "square"]
	Pin[0 10000 6000 3000 6600 3800 "2" "2" ""]
	Pin[0 20000 6000 3000 6600 3800 "3" "3" ""]
	Pin[0 30000 6000 3000 6600 3800 "4" "4" ""]
	Pin[0 40000 6000 3000 6600 3800 "5" "5" ""]
	ElementLine [-5000 -5000 -5000 45000 1000]
	ElementLine [-5000 45000 5000 45000 1000]
	ElementLine [5000 45000 5000 -5000 1000]
	ElementLine [5000 -5000 -5000 -5000 1000]
	ElementLine [-5000 5000 5000 5000 1000]
	ElementLine [5000 5000 5000 -5000 1000]

)
"""
##    print '\n'.join(ovalize(test_element))

#   Pad[-1500 0 1500 0 6000 3000 6600 "" "1" "onsolder"]
#   Pad[-1500 0 1500 0 6000 3000 6600 "" "1" "onsolder"]

# Pin[x y thickness clearance mask drillholedia name number flags]
# Pad[x1 y1 x2 y2 thickness clearance mask name pad_number flags]

RATIO_DEFAULT = 0.5
POSTFIX_DEFAULT = "_oval"
VERSION = "1.0"

def ovals(element, ratio=RATIO_DEFAULT, vert=False, verbose=False):
    if isinstance(element, str):
        element = element.splitlines()
    ret = list()
    pin_count = 0
    for line in element:
        ret.append(line)
        line = line.strip()
        if line.startswith('Pin'):
            pin_count += 1
            data = line.lstrip('Pin[').rstrip(']').split()
            x, y, t, c, m = map(int, data[:5])
            num = int(data[7].strip('"'))

            l = t * ratio # set pad length to thickness * ratio
            if vert == False: # make ovals horizontal
                x1 = x - l/2
                y1 = y
                x2 = x + l/2
                y2 = y
            else: # make them vertical
                x1 = x
                y1 = y + l/2
                x2 = x
                y2 = y - l/2
                
            str_var = (x1, y1, x2, y2, t, c, m, num)
            pad_str = '\tPad[%i %i %i %i %i %i %i "" "%i" "onsolder"]'
            ret.append(pad_str % (str_var))
    if verbose: print "\tGave", pin_count, "pins ovals."
    return ret
            

if __name__ == '__main__':
##    with open('JUMPER5.fp') as f:
##        out = '\n'.join(ovals(f.read(), vert=False))
##    print out
    
    from optparse import OptionParser
    usage = "usage: %prog [options] element1 [element2...]"
    ver = "%%prog %s" % VERSION
    parser = OptionParser(usage=usage, version=ver, description=__doc__)

    parser.add_option("-p", "--postfix",
                  type="str", dest="postfix", default=POSTFIX_DEFAULT,
                  help="String to append to input filename [default: %default]")
    parser.add_option("-r", "--ratio",
                  type="float", dest="ratio", default=RATIO_DEFAULT,
                  help="Ratio of oval pad length to pin dia [default: %default]")
    parser.add_option("-s", "--stdout",
                  action="store_true", dest="stdout", default=False,
                  help="print ovaled element(s) to stdout")
    parser.add_option("-v", "--verbose",
                  action="count", dest="verbose", default=False,
                  help="print status messages to stdout")
    parser.add_option("--vert",
                  action="store_true", dest="vertical", default=False,
                  help="place vertial oval pads instead of horizontal")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        print "No files to work on, I'm going back to sleep..."
        exit(1)
    
    if options.verbose > 1:
        print "ratio:", options.ratio
        print "stdout:", options.stdout
        print "verbose:", options.verbose
        print "vert:", options.vertical

    for a in args:
        if options.verbose:
            print "Opening", a
        with open(a) as f:
            result = '\n'.join(
                ovals(
                    f.read(),
                    ratio=options.ratio,
                    vert=options.vertical,
                    verbose=options.verbose)
                ) + '\n'
        if options.stdout:
            print result
        else:
            filename = (options.postfix+'.').join(a.rsplit('.', 1))
            with open(filename, 'w') as f:
                if options.verbose:
                    print "\tWritting", a, "to", filename
                f.write(result)
        if options.verbose:
            print "\tFinished with", a

