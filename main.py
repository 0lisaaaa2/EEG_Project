from config import subjects, tasks
import config
import mne
import matplotlib.pyplot as plt
from collections import defaultdict
import s_00_fetch_data, s_01_filter, s_02_downsample, s_03_data_annotation, s_05_ica, s_06_interpolation, s_04_rereference, s_07_epochs, s_08_erp, s_09_spn, s_10_cost, s_11_grand

if __name__ == "__main__":

    spn_results = {}

    grand_spns = defaultdict(list)   # keys: task, values: list of Evoked
    grand_erps = defaultdict(list)   # keys: task, values: list of Evoked
    grand_costs = []                # list of perspective cost Evokeds
    grand_cost_amps = []

    for subject in subjects:
        for task in tasks:
            #get raw data and plot
            raw = s_00_fetch_data.load_data(subject, task)
            raw.plot(block=True, scalings=40e-6, title='Raw Data')

            #resample and plot
            resample_raw = s_02_downsample.downsample_data(raw, config.sample_rate)
            resample_raw.plot(block=True, scalings=40e-6, title='Data after Resampling')

            #filter and plot
            filter_raw = s_01_filter.filter(resample_raw)
            filter_raw.plot(block=True, scalings=40e-6,  title='Data after Filtering')

            # data annotation of bad channels and bad segmetns and plot
            s_03_data_annotation.remove_bad_channels(filter_raw, subject, task)
            #s_03_data_annotation.detect_bad_channels(filter_raw)
            #s_03_data_annotation.detect_bad_annotationa(filter_raw)
            filter_raw.plot(block=True, scalings=40e-6, title='Data after After Annotation (No Change!)')

            # # rereferencing and plot -> move before ica
            reref_raw = s_04_rereference.rereferencing(filter_raw)
            reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

            #ica and plot
            clean_raw = s_05_ica.ica(reref_raw)
            clean_raw.plot(block=True, scalings=40e-6, title='Data after ICA Cleaning')

            # interpolation of bad and plot
            inter_raw = s_06_interpolation.interpolate_bad_channels(clean_raw)
            inter_raw.plot(block=True, scalings=40e-6, title='Data after Interpolation of Bad Channels')

            # # rereferencing and plot -> move before ica
            # reref_raw = s_06_rereference.rereferencing(inter_raw)
            # reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

            # epoching and plot
            epochs = s_07_epochs.epoching(inter_raw)

            # erp and baseline correct and plot
            erp_sym, erp_asym = s_08_erp.compute_erp_all(epochs)

            # spn
            spn, spn_amplitude = s_09_spn.compute_spn_posterior(erp_sym, erp_asym)
            spn_results[(subject, task)] = (spn, spn_amplitude)
            grand_spns[task].append(spn)
            grand_erps[task].append([erp_sym, erp_asym])

        # perspective cost
        spn_front, spn_front_amp = spn_results[(subject, 'regfront')]
        spn_persp, spn_persp_amp = spn_results[(subject, 'regperp')]

        perspective_cost_spn = s_10_cost.comput_perspective_cost_spn(spn_front, spn_persp)
        perspective_cost_amp = s_10_cost.comput_perspective_cost_amp(spn_front_amp, spn_persp_amp)

        # store for grand average
        grand_costs.append(perspective_cost_spn)
        grand_cost_amps.append(perspective_cost_amp)

        s_10_cost.plot_spns_vs_pc(spn_front, spn_persp, perspective_cost_spn)
        print(f"Subject {subject} - Perspective Cost SPN Amplitude: {perspective_cost_amp}")


    print("\nComputing grand averages...")

    # Grand average SPN per task
    grand_avg_spn_front = mne.grand_average(grand_spns['regfront'])
    grand_avg_spn_persp = mne.grand_average(grand_spns['regperp'])

     # grand average over erps per task
    grand_avg_erp_front_sym = mne.grand_average([e[0] for e in grand_erps['regfront']])
    grand_avg_erp_front_asym = mne.grand_average([e[1] for e in grand_erps['regfront']])

    grand_avg_erp_persp_sym = mne.grand_average([e[0] for e in grand_erps['regperp']])
    grand_avg_erp_persp_asym = mne.grand_average([e[1] for e in grand_erps['regperp']])

    # Grand average perspective cost
    grand_avg_cost = mne.grand_average(grand_costs)

    # Mean amplitude across subjects ??????
    mean_cost_amp = sum(grand_cost_amps) / len(grand_cost_amps)

    print(f"\nGrand-average Perspective Cost Amplitude: {mean_cost_amp * 1e6:.2f} µV")

    # # Plot grand-average SPNs
    # mne.viz.plot_compare_evokeds(
    #     {"Frontoparallel": grand_avg_spn_front,
    #     "Perspective": grand_avg_spn_persp},
    #     combine="mean",
    #     title="Grand Average SPN (Posterior Cluster)"
    # )


    # 1) ERP vs SPN — Frontoparallel
    s_11_grand.plot_spn_vs_erps(
        erp_sym=grand_avg_erp_front_sym,
        erp_asym=grand_avg_erp_front_asym,
        spn=grand_avg_spn_front
    )

    # 2) ERP vs SPN — Perspective
    s_11_grand.plot_spn_vs_erps(
        erp_sym=grand_avg_erp_persp_sym,
        erp_asym=grand_avg_erp_persp_asym,
        spn=grand_avg_spn_persp
    )

    # 3) SPNs vs Perspective Cost
    s_11_grand.plot_spns_vs_pc(
        spn_front=grand_avg_spn_front,
        spn_persp=grand_avg_spn_persp,
        perspective_cost=grand_avg_cost
    )

    

