from analysis import *
import os

def test():
    save_path = "figures"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    perf = PerformanceMetrics('pilot_study_data')
    perf.plot_results(save_path)

test()

