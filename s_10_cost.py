import mne
import config

# compute perspective cost as amplitude difference
def comput_perspective_cost_amp(spn_front_amp, spn_persp_amp):
    return spn_front_amp - spn_persp_amp

# compute perspective cost as difference wave
def comput_perspective_cost_spn(spn_front, spn_persp):
    return mne.combine_evoked([spn_front, spn_persp], weights=[1, -1])

def plot_spns_vs_pc(spn_front, spn_persp, perspective_cost):

    mne.viz.plot_compare_evokeds(
        {
            "Frontoparallel Condition": spn_front,
            "Perspective Condition": spn_persp,
            "Perspective Cost (SPN_front - SPN_persp)": perspective_cost,
        },
        combine="mean",
        colors={
            "Frontoparallel Condition": "black",
            "Perspective Condition": "gray",
            "Perspective Cost (SPN_front - SPN_persp)": "red",
        },
        title="SPNs and Perspective Cost",
        ci=False
    )