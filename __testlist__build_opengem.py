"""OpenGEM build pin. Packages the fork's tree under GIT_SRC_DIR into one zip and
registers it as build output {opengem_pkg}, so A/B pins give every emulator
testlist (DOSBox-X, QEMU i386, 86Box) the same OpenGEM. Placeholder recipe: the
SDK tree has no build script yet, so this zips GIT_SRC_DIR/binary/{opengem_rel};
swap in the real OpenWatcom build when it exists.
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
    "function": "BUILD: OpenGEM package",
    "projbasedir": "/testsrc/sourcedir/",
    "host_flag": "LINUX_VIRT",
    "gem_repo": "{projbasedir}{projdir}",
    "opengem_rel": "OPENGEM7-RC3",
    "build_slot": "",
    "build_workdir": "{gem_repo}",
    "opengem_out": "{projbasedir}{projdir}/test_objoutput/build_out_opengem",
    "opengem_pkg": "{opengem_out}/opengem.zip",
    "is_tool": True,
    "build_tool": True,
    "build_output": "opengem_pkg",
    "build_repo": "{build_workdir}",
    "slot_config": {
        "opengem_out": "{projbasedir}{projdir}/test_objoutput/build_out_opengem_{build_slot}",
    },
    "structure": {"project": {"_rel": "{projdir}"}},
    "steps": [
        {
            "action": "test_hostbuild",
            "title": "package OpenGEM",
            "description": "Zip GIT_SRC_DIR/binary/{opengem_rel} (placeholder for a real OpenWatcom build).",
            "param": {
                "command": "set -e; rm -rf '{opengem_out}'; mkdir -p '{opengem_out}'; cd '{gem_repo}/GIT_SRC_DIR/binary/{opengem_rel}'; zip -qr '{opengem_pkg}' .; ls -l '{opengem_pkg}'",
                "timeout": 300,
            },
            "subaction": "",
        },
        {
            "action": "test_fileexists",
            "title": "verify package",
            "param": {"file_path": "{opengem_pkg}", "min_size": 100000, "timeout": 10},
            "subaction": "",
        },
    ],
    "description": "Registers the OpenGEM package as a build object (A/B pin).",
    "tags": ["build", "opengem"],
}
PATHS = init_test_env(CONFIG, __name__)
