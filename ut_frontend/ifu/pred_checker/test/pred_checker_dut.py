import toffee_test
import toffee
from ..env import PredCheckerEnv
from dut.PredChecker import DUTPredChecker
import toffee.funcov as fc
from toffee.funcov import CovGroup


def init_pred_checker_funcov(dut:DUTPredChecker, g: fc.CovGroup):
    # 1. Add point
    g.add_watch_point(dut, {
        "ERROR": lambda d: getattr(dut, "io_out_stage10ut_fixedRange_0").value == 0,
        "SUCCE": lambda d: getattr(dut, "io_out_stage10ut_fixedRange_0").value == 1,
    }, name = "predChecker_RANGE")
    
    
    

#def init_pred_checker_cover_point(pred_checker):
#    g = fc.CovGroup("predChecker")
#    g.add_watch_point(pred_checker.io_out_stage2Out_fixedMissPred_0, {"io_out_stage20ut_fixedMissPred": lambda x: fc.Eq(0)}, name="PredChecker_MissPred[0]")
#    pred_checker.StepRis(lambda x: g.sample())
#    return g


@toffee_test.fixture
async def predchecker_env(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(DUTPredChecker)
    #toffee_request.add_cov_groups(init_pred_checker_cover_point(dut))
    dut.InitClock("clock")
    toffee.start_clock(dut)
    env = PredCheckerEnv(dut)
    yield env

    import asyncio
    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
            
            
            