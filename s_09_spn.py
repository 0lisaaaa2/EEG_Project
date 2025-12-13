import mne
import config

"""
authors only calculate spn for posterior electrode cluster
-> where SPN is expected to be most pronounced

for erp, include all electrodes, restrict only in spn calculation

"""

# alrady focus on posterior cluster in spn calculation?

# defined in paper
left_post = ["P3", "P5", "P7", "P9", "PO7", "PO3", "O1"]
right_post = ["P4", "P6", "P8", "P10", "PO8", "PO4", "O2"]
posterior_channels = left_post + right_post

# not sure if calculate spn for all channels or only posterior?
def compute_spn_all(erp_sym, erp_asym):

    # compute SPN as difference wave (SYM - ASYM)
    spn = mne.combine_evoked([erp_sym, erp_asym], weights=[1, -1])


    # visualize SPN

    return spn


def compute_spn_posterior(erp_sym, erp_asym):
    # pick only posterior channels
    erp_sym_post = erp_sym.copy().pick_channels(posterior_channels)
    erp_asym_post = erp_asym.copy().pick_channels(posterior_channels)

    # compute SPN (SYM - ASYM)
    spn = mne.combine_evoked([erp_sym_post, erp_asym_post], weights=[1, -1])

    # visualize SPN
    plot_spn_vs_erps(erp_sym_post, erp_asym_post, spn, posterior_channels=posterior_channels)
    

    spn_amplitude = extract_spn_amplitude(spn)

    return spn, spn_amplitude

def extract_spn_amplitude(spn):
    # define time window for SPN measurement
    tmin_spn = config.tmin_spn
    tmax_spn = config.tmax_spn

    # extract mean amplitude in the defined time window
    spn_amplitude = spn.copy().crop(tmin=tmin_spn, tmax=tmax_spn).data.mean(axis=1).mean(axis=0) # average across times, then across electrodes

    print(f"SPN Amplitude ({tmin_spn}s to {tmax_spn}s): {spn_amplitude * 1e6:.2f} µV")

    return spn_amplitude


# plot spn vs erps in one plot
def plot_spn_vs_erps(erp_sym, erp_asym, spn, posterior_channels=posterior_channels):

    mne.viz.plot_compare_evokeds(
        {
            "Symmetry": erp_sym,
            "Asymmetry": erp_asym,
            "SPN (Sym − Asym)": spn,
        },
        picks=posterior_channels,
        combine="mean",
        colors={
            "Symmetry": "purple",
            "Asymmetry": "green",
            "SPN (Sym − Asym)": "gray",
        },
        title="Posterior cluster ERPs and SPN",
        ci=False
    )