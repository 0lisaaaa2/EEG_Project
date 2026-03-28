import mne
import config

"""
Compute ERPs for SYM and ASYM conditions, and visualize them.
"""


# comput erps for all channels, then restrict to posterior only for spn calculation later
def compute_erp_all(epochs):

    print("Amount of epochs:", len(epochs['SYM'].events), len(epochs['ASYM'].events)) 


    baseline = (config.tmin_baseline, config.tmax_baseline)
    erp_sym_all = epochs['SYM'].average().apply_baseline(baseline)
    erp_asym_all = epochs['ASYM'].average().apply_baseline(baseline)

    # uncomment to visualize ERPs for a specific channel, e.g., 'Cz' 
    #plot_erps_channel(erp_sym_all, erp_asym_all, channel_name='PO7')

    # uncomment to visualize butterfly plot for SYM condition
    #plot_butterfly(erp_sym_all, title="Butterfly Plot - SYM condition")

    return erp_sym_all, erp_asym_all


# Compare ERPs for a specific channel
def plot_erps_channel(erp_sym, erp_asym, channel_name):
    mne.viz.plot_compare_evokeds(
        {"SYM": erp_sym, "ASYM": erp_asym},
        picks=[channel_name],
        combine=None,   
        colors={"SYM": "tab:blue", "ASYM": "tab:orange"},
        title=f"ERP comparison at channel {channel_name} (SYM vs ASYM)"
    )

# Butterfly plot -> sanity check: more reaction in posterior channels
def plot_butterfly(erp, title="Butterfly Plot"):
    erp.plot(
        spatial_colors=True,
        titles=title,
        show=True
    )