# -*- encoding: utf-8 -*-

from lib.placement import *
import lib.placement
import imp

print "call reload after you have modify lib/placement.py"

def reload():
    imp.reload(lib.placement)
    print "please run this statement manually:"
    print "from lib.placement import *"