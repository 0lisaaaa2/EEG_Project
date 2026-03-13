

def mean_amplitude(evoked, roi, tmin, tmax):
    evoked_roi = evoked.copy().pick_channels(roi)
    evoked_crop = evoked_roi.crop(tmin=tmin, tmax=tmax)
    return evoked_crop.data.mean()

def additional_stats(evoked_front_sym, evoked_pers_sym, evoked_front_asym, evoked_pers_asym):
    