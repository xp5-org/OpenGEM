"""DUMMY tool: DOSBox-X orchestration helper (not built yet). Registers {dosbox_driver_exe} in the tool registry so
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
    "function": "tool: dosbox_driver (dummy)",
    "projbasedir": "/testsrc/sourcedir/",
    "host_flag": "LINUX_VIRT",
    "dosbox_driver_out": "{projbasedir}{projdir}/test_objoutput/build_out_dosbox_driver",
    "dosbox_driver_exe": "{dosbox_driver_out}/dosbox_driver.sh",
    "is_tool": True,
    "tool_build": True,
    "tool_sources": [],
    "tool_outputs": {"dosbox_driver_exe": "{dosbox_driver_exe}"},
    "structure": {"project": {"_rel": "{projdir}"}},
    "steps": [
        {
            "action": "test_hostbuild",
            "title": "write dummy dosbox_driver",
            "description": "Placeholder until the real tool exists.",
            "param": {
                "command": "set -e; mkdir -p '{dosbox_driver_out}'; printf '#!/bin/sh\\necho dosbox_driver dummy: not implemented\\nexit 1\\n' > '{dosbox_driver_exe}'; chmod +x '{dosbox_driver_exe}'",
                "timeout": 30,
            },
            "subaction": "",
        },
        {
            "action": "test_fileexists",
            "title": "verify dummy",
            "param": {"file_path": "{dosbox_driver_exe}", "min_size": 10, "timeout": 10},
            "subaction": "",
        },
    ],
    "description": "DOSBox-X orchestration helper; dummy until built.",
    "tags": ["tool", "dummy"],
}
PATHS = init_test_env(CONFIG, __name__)
