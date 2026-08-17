import numpy as np

def time_based_markevery(time_array, n_marks=4):
    time_array = np.asarray(time_array)
    t0, t1 = (time_array[0], time_array[-1])
    target_times = np.linspace(t0, t1, n_marks + 1)
    idx = sorted(set((int(np.argmin(np.abs(time_array - t))) for t in target_times)))
    return idx

def staggered_time_markevery(time_array, n_series=3, n_marks=4):
    time_array = np.asarray(time_array)
    t0, t1 = (time_array[0], time_array[-1])
    span = t1 - t0
    result = []
    for s in range(n_series):
        phase = span * (s / (n_series * (n_marks + 1)))
        target_times = np.linspace(t0, t1, n_marks + 1) + phase
        target_times = np.clip(target_times, t0, t1)
        idx = sorted(set((int(np.argmin(np.abs(time_array - t))) for t in target_times)))
        result.append(idx)
    return result
