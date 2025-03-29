from analysis import *

def test():
    perf = PerformanceMetrics("data", get_what="both")
    perf.plot_results()

    perf = PerformanceMetrics("data", get_what="block")
    perf.plot_results()

    perf = PerformanceMetrics("data", get_what="random")
    perf.plot_results()

    print("Plots saved in figures folder ...")

test()

