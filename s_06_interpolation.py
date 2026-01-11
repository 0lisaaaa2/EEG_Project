import mne

def interpolate_bad_channels(raw):
    raw_interp = raw.copy()
    print("Blub", raw_interp.info['bads'])  # ensure bads are set

    exg_channels = ["EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"]
    for ch in exg_channels:
        if ch in raw_interp.ch_names:
            raw_interp.set_channel_types({ch: "misc"})
    raw_interp.set_montage('standard_1020')

    before = raw.copy().get_data(picks=["P1"])
    raw_interp.interpolate_bads(reset_bads=True)
    after = raw_interp.get_data(picks=["P1"])

    #print("Before:", before[:,:5])
    #print("After:", after[:,:5])

    #raw.plot(block=True, scalings=40e-6, picks=["P1", "POz", "Pz"])
    #raw_interp.plot(block=True, scalings=40e-6, picks=["P1", "POz", "Pz"])

    return raw_interp