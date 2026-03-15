import config
import scipy.stats as stats
from scipy.stats import t

def mean_amplitude(evoked, roi, tmin, tmax):
    evoked_roi = evoked.copy().pick_channels(roi)
    evoked_crop = evoked_roi.crop(tmin=tmin, tmax=tmax)
    return evoked_crop.data.mean()

def erp_to_amplitude(evoked_front_sym, evoked_pers_sym, evoked_front_asym, evoked_pers_asym):
    roi = config.posterior_channels
    tmin = config.tmin_spn
    tmax = config.tmax_spn

    front_sym_val = mean_amplitude(evoked_front_sym, roi, tmin, tmax)
    pers_sym_val = mean_amplitude(evoked_pers_sym, roi, tmin, tmax)

    front_asym_val = mean_amplitude(evoked_front_asym, roi, tmin, tmax)
    pers_asym_val = mean_amplitude(evoked_pers_asym, roi, tmin, tmax)

    return (front_sym_val, pers_sym_val, front_asym_val, pers_asym_val)


def additional_t_test(pers_val, front_val, symasym):
    res= stats.ttest_rel(pers_val, front_val)
    print(f"{symasym}: t={res.statistic}, p={res.pvalue}")