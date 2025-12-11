import numpy as np
import mne

def find_flat_channels(raw, thresh=1e-7):
    data = raw.get_data()
    variances = data.var(axis=1)
    flat = [raw.ch_names[i] for i, var in enumerate(variances) if var < thresh]
    return flat

def find_bad_amplitude(raw, z_thresh=3):
    data = raw.get_data()
    variances = data.var(axis=1)

    z = (variances - variances.mean()) / variances.std()
    bads = [raw.ch_names[i] for i, zi in enumerate(z) if abs(zi) > z_thresh]
    return bads


def find_bad_corr(raw, thresh=0.4):
    data = raw.get_data()

    # Korrelationsmatrix
    corr = np.corrcoef(data)
    mean_corr = corr.mean(axis=1)

    bads = [raw.ch_names[i] for i, mc in enumerate(mean_corr) if mc < thresh]
    return bads

def auto_find_bad_channels(raw):
    bads = set()

    bads.update(find_flat_channels(raw))
    bads.update(find_bad_amplitude(raw, z_thresh=3))
    bads.update(find_bad_corr(raw, thresh=0.4))

    return list(bads)
