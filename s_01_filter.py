# davor und dannach frequency spectrum plotten, damit man sieht was rausgefiltert wurde

import matplotlib.pyplot as plt
import numpy as np
import mne
import config


def frequencyspectrum(raw_before_filter, raw_after_highlow, raw_after_notch, fmax=100):
    psd_before_filter = raw_before_filter.compute_psd(fmax=fmax)
    psd_after_highlow = raw_after_highlow.compute_psd(fmax=fmax)
    psd_after_notch = raw_after_notch.compute_psd(fmax=fmax)

    # Mittelwert über alle Kanäle
    psd_before_filter_mean = psd_before_filter.get_data().mean(axis=0)
    psd_after_highlow_mean = psd_after_highlow.get_data().mean(axis=0)
    psd_after_notch_mean = psd_after_notch.get_data().mean(axis=0)

    freqs_1 = psd_before_filter.freqs
    freqs_2 = psd_after_highlow.freqs
    freqs_3 = psd_after_notch.freqs

    plt.figure(figsize=(10, 5))
    plt.plot(freqs_1, 10 * np.log10(psd_before_filter_mean), label='Before Filtering')
    plt.plot(freqs_2, 10 * np.log10(psd_after_highlow_mean), label='After HighLowPass Filter')
    plt.plot(freqs_3, 10 * np.log10(psd_after_notch_mean), label='After Notch Filter')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (dB)")
    plt.title("Power Spectrum Before vs After Filtering")
    plt.legend()
    plt.show()


def highlowpass(raw):
    highpass = config.highpass
    lowpass = config.lowpass
    raw_filtered = raw.copy().filter(
        l_freq=highpass,
        h_freq=lowpass
    )
    return raw_filtered


def notch(raw):
    frequency = config.notch
    return raw.copy().notch_filter(frequency)



def filter(raw):
    # raw = s_00_fetch_data.load_data("001", "regfront")
    raw_after_highlow = highlowpass(raw)
    raw_after_notch = notch(raw_after_highlow)
    frequencyspectrum(raw, raw_after_highlow, raw_after_notch)

    return raw_after_notch