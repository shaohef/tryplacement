# -*- encoding: utf-8 -*-

from lib.placement import *
from lib.glance import *
from lib.kstoken import reload_token
import lib.placement
import lib.glance
import imp

print "call reload after you have modify lib/placement.py and lib/glance.py"

def reload():
    imp.reload(lib.placement)
    imp.reload(lib.glance)
    print "please run this statement manually:"
    print "from lib.placement import *"
    print "from lib.glance import *"
