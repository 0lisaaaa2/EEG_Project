import mne
import matplotlib.pyplot as plt
import config
import numpy as np

# Compute grand averages 

def compute_grand_erp(grand_erps):
    grand_avg_erp_front_sym = mne.grand_average([e[0] for e in grand_erps['regfront']])
    grand_avg_erp_front_asym = mne.grand_average([e[1] for e in grand_erps['regfront']])

    grand_avg_erp_persp_sym = mne.grand_average([e[0] for e in grand_erps['regperp']])
    grand_avg_erp_persp_asym = mne.grand_average([e[1] for e in grand_erps['regperp']])

    return grand_avg_erp_front_sym, grand_avg_erp_front_asym, grand_avg_erp_persp_sym, grand_avg_erp_persp_asym

def compute_grand_spn(grand_spns):
    grand_avg_spn_front = mne.grand_average(grand_spns['regfront'])
    grand_avg_spn_persp = mne.grand_average(grand_spns['regperp'])

    return grand_avg_spn_front, grand_avg_spn_persp

def compute_grand_cost(grand_costs):
    grand_avg_cost = mne.grand_average(grand_costs)
    return grand_avg_cost

def compute_grand_amps(grand_cost_amps, grand_spn_amps):
    grand_avg_cost_amp = np.mean(grand_cost_amps)
    grand_avg_spn_front_amp = np.mean(grand_spn_amps['regfront'])
    grand_avg_spn_persp_amp = np.mean(grand_spn_amps['regperp'])

    return grand_avg_cost_amp, grand_avg_spn_front_amp, grand_avg_spn_persp_amp


# Plots

# plot spn vs erps in one plot
def plot_spn_vs_erps(erp_sym, erp_asym, spn, posterior_channels=config.posterior_channels):

    # Pick same posterior channels from all evokeds
    erp_sym_post = erp_sym.copy().pick_channels(posterior_channels)
    erp_asym_post = erp_asym.copy().pick_channels(posterior_channels)
    spn_post = spn.copy().pick_channels(posterior_channels)

    mne.viz.plot_compare_evokeds(
        {
            "Symmetry": erp_sym_post,
            "Asymmetry": erp_asym_post,
            "SPN (Sym − Asym)": spn_post,
        },
        combine="mean",
        colors={
            "Symmetry": "purple",
            "Asymmetry": "green",
            "SPN (Sym − Asym)": "gray",
        },
        title="Posterior cluster ERPs and SPN",
        ci=False,
        ylim=dict(eeg=(-10, 10))
    )


# spns vs perspective cost
def plot_spns_vs_pc(spn_front, spn_persp, perspective_cost, posterior_channels=config.posterior_channels):

    spn_front_post = spn_front.copy().pick_channels(posterior_channels)
    spn_persp_post = spn_persp.copy().pick_channels(posterior_channels)
    perspective_cost_post = perspective_cost.copy().pick_channels(posterior_channels)

    mne.viz.plot_compare_evokeds(
        {
            "Frontoparallel Condition": spn_front_post,
            "Perspective Condition": spn_persp_post,
            "Perspective Cost (SPN_front - SPN_persp)": perspective_cost_post,
        },
        combine="mean",
        colors={
            "Frontoparallel Condition": "black",
            "Perspective Condition": "gray",
            "Perspective Cost (SPN_front - SPN_persp)": "red",
        },
        title="SPNs and Perspective Cost (Posterior Cluster)",
        ci=False
    )

# amplitude bar chart
def plot_spn_amplitude(grand_avg_cost, grand_avg_front, grand_avg_perp):
    labels = ['Frontoparallel', 'Perspective', 'Perspective Cost']
    means = [grand_avg_front * 1e6, grand_avg_perp * 1e6, grand_avg_cost * 1e6]  # convert to µV

    plt.figure(figsize=(8, 6))
    plt.bar(labels, means, color=['black', 'gray', 'red'])

    # horizontal zero line
    plt.axhline(0, linestyle='--', linewidth=1)

    plt.ylabel('SPN Amplitude (miroVolts)')
    plt.title('Average SPN Amplitudes Across All Subjects')
    plt.tight_layout
    plt.show()

def topo_data(evoked, tmin=0.3, tmax=0.6):
    ev = evoked.copy().crop(tmin, tmax)
    data = ev.data.mean(axis=1)
    sd = np.std(data)
    return data * 1e6, sd * 1e6

def plot_topography(spn_front, spn_persp, perspective_cost):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3))
    plt.subplots_adjust(wspace=0.4)

    evokeds = [
        spn_front,
        spn_persp,
        perspective_cost
    ]

    titles = ["Frontoparallel", "Perspective", "Cost"]
    vlim = (-3, 1)  # µV – einheitlich!

    for ax, evk, title in zip(axes, evokeds, titles):
        data, sd = topo_data(evk)

        im, _ = mne.viz.plot_topomap(
            data,
            evk.info,
            axes=ax,
            cmap='viridis',
            vlim=vlim,
            contours=0,
            show=False
        )

        ax.set_title(f"{title}\nSD = {sd:.3f}", fontsize=10)

    # Trennlinie vor Cost
    fig.add_artist(plt.Line2D(
        [0.67, 0.67], [0.15, 0.85],
        transform=fig.transFigure,
        color='black', linewidth=2
    ))

    # Farbskala
    cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    plt.colorbar(im, cax=cax, label="Amplitude in µV")

    plt.show()