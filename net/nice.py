#!/usr/bin/env python3


import glob
import os
import re


for filename in glob.iglob("*.errors"):
    root, _ = os.path.splitext(filename)
    with open(filename) as errfile, \
      open(root + ".mathematica.errors", 'w') as mathfile:
        data = errfile.read()
        data = data.translate(str.maketrans('[]', '{}'))
        data = re.sub('e', '*^', data)
        mathfile.write(data)
