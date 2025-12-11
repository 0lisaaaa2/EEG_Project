import mne
from mne_icalabel import label_components

def ica(raw):
    #exg_channels = ['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8']
    raw_ica = raw.copy().pick(picks=mne.pick_types(raw.info, eeg=True))
    #raw_ica.set_channel_types({ch: 'misc' for ch in exg_channels if ch in raw.ch_names})
    raw_ica = raw_ica.filter(l_freq=1.0, h_freq=None)
    
    raw_ica.set_montage('standard_1020')
    
    ica = mne.preprocessing.ICA(
        n_components=0.99,
        method="fastica",
        max_iter="auto",
        random_state=97
    )

    #ica_raw = raw.copy().drop_channels(raw.info['bads'])
    #ica_raw.set_montage('standard_1020')
    #ica.fit(ica_raw)

    ica.fit(raw_ica)

    # show time series of ICs
    ica.plot_sources(raw, show_scrollbars=True, show=True)

    ica.plot_components()

    labels = label_components(raw_ica, ica, method='iclabel')

    # print(labels["labels"]) # category labels per IC
    print(labels)  # probabilities per IC and category
    
    # exlude everything that is not brain or other with a probability of at least 0.8
    excluded_components = [
        idx for idx, lbl in enumerate(labels['labels'])
        if lbl not in ['brain', 'other'] and labels['y_pred_proba'][idx] >= 0.8
    ]

    print(f"Excluding components: {excluded_components}")

    ica.exclude = excluded_components
    return ica.apply(raw.copy())