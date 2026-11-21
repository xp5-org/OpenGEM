"""DUMMY tool: 86Box orchestration helper (not built yet). Registers {box86_driver_exe} in the tool registry so
testlists can reference it now; the build step is a placeholder that writes a stub script.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
TESTSRC_HELPERDIR = "/testsrc/pyhelpers"
if TESTSRC_HELPERDIR not in sys.path:
    sys.path.insert(0, TESTSRC_HELPERDIR)

from apphelpers import init_test_env

CONFIG = {
    "parent": "OpenGEM OpenWatcom",
    "projdir": "opengem_openwatcom",
    "function": "tool: box86_driver (dummy)",
    "projbasedir": "/testsrc/sourcedir/",
    "host_flag": "LINUX_VIRT",
    "box86_driver_out": "{projbasedir}{projdir}/test_objoutput/build_out_box86_driver",
    "box86_driver_exe": "{box86_driver_out}/box86_driver.sh",
    "is_tool": True,
    "tool_build": True,
    "tool_sources": [],
    "tool_outputs": {"box86_driver_exe": "{box86_driver_exe}"},
    "structure": {"project": {"_rel": "{projdir}"}},
    "steps": [
        {
            "action": "test_hostbuild",
            "title": "write dummy box86_driver",
            "description": "Placeholder until the real tool exists.",
            "param": {
                "command": "set -e; mkdir -p '{box86_driver_out}'; printf '#!/bin/sh\\necho box86_driver dummy: not implemented\\nexit 1\\n' > '{box86_driver_exe}'; chmod +x '{box86_driver_exe}'",
                "timeout": 30,
            },
            "subaction": "",
        },
        {
            "action": "test_fileexists",
            "title": "verify dummy",
            "param": {"file_path": "{box86_driver_exe}", "min_size": 10, "timeout": 10},
            "subaction": "",
        },
    ],
    "description": "86Box orchestration helper; dummy until built.",
    "tags": ["tool", "dummy"],
}
PATHS = init_test_env(CONFIG, __name__)
