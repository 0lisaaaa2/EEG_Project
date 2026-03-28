import mne

"""
Compute perspective cost as difference between SPN amplitudes in frontoparallel and perspective conditions, and as difference wave between SPN_front and SPN_persp.
"""

# compute perspective cost as amplitude difference
def compute_perspective_cost_amp(spn_front_amp, spn_persp_amp):
    return spn_front_amp - spn_persp_amp

# compute perspective cost as difference wave
def compute_perspective_cost_spn(spn_front, spn_persp):
    return mne.combine_evoked([spn_front, spn_persp], weights=[1, -1])
