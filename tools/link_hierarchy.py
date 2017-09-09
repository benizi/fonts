#!/usr/bin/env python
#
# Create a hierarchy of symlinks to the fonts.
#
# This is useful to, e.g., add all the fonts to the ConTeXt font loading path:
#
# $ tools/link_hierarchy.py /usr/share/fonts/google-fonts
# $ env OSFONTDIR=/usr/share/fonts mtxrun --script fonts --reload
from sys import argv
import os
from os import path
from os.path import dirname

class IllegalArgumentError(ValueError):
  pass

if len(argv) < 2:
  raise IllegalArgumentError("Usage: %s output-directory [source]" % argv[0])

outdir = argv[1]
googfonts = argv[2] if len(argv) > 2 else dirname(dirname(argv[0]))
#print("OUT={%(outdir)s}\nSRC={%(googfonts)s}" % locals())

for root, subdirs, files in os.walk(googfonts):
    for f in files:
        full = path.join(root, f)
        _, ext = path.splitext(f)
        if ext != '.ttf':
            continue
        linkdir = path.join(outdir, f[0].lower())
        link = path.join(linkdir, f)
        os.makedirs(linkdir, exist_ok=True)
        if not path.exists(link):
            os.symlink(full, link)
            print("%(link)s -> %(full)s" % locals())
        #print("f={%(f)s} ext={%(ext)s}" % locals())
        #print("full {%(full)s}" % locals())
