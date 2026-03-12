import mne
import config
import numpy as np
import matplotlib.pyplot as plt
from mne.stats import permutation_cluster_test, permutation_cluster_1samp_test


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

# plot tfr average over posterior electrodes
def compute_tfr_allelectrodes(epochs, condition, posterior_channels=config.posterior_channels):
    # Pick posterior channels
    epochs = epochs.copy().load_data()
    epochs_post = epochs[condition].copy().pick(posterior_channels)

    freqs = np.arange(4, 40, 1)   # 4–40 Hz
    n_cycles = freqs / 2  

    power_total = epochs_post.compute_tfr(freqs=freqs, n_cycles=n_cycles, average=True,method='morlet')
    plot_allelec(power_total)
    return power_total

# plot tfr average over posterior electrodes
def plot_tfr(power, title, vmin, vmax):
    power.plot(
        picks="all",
        combine="mean",   # average across posterior electrodes
        title=title,
        vlim=(vmin, vmax),
    )

# plot tfr for all electrodes
def plot_allelec(power):
    power.plot_topo(baseline=[config.tmin_baseline,config.tmax_baseline],mode="logratio",vmin=-2,vmax=2);



def run_statistics_tfr(tfr_spn_front_value, tfr_spn_persp_value, alpha, n_perm):
    # extract data arrays
    # shape: subjects x channels x freqs x times
    data_front = np.stack([tfr.data for tfr in tfr_spn_front_value])
    data_persp = np.stack([tfr.data for tfr in tfr_spn_persp_value])

    # difference for paired test
    diff = data_front - data_persp

    # calulate effect size in alpha band
    freqs = tfr_spn_front_value[0].freqs
    times = tfr_spn_front_value[0].times

    # reshape to subjects x features
    n_subj, n_ch, n_freq, n_time = diff.shape
    diff_reshaped = diff.reshape(n_subj, -1)

    # permutation cluster test
    T_obs, clusters, p_values, H0 = permutation_cluster_1samp_test(
        diff_reshaped,
        n_permutations=n_perm,
        tail=0
    )

    # find significant clusters
    significant_clusters = [
        clusters[i] for i, p in enumerate(p_values) if p < alpha
    ]

    print(f"Found {len(significant_clusters)} significant clusters")

    print("\n=== TF Statistics: SPN Front vs Perspective ===")

    print(f"Total clusters found: {len(clusters)}")

    print(f"Significant clusters (p < 0.05): {len(significant_clusters)}")

    if len(significant_clusters) == 0:
        print("No significant TF clusters found.")
    else:
        for i, idx in enumerate(significant_clusters):
            p = p_values[i]
            size = len(clusters[i][0])
            print(f"Cluster {i+1}: p = {p:.4f}, size = {size}")


# calculate effect sizes
# cohens d for each time-frequency point, then average across channels and alpha frequencies
def calculate_effect_size(tfr_spn_front_value, tfr_spn_persp_value, alpha_band=(8, 12)):
    # extract data arrays
    # shape: subjects x channels x freqs x times
    data_front = np.stack([tfr.data for tfr in tfr_spn_front_value])
    data_persp = np.stack([tfr.data for tfr in tfr_spn_persp_value])

    # difference for paired test
    diff = data_front - data_persp

    # calulate effect size in alpha band
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