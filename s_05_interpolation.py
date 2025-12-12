import mne

def interpolate_bad_channels(raw):
    raw_interp = raw.copy()
    raw_interp.set_montage('standard_1020')
    raw_interp.interpolate_bads(reset_bads=True)
    return raw_interp