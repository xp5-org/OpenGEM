"""testlist3: playtest. Stage OpenGEM 7 RC3 with the OpenWatcom-built DESKTOP.EXE (from
testlist2) swapped in as DESKTOP.APP, boot it in DOSBox-X and check the desktop comes up.
The original Pacific-built DESKTOP.APP is kept as DESKTOP.ORG next to it.
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
    "instance_name": "dosbox1",
    "function": "testlist3",
    "projbasedir": "/testsrc/sourcedir/",
    "machine": "svga_s3",
    "memsize": 16,
    "gem_src": "{projbasedir}{projdir}/GIT_SRC_DIR/binary/OPENGEM7-RC3",
    "new_desktop": "{projbasedir}{projdir}/test_objoutput/desk_run/DESKTOP.EXE",
    "new_rsc": "{projbasedir}{projdir}/test_objoutput/desk_run/DESKTOP.RSC",
    "gem_run": "{projbasedir}{projdir}/test_objoutput/gem_run",
    "structure": {"project": {"_rel": "{projdir}", "out_dir": {"_rel": "test_objoutput"}}},
    "steps": [
        {
            "action": "test_hostbuild",
            "title": "stage OpenGEM with the new desktop",
            "description": "C: is a host dir: copy the RC3 tree, swap in the OpenWatcom DESKTOP.EXE as DESKTOP.APP.",
            "param": {
                "command": "set -e; test -s '{new_desktop}'; grep -q owc_01a '{new_rsc}'; rm -rf '{gem_run}'; mkdir -p '{gem_run}'; cp -r '{gem_src}/.' '{gem_run}/'; cd '{gem_run}/GEMAPPS/GEMSYS'; mv DESKTOP.APP DESKTOP.ORG; cp '{new_desktop}' DESKTOP.APP; cp '{new_rsc}' DESKTOP.RSC; ls -l DESKTOP.*",
                "timeout": 60
            },
            "subaction": ""
        },
        {
            "action": "test_dosbox_conf",
            "param": {
                "autoexec": [
                    "mount c {gem_run}",
                    "c:",
                    "echo drive c is mounted"
                ],
                "config_path": "{projbasedir}{projdir}/test_objoutput/dosbox_gem.conf",
                "cpu_cycles": "max",
                "machine": "{machine}",
                "memsize": "{memsize}"
            },
            "subaction": ""
        },
        {
            "action": "test_start_dosbox",
            "param": {"config_path": "{projbasedir}{projdir}/test_objoutput/dosbox_gem.conf", "name": "dosbox1", "timeout": 20},
            "subaction": ""
        },
        {
            "action": "test_ocrwordsearch",
            "param": {"name": "dosbox1", "require_success": "True", "successphrase": "drive c is mounted",
                      "attemptdelay": "2", "numberofattempts": "10"},
            "subaction": ""
        },
        {"action": "test_sendcommand", "title": "start GEM", "param": {"cmd_text": "gem", "name": "dosbox1", "special_keys": "Return"}, "subaction": ""},
        {
            "action": "test_ocrwordsearch",
            "description": "GEM desktop menu bar is up.",
            "param": {"name": "dosbox1", "require_success": "True", "successphrase": "Options",
                      "takeascreenshot": True, "attemptdelay": "2", "numberofattempts": "10"},
            "subaction": ""
        },
        {"action": "test_terminate_all", "param": {}, "subaction": "", "teardown": True, "pause_on": True}
    ],
    "description": "Playtest: boot OpenGEM in DOSBox-X with the OpenWatcom-built desktop.",
    "tags": ["dosbox", "openwatcom", "desktop", "playtest"],
}
PATHS = init_test_env(CONFIG, __name__)
