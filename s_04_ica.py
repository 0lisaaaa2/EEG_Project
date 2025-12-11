import mne

def ica(raw):
    exg_channels = ['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8']
    raw_ica = raw.copy().pick(picks=mne.pick_types(raw.info, eeg=True))
    raw_ica.set_channel_types({ch: 'misc' for ch in exg_channels if ch in raw.ch_names})
    raw_ica = raw_ica.filter(l_freq=1.0, h_freq=None)
    raw_ica.set_montage('standard_1020')
    ica = mne.preprocessing.ICA(
        n_components=0.99,
        method='fastica',
        max_iter=500,
        random_state=97
    )
    ica.fit(raw_ica)
    ica.plot_components()
    ica.exclude = [1]
    return ica.apply(raw.copy())