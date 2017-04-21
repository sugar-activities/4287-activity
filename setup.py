#!/usr/bin/env python
from sugar.activity import bundlebuilder

# ignore directories not needed for activity
bundlebuilder.IGNORE_DIRS.append(".bzr")
bundlebuilder.IGNORE_DIRS.append("thirdparty")

# ignore files (vi *.swp, bzr, and inkscape icons)
bundlebuilder.IGNORE_FILES.append(".bzrignore")
bundlebuilder.IGNORE_FILES.append("*.swp")
bundlebuilder.IGNORE_FILES.append("*-inkscape.svg")
bundlebuilder.IGNORE_FILES.append("*-gtk.png")

bundlebuilder.start()

