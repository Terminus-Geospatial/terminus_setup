---
trigger: always_on
---

* All new python files should have this initial structure:

```python
#!/usr/bin/env python3
#
############################# INTELLECTUAL PROPERTY RIGHTS #############################
##                                                                                    ##
##                           Copyright (c) 2024 Terminus LLC                          ##
##                                All Rights Reserved.                                ##
##                                                                                    ##
##          Use of this source code is governed by LICENSE in the repo root.          ##
##                                                                                    ##
############################# INTELLECTUAL PROPERTY RIGHTS #############################
#
#    File:    tmns-build-all.py
#    Author:  Marvin Smith
#    Date:    8/2/2024
#
#    Purpose:  Build tmns applications in a more advanced way

#  Python Standard Libraries
import argparse
import configparser
import logging
import os
import subprocess
```

* Please organize imports, unless there is a logical reason otherwise, alphabetically, and grouped by project.  I always start with "Python Standard Libraries", add things like numpy, and then end with my own project files.  Don't add a section such as "Python Standard Libraries", if there are no imports of that type

* I prefer spaces between parenthesis and variables inside