"""testlist1: compile the FreeGEM Desktop 3.2.3 source (the OpenGEM desktop) with
OpenWatcom 16-bit small model under DOSBox-X, to see what errors the port hits.
The desktop is written for Pacific C (pacc, ppdgem-s.lib GEM bindings), so
compile/link errors are the expected output; the last step prints BUILD.LOG and
fails when it contains "Error!". Run/launch of the desktop comes after it builds.
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
    "function": "testlist1",
    "projbasedir": "/testsrc/sourcedir/",
    "hdd1_template": "dos622_owc.img",
    "hdd1_overlay": "c_drive.qcow2",
    "machine": "svga_s3",
    "memsize": 16,
    "desk_zip": "{projbasedir}{projdir}/GIT_SRC_DIR/source/OpenGEM-7-RC3-SDK/sdk/desktop/FreeGEM Desktop 3.2.3.zip",
    "gem_kit": "{projbasedir}{projdir}/GIT_SRC_DIR/source/OpenGEM-7-RC3-SDK/sdk/bindings/pacific-c",
    "desk_run": "{projbasedir}{projdir}/test_objoutput/desk_run",
    "structure": {"project": {"_rel": "{projdir}", "out_dir": {"_rel": "test_objoutput"}}},
    "steps": [
        {
            "action": "test_hostbuild",
            "title": "extract desktop source",
            "description": "D: is a host dir: unpack the zip fresh, add the build batch files.",
            "param": {
                "command": "set -e; rm -rf '{desk_run}'; mkdir -p '{desk_run}'; unzip -qo '{desk_zip}' -d '{desk_run}'; cp '{projbasedir}{projdir}/prereqs/BUILD.BAT' '{projbasedir}{projdir}/prereqs/ONE.BAT' '{desk_run}/'; mkdir -p '{desk_run}/GEMINC'; cp '{gem_kit}/INCLUDE/'*.H '{desk_run}/GEMINC/'; sh '{projbasedir}{projdir}/prereqs/port_desktop.sh' '{desk_run}'; ls '{desk_run}' | wc -l",
                "timeout": 60
            },
            "subaction": ""
        },
        {
            "action": "test_flatten_qcow_to_raw",
            "param": {
                "hdd1_template": "{hdd1_template}",
                "qcow_path": "{projbasedir}{projdir}/{hdd1_overlay}",
                "raw_path": "{projbasedir}{projdir}/test_objoutput/c_drive_raw.img"
            },
            "subaction": ""
        },
        {
            "action": "test_dosbox_conf",
            "param": {
                "autoexec": [
                    "imgmount c {projbasedir}{projdir}/test_objoutput/c_drive_raw.img -t hdd -fs fat",
                    "mount d {desk_run}"
                ],
                "config_path": "{projbasedir}{projdir}/test_objoutput/dosbox_owc.conf",
                "cpu_cycles": "max",
                "machine": "{machine}",
                "memsize": "{memsize}"
            },
            "subaction": ""
        },
        {
            "action": "test_start_dosbox",
            "param": {
                "config_path": "{projbasedir}{projdir}/test_objoutput/dosbox_owc.conf",
                "name": "dosbox1",
                "timeout": 20
            },
            "subaction": ""
        },
        {
            "action": "test_ocrwordsearch",
            "param": {"name": "dosbox1", "require_success": "True", "successphrase": "drive c is mounted",
                      "attemptdelay": "2", "numberofattempts": "10"},
            "subaction": ""
        },
        {"action": "test_sendcommand", "param": {"cmd_text": "d:", "delay": "1", "name": "dosbox1", "special_keys": "Return"}, "subaction": ""},
        {"action": "test_sendcommand", "title": "run BUILD.BAT", "param": {"cmd_text": "build", "name": "dosbox1", "special_keys": "Return"}, "subaction": ""},
        {
            "action": "test_fileexists",
            "description": "BUILD.BAT writes DONE.TXT last, whatever the compiler said.",
            "param": {"file_path": "{desk_run}/DONE.TXT", "timeout": 600},
            "subaction": ""
        },
        {
            "action": "test_ocrwordsearch",
            "param": {"name": "dosbox1", "require_success": False, "successphrase": "d:",
                      "takeascreenshot": True, "attemptdelay": "2", "numberofattempts": "10"},
            "subaction": ""
        },
        {"action": "test_terminate_all", "param": {}, "subaction": "", "teardown": True},
        {
            "action": "test_hostbuild",
            "title": "report compiler errors",
            "description": "wcc writes diagnostics to <file>.ERR, so read those; fails on any 'Error!'.",
            "param": {
                "command": "cd '{desk_run}'; for f in *.ERR; do echo \"## $f\"; tr -d '\\r' < $f | head -c 1500; done | head -c 12000; echo; echo ERRORS: $(cat *.ERR | grep -c 'Error!'); echo FILES-WITH-ERRORS: $(grep -l 'Error!' *.ERR | wc -l); ! grep -q 'Error!' *.ERR",
                "timeout": 30
            },
            "subaction": ""
        }
    ],
    "description": "Build the OpenGEM desktop with OpenWatcom in DOSBox-X and surface errors.",
    "tags": ["dosbox", "openwatcom", "desktop", "build"],
}
PATHS = init_test_env(CONFIG, __name__)
