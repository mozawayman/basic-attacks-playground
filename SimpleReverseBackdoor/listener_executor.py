#!/usr/bin/env python

import Listener as l

listener = l.Listener("10.0.2.15", 4444)
listener.start(bufferSize=1024)
