#!/usr/bin/env python3
"""Same-length patch of the About-box version string inside DESKTOP.RSC (offsets stay valid)."""
import sys
OLD = b"Version 3.2.3-pacc10a, August 2005"
NEW = b"Version 3.2.3-owc_01a, Nov 2026"
p = sys.argv[1]
d = open(p, 'rb').read()
assert d.count(OLD) == 1, "version string not found exactly once"
open(p, 'wb').write(d.replace(OLD, NEW.ljust(len(OLD))))
print("patched", p)
