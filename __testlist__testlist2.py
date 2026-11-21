"""testlist2: build the GEM bindings library (LIBSRC -> PPDGEM-L.LIB) and the FreeGEM
Desktop 3.2.3 with OpenWatcom 16-bit large model under DOSBox-X, then link
DESKTOP.EXE. Pacific-isms are patched in a throwaway copy by prereqs/port_*.sh;
the two Pacific assembler files are ported to wasm (prereqs/*.asm).
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
    "function": "testlist2",
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
                "command": "set -e; P='{projbasedir}{projdir}/prereqs'; K='{gem_kit}'; R='{desk_run}'; rm -rf \"$R\"; mkdir -p \"$R\"; unzip -qo '{desk_zip}' -d \"$R\"; mkdir -p \"$R/GEMINC\" \"$R/LIBSRC/GEMINC\"; cp \"$K/INCLUDE/\"*.H \"$R/GEMINC/\"; cp \"$K/INCLUDE/\"*.H \"$R/LIBSRC/GEMINC/\"; cp \"$K/LIBSRC/\"*.C \"$K/LIBSRC/\"*.H \"$R/LIBSRC/\"; cp $P/BUILD2.BAT $P/ONEL.BAT $P/ONED.BAT $P/LINK.LNK $P/ppdldraw.asm $P/deskosif.asm \"$R/\"; sh $P/port_desktop.sh \"$R\"; rm -f \"$R/ICN2XML.C\" \"$R/XML2ICN.C\" \"$R/DESKOSIF.AS\"; sh $P/port_lib.sh \"$R/LIBSRC\"; ls \"$R/LIBSRC\" | wc -l",
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
        {"action": "test_sendcommand", "title": "run BUILD2.BAT", "param": {"cmd_text": "build2", "name": "dosbox1", "special_keys": "Return"}, "subaction": ""},
        {
            "action": "test_fileexists",
            "description": "BUILD2.BAT writes DONE.TXT last, whatever the compiler said.",
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
            "description": "Fails on any compiler error or a missing DESKTOP.EXE.",
            "param": {
                "command": "cd '{desk_run}'; tr -d '\\r' < BUILD.LOG | grep -v '^===' | tail -40; echo; E=$(cat *.ERR LIBSRC/*.ERR 2>/dev/null | grep -c 'Error!'); echo ERRORS: $E; ls LIBSRC/*.OBJ | wc -l; ls -la LIBSRC/PPDGEM-L.LIB DESKTOP.EXE; test -s DESKTOP.EXE && test $E -eq 0",
                "timeout": 30
            },
            "subaction": ""
        }
    ],
    "description": "Build the OpenGEM desktop with OpenWatcom in DOSBox-X and surface errors.",
    "tags": ["dosbox", "openwatcom", "desktop", "build"],
}
PATHS = init_test_env(CONFIG, __name__)
