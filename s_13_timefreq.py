import mne
import config
import numpy as np
import matplotlib.pyplot as plt

"""
(Further Analysis)
Compute time-frequency representations (TFRs) for the SPN in the frontoparallel and perspective conditions, and compare them statistically.
"""


"""
Theta: 4-7 Hz
Alpha: 8-13 Hz
Beta: 14-30 Hz
Gamma: 30-40+ Hz
"""

# compute tfr for a condition on posterior electrodes
def compute_tfr(epochs, condition, posterior_channels=config.posterior_channels):
   
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



# plot tfr average over posterior electrodes
def plot_tfr(power, title, vmin, vmax):
    power.plot(
        picks="all",
        combine="mean",   # average across posterior electrodes
        title=title,
        vlim=(vmin, vmax),
    )



# calculate effect size cohens d for alpha band 
# # for each time-frequency point, then average across channels and alpha frequencies
def calculate_effect_size(tfr_spn_front_value, tfr_spn_persp_value, alpha_band=(8, 12)):
    # extract data arrays
    data_front = np.stack([tfr.data for tfr in tfr_spn_front_value])
    data_persp = np.stack([tfr.data for tfr in tfr_spn_persp_value])

    diff = data_front - data_persp

    freqs = tfr_spn_front_value[0].freqs
    times = tfr_spn_front_value[0].times

    # Compute mean and std across subjects
    mean_diff = np.mean(diff, axis=0)       # shape: channels × freqs × times
    std_diff = np.std(diff, axis=0, ddof=1)

    # Cohen's d
    cohens_d = mean_diff / std_diff         # channels × freqs × times

    # Average across channels
    cohens_d_avg = np.mean(cohens_d, axis=0)  # freqs × times

    # Find alpha-band indices
    freq_inds = (freqs >= alpha_band[0]) & (freqs <= alpha_band[1])

    # Mean Cohen's d in alpha band -> average across alpha frequencies and all time points
    alpha_mean_d = np.mean(cohens_d_avg[freq_inds, :])
    print(f"Mean Cohen's d in alpha band (8-12 Hz): {alpha_mean_d:.2f}")