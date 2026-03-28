import mne
import config


"""
Compute SPN as difference wave (SYM - ASYM) for posterior cluster only, and extract SPN amplitude.
"""


# compute SPN for posterior cluster only
def compute_spn_posterior(erp_sym, erp_asym):
    erp_sym_post = erp_sym.copy().pick_channels(config.posterior_channels)
    erp_asym_post = erp_asym.copy().pick_channels(config.posterior_channels)

    # compute SPN (SYM - ASYM)
    spn = mne.combine_evoked([erp_sym_post, erp_asym_post], weights=[1, -1])

    # uncomment to visualize SPN
    #plot_spn_vs_erps(erp_sym_post, erp_asym_post, spn, posterior_channels=config.posterior_channels)
    
    spn_amplitude = extract_spn_amplitude(spn)

    return spn, spn_amplitude


# calculate average spn amplitude in defined time window
def extract_spn_amplitude(spn):
    tmin_spn = config.tmin_spn
    tmax_spn = config.tmax_spn

    spn_amplitude = spn.copy().crop(tmin=tmin_spn, tmax=tmax_spn).data.mean(axis=1).mean(axis=0) # average across times, then across electrodes

    #print(f"SPN Amplitude ({tmin_spn}s to {tmax_spn}s): {spn_amplitude * 1e6:.2f} µV")

    return spn_amplitude


# plot spn vs erps in one plot
def plot_spn_vs_erps(erp_sym, erp_asym, spn, posterior_channels=config.posterior_channels):

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