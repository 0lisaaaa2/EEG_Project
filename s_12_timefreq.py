import mne
import config
import numpy as np
import matplotlib.pyplot as plt


"""
Theta: 4-7 Hz
Alpha: 8-13 Hz
Beta: 14-30 Hz
Gamma: 30-40+ Hz

time frequency analysis is non-linear: compute tfr on epochs, then average them later (dont: compute tfr from grand average erp)
"""

def compute_tfr(epochs, condition, posterior_channels=config.posterior_channels):
    """
    Compute time-frequency power for a condition on posterior electrodes
    """

    # Pick posterior channels
    epochs = epochs.copy().load_data()
    epochs_post = epochs[condition].copy().pick(posterior_channels)

    # Frequencies of interest
    freqs = np.arange(4, 40, 1)   # 4–40 Hz
    n_cycles = freqs / 2         # standard choice

    # Compute TFR using Morlet wavelets
    power = mne.time_frequency.tfr_morlet(
        epochs_post,
        freqs=freqs,
        n_cycles=n_cycles,
        use_fft=True,
        return_itc=False,
        average=True
    )

    # Baseline correction
    power.apply_baseline((config.tmin_baseline, config.tmax_baseline), mode="logratio")

    return power

def plot_tfr(power, title):
    power.plot(
        picks="all",
        combine="mean",   # average across posterior electrodes
        title=title
    )