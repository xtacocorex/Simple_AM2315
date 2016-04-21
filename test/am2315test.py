#!/usr/bin/env python

from am2315 import AM2315

thsen = AM2315.AM2315()
print "T   ", thsen.read_temperature()
print "H   ", thsen.read_humidity()
print "H,T ", thsen.read_humidity_temperature()

