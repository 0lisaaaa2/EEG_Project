import mne
import matplotlib.pyplot as plt
import config


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
        ci=False
    )



# spns vs perspective cost
# def plot_spns_vs_pc(spn_front, spn_persp, perspective_cost):

#     mne.viz.plot_compare_evokeds(
#         {
#             "Frontoparallel Condition": spn_front,
#             "Perspective Condition": spn_persp,
#             "Perspective Cost (SPN_front - SPN_persp)": perspective_cost,
#         },
#         combine="mean",
#         colors={
#             "Frontoparallel Condition": "black",
#             "Perspective Condition": "gray",
#             "Perspective Cost (SPN_front - SPN_persp)": "red",
#         },
#         title="SPNs and Perspective Cost",
#         ci=False
#     )
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
