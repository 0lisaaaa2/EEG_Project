# davor und dannach frequency spectrum plotten, damit man sieht was rausgefiltert wurde

import matplotlib.pyplot as plt
import numpy as np

import mne

import config
import s_00_fetch_data


def frequencyspectrum(raw_before, raw_after, fmax=100):
    psd_before, freqs = raw_before.compute_psd(fmax=fmax)
    psd_after, _ = raw_after.compute_psd(fmax=fmax)

    # Mittelwert über alle Kanäle
    psd_before_mean = psd_before.get_data().mean(axis=0)
    psd_after_mean = psd_after.get_data().mean(axis=0)

    plt.figure(figsize=(10, 5))
    plt.plot(freqs, 10 * np.log10(psd_before_mean), label='Before Filtering')
    plt.plot(freqs, 10 * np.log10(psd_after_mean), label='After Filtering')
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



if __name__ == "__main__":
    raw = s_00_fetch_data.load_data("001", "regfront")
    #raw_after_highlow = highlowpass(raw_before)
    #frequencyspectrum(raw, raw_after_after_highlow)
    #raw_after_notch = notch(raw_after)