import mne
import config

"""
authors only calculate spn for posterior electrode cluster
-> where SPN is expected to be most pronounced

for erp, include all electrodes, restrict only in spn calculation

"""


def compute_erp_all(epochs):

    print("Amount of epochs:", len(epochs['SYM'].events), len(epochs['ASYM'].events)) #len(Epochs.events)


    baseline = (config.tmin_baseline, config.tmax_baseline)
    erp_sym = epochs['SYM'].average().apply_baseline(baseline)
    erp_asym = epochs['ASYM'].average().apply_baseline(baseline)

    # visualize ERPs
    #plot_erps(erp_sym, erp_asym)

    # visualize ERPs for a specific channel, e.g., 'Cz'
    plot_erps_channel(erp_sym, erp_asym, channel_name='Cz')

    # butterfly plot for SYM condition
    plot_butterfly(erp_sym, title="Butterfly Plot - SYM condition")

    return erp_sym, erp_asym



# Compare ERPs for SYM and ASYM conditions
# not a helpful visualization, ignore for now
def plot_erps(erp_sym, erp_asym, picks="eeg"):
    mne.viz.plot_compare_evokeds(
        {"SYM": erp_sym, "ASYM": erp_asym},
        picks=picks,
        combine="mean",   # average across channels
        colors={"SYM": "tab:blue", "ASYM": "tab:orange"},
        title="ERP comparison (SYM vs ASYM)"
    )

# Compre ERPs for a specific channel
def plot_erps_channel(erp_sym, erp_asym, channel_name):
    mne.viz.plot_compare_evokeds(
        {"SYM": erp_sym, "ASYM": erp_asym},
        picks=[channel_name],
        combine=None,   # do not average across channels
        colors={"SYM": "tab:blue", "ASYM": "tab:orange"},
        title=f"ERP comparison at channel {channel_name} (SYM vs ASYM)"
    )

# Butterfly plot
def plot_butterfly(erp, title="Butterfly Plot"):
    erp.plot(
        spatial_colors=True,
        titles=title,
        show=True
    )


