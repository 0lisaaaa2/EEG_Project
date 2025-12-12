import mne
from mne_icalabel import label_components


"""
Get a copy of EEG data and prepare it for ICA
input: raw (EEG data)
output: raw_ica (copied and prepared EEG data)
"""
def get_ica_copy(raw):
    raw_ica = raw.copy().pick(picks=mne.pick_types(raw.info, eeg=True))
    #raw_ica = raw.copy().pick(picks=mne.pick_types(raw.info, eeg=True, meg=False, eog=True, exclude='bads'))
    raw_ica = raw_ica.filter(l_freq=1.0, h_freq=None)
    raw_ica.set_montage('standard_1020')
    #raw_ica = raw_ica.set_eeg_reference('average') # is this required?
    return raw_ica


"""
Set ICA to use for fitting
input: raw (EEG data)
output: ica
"""
def get_ica(raw):
    ica = mne.preprocessing.ICA(
        n_components=0.99,
        method="fastica", #"fastica"
        max_iter="auto",
        random_state=97
    )
    return ica


"""
Label all components found during ICA
input: raw (EEG Data), ica
"""
def label_components_ica(raw, ica):
    labels = label_components(raw, ica, method='iclabel') # probabilities per IC and category
    print(labels)
    return labels


"""
Exclude "bad" components.
input: ica, labels
"""
def exclude_components(ica, labels):
    # exlude everything that is not brain or other with a probability of at least 0.8
    excluded_components = [
        idx for idx, lbl in enumerate(labels['labels'])
        if lbl not in ['brain', 'other'] and labels['y_pred_proba'][idx] >= 0.8
    ]
    print(f"Excluding components: {excluded_components}")
    ica.exclude = excluded_components


"""
Do ICA, plot and find and remove "bad" components
input: raw (EEG Data)
return: raw_cleaned (EEG Data after ICA)
"""
def ica(raw):
    raw_ica = get_ica_copy(raw)
    ica = get_ica(raw_ica)

    ica.fit(raw_ica)

    labels = label_components_ica(raw_ica, ica)

    # show time series of ICs
    ica.plot_sources(raw, show_scrollbars=True, show=True)
    ica.plot_components()
    
    exclude_components(ica, labels)
    raw_cleaned = ica.apply(raw.copy())
    return raw_cleaned