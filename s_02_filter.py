import matplotlib.pyplot as plt
import numpy as np
import config


"""
Apply high- and low-pass-filtering and notch-filtering to the raw data, and visualize the power spectrum before and after filtering.
"""

# apply all filters and plot frequencyspectrum
def filter(raw):
    raw_after_highlow = highlowpass(raw)
    raw_after_notch = notch(raw_after_highlow)
    frequencyspectrum(raw, raw_after_highlow, raw_after_notch)

    return raw_after_notch

# compute and plot the frequencyspectrum for three functions
def frequencyspectrum(raw_before_filter, raw_after_highlow, raw_after_notch, fmax=100):

    # Compute PSD (returns V²/Hz)
    psd_before_filter = raw_before_filter.compute_psd(fmax=fmax)
    psd_after_highlow = raw_after_highlow.compute_psd(fmax=fmax)
    psd_after_notch = raw_after_notch.compute_psd(fmax=fmax)
    
    # Calculate psd
    psd_before_filter = raw_before_filter.compute_psd(fmax=fmax)
    psd_after_highlow = raw_after_highlow.compute_psd(fmax=fmax)
    psd_after_notch = raw_after_notch.compute_psd(fmax=fmax)

    # Mean over all channels
    psd_before_filter_mean = psd_before_filter.get_data().mean(axis=0)
    psd_after_highlow_mean = psd_after_highlow.get_data().mean(axis=0)
    psd_after_notch_mean = psd_after_notch.get_data().mean(axis=0)

    # Get frequenies
    freqs_1 = psd_before_filter.freqs
    freqs_2 = psd_after_highlow.freqs
    freqs_3 = psd_after_notch.freqs

    # uncomment to plot the plot
    #plt.figure(figsize=(10, 5))
    #plt.plot(freqs_1, 10 * np.log10(psd_before_filter_mean), label='Before Filtering')
    #plt.plot(freqs_2, 10 * np.log10(psd_after_highlow_mean), label='After HighLowPass Filter')
    #plt.plot(freqs_3, 10 * np.log10(psd_after_notch_mean), label='After Notch Filter')
    #plt.xlabel("Frequency (Hz)")
    #plt.ylabel("Power (dB)")
    #plt.title("Power Spectrum Before vs After Filtering")
    #plt.legend()
    #plt.show() # delete comment if you want to plot

# highpass and lowpass filtering
def highlowpass(raw):
    highpass = config.highpass
    lowpass = config.lowpass
    raw_filtered = raw.copy().filter(
        l_freq=highpass,
        h_freq=lowpass
    )
    return raw_filtered

# notch-filtering
def notch(raw):
    frequency = config.notch
    return raw.copy().notch_filter(frequency)