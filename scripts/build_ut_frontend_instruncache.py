import os
from comm import warning, info, get_all_rtl_files


def build(cfg):
    from tempfile import NamedTemporaryFile
    from toffee_test.markers import match_version
    from comm import error, info, get_root_dir, exe_cmd

    # check version
    if not match_version(cfg.rtl.version, "openxiangshan-kmh-*"):
        error(f"frontend_instruncache: Unsupported RTL version {cfg.rtl.version}")
        return False

    # find source files for InstrUncache
    rtl_files = get_all_rtl_files("InstrUncache", cfg=cfg)
    info(f"rtl_files: {rtl_files}")
    assert rtl_files, "Cannot find RTL files of Frontend.InstrUncache"

    # additional internal signal files
    internal_signals_path = os.path.join(
        get_root_dir("scripts/instruncache_related/instruncache_internals.yaml")
    )
    # assert os.path.exists(internal_signals_path), "Cannot find internal signal files"

    # export InstrUncache.sv
    if not os.path.exists(get_root_dir("dut/InstrUncache")):
        info("Exporting InstrUncache.sv")
        with NamedTemporaryFile("w+", encoding="utf-8", suffix=".txt") as filelist:
            filelist.write("\n".join(rtl_files))
            filelist.flush()
            s, _, err = exe_cmd(
                f"picker export --cp_lib false {rtl_files[0]} --fs {filelist.name} --lang python --tdir "
                f"{get_root_dir('dut')}/ -w InstrUncache.fst -c --internal={internal_signals_path}"
            )
        assert s, err
    return True


def get_metadata():
    return {
        "dut_name": "frontend_instruncache",
        "dut_dir": "InstrUncache",
        "test_targets": [
            "ut_frontend/instruncache/classic_version",
            "ut_frontend/instruncache/toffee_version",
            "ut_frontend/instruncache",
            "ut_frontend"
        ]
    }


def line_coverage_files(cfg):
    return ["InstrUncache.v"]
