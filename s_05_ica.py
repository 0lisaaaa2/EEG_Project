import mne
from mne_icalabel import label_components

"""
Applies ICA to the raw EEG data, identifies and excludes "bad" components, and returns the cleaned data.
"""



# get copy of EEG data and prepare it for ICA
def get_ica_copy(raw):
    raw_ica = raw.copy()

    # EXG correctly typed (ON raw_ica!)
    raw_ica.set_channel_types({
        'EXG1': 'eog',
        'EXG2': 'eog',
        'EXG3': 'eog',
        'EXG4': 'eog',
        'EXG5': 'emg',
        'EXG6': 'emg',
        'EXG7': 'misc',
        'EXG8': 'misc',
    })

    # set montage for ICA data 
    raw_ica.set_montage('standard_1020')

    # for ica, only keep eeg and eog channels, exclude bad channels
    raw_ica.pick_types(eeg=True, eog=True, exclude='bads')

    # apply a high-pass filter to remove slow drifts that can interfere with ICA decomposition
    raw_ica.filter(l_freq=1.0, h_freq=None)

    return raw_ica


# set ICA to use for fitting
def get_ica(raw):
    ica = mne.preprocessing.ICA(
        n_components=len(mne.pick_types(raw.info, eeg=True)), 
        method="infomax",  # "fastica" -> use infomax because of icalabel recommendation
        max_iter="auto",
        random_state=97,
        verbose=False
    )
    return ica


# label components using icalabel
def label_components_ica(raw, ica):
    labels = label_components(raw, ica, method='iclabel')  # probabilities per IC and category
    #print(labels)
    return labels


# exclude components that are not brain or other with a probability of at least 0.8
def exclude_components(ica, labels):
    excluded_components = [
        idx for idx, lbl in enumerate(labels['labels'])
        if lbl not in ['brain', 'other'] and labels['y_pred_proba'][idx] >= 0.8
    ]
    #print(f"Excluding components: {excluded_components}")
    ica.exclude = excluded_components


# main function to do ICA and return cleaned data
def ica(raw):
    raw_ica = get_ica_copy(raw)
    ica = get_ica(raw_ica)

    ica.fit(raw_ica)

    labels = label_components_ica(raw_ica, ica)

    # show time series of ICs
    # ica.plot_sources(raw, show_scrollbars=True, show=True)
    # ica.plot_components()

    exclude_components(ica, labels)
    n_excluded = len(ica.exclude)
    raw_cleaned = ica.apply(raw.copy())
    return raw_cleaned, n_excluded