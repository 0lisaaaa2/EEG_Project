from config import subjects, tasks
import config
from collections import defaultdict
import mne
import s_00_fetch_data, s_01_downsample, s_02_filter, s_03_data_annotation, s_05_ica, s_06_interpolation, s_04_rereference, s_07_epochs, s_08_erp, s_09_spn, s_10_cost, s_11_grand, s_12_timefreq, s_13_stat, s_14_additional_stat

def main_pipeline():
    # storage for results
    spn_results = {}

    grand_erps = defaultdict(list) 
    grand_spns = defaultdict(list) 
    grand_tfrs = defaultdict(list) 

    grand_costs = []  
    grand_cost_amps = []
    grand_spn_amps = defaultdict(list)  

    rejected_components={}
    rejected_trials={}

    erp_data = {}
    amplitudes_front_sym = []
    amplitudes_persp_sym = []
    amplitudes_front_asym = []
    amplitudes_persp_asym = []

    # loop through subjects and tasks
    for subject in subjects:

        print("#########################################################################################################################################################")
        print("Start Processing Subject", subject)

        rejected_components[subject] = {}
        rejected_trials[subject] = {}
        erp_data[subject] = {}

        for task in tasks:

            # get raw data
            raw = s_00_fetch_data.load_data(subject, task)
            # raw.plot(block=True, scalings=40e-6, title='Raw Data')

            # resampling
            resample_raw = s_01_downsample.downsample_data(raw, config.sample_rate)
            # resample_raw.plot(block=True, scalings=40e-6, title='Data after Resampling')

            # apply filters
            filter_raw = s_02_filter.filter(resample_raw)
            # filter_raw.plot(block=True, scalings=40e-6,  title='Data after Filtering')

            # data annotation of bad channels and bad segmetns and plot
            # detect and annotate bad channels and segments
            # s_03_data_annotation.remove_bad_channels(filter_raw, subject, task)
            # s_03_data_annotation.detect_bad_channels(filter_raw)
            # s_03_data_annotation.detect_bad_annotationa(filter_raw)
            # filter_raw.plot(block=True, scalings=40e-6, title='Data after After Annotation (No Change!)')

            # # rereferencing
            reref_raw = s_04_rereference.rereferencing(filter_raw)
            # reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

            # apply ica
            clean_raw, n_excluded = s_05_ica.ica(reref_raw)
            rejected_components[subject][task]=n_excluded # track number of rejected components per subject and task
            # clean_raw.plot(block=True, scalings=40e-6, title='Data after ICA Cleaning')

            # interpolation of bad channels 
            inter_raw = s_06_interpolation.interpolate_bad_channels(clean_raw)
            # inter_raw.plot(block=True, scalings=40e-6, title='Data after Interpolation of Bad Channels')

            # epoching the data
            epochs = s_07_epochs.epoching(inter_raw)

            # compute erps for all electrodes 
            erp_sym, erp_asym = s_08_erp.compute_erp_all(epochs)
            # save erps for statistical analysis later on (further analysis)
            if task == "regfront":
                erp_data[subject]["front"] = {"sym": erp_sym, "asym": erp_asym}
            if task == "regperp":
                erp_data[subject]["pers"] = {"sym": erp_sym, "asym": erp_asym}

            # time frequency analysis (further analysis)
            tfr_sym = s_12_timefreq.compute_tfr(epochs, "SYM")
            tfr_asym = s_12_timefreq.compute_tfr(epochs, "ASYM")
            tfr_spn = tfr_sym.copy()
            tfr_spn.data = tfr_sym.data - tfr_asym.data

            grand_tfrs[f"{task}_SYM"].append(tfr_sym)
            grand_tfrs[f"{task}_ASYM"].append(tfr_asym)
            grand_tfrs[f"{task}_SPN"].append(tfr_spn)

            # uncomment to visualize time-frequency results for each subject and task (usually not of interest)
            # s_12_timefreq.plot_tfr(tfr_sym, "SYM — Posterior Time-Frequency")
            # s_12_timefreq.plot_tfr(tfr_asym, "ASYM — Posterior Time-Frequency")
            # s_12_timefreq.plot_tfr(tfr_spn, "SPN (SYM − ASYM) — Time-Frequency")

            # compute spn as difference wave of erps and extract spn amplitude
            spn, spn_amplitude = s_09_spn.compute_spn_posterior(erp_sym, erp_asym)
            spn_results[(subject, task)] = (spn, spn_amplitude)
            grand_spns[task].append(spn)
            grand_erps[task].append([erp_sym, erp_asym])

        # calculate perspective cost
        spn_front, spn_front_amp = spn_results[(subject, 'regfront')]
        spn_persp, spn_persp_amp = spn_results[(subject, 'regperp')]

        perspective_cost_spn = s_10_cost.comput_perspective_cost_spn(spn_front, spn_persp)
        perspective_cost_amp = s_10_cost.comput_perspective_cost_amp(spn_front_amp, spn_persp_amp)

        grand_costs.append(perspective_cost_spn)
        grand_cost_amps.append(perspective_cost_amp)
        grand_spn_amps['regfront'].append(spn_front_amp)
        grand_spn_amps['regperp'].append(spn_persp_amp)

        # uncomment to visualize spn vs perspective cost for each subject (usually not of interest)
        # s_10_cost.plot_spns_vs_pc(spn_front, spn_persp, perspective_cost_spn)
        # print(f"Subject {subject} - Perspective Cost SPN Amplitude: {perspective_cost_amp}")

        # For additional statistical tests (further analysis)
        evoked_front_sym = erp_data[subject]["front"]["sym"]
        evoked_pers_sym = erp_data[subject]["pers"]["sym"]
        evoked_front_asym = erp_data[subject]["front"]["asym"]
        evoked_pers_asym = erp_data[subject]["pers"]["asym"]

        front_sym_val, pers_sym_val, front_asym_val, pers_asym_val = s_14_additional_stat.erp_to_amplitude(evoked_front_sym, evoked_pers_sym, evoked_front_asym, evoked_pers_asym)
        amplitudes_front_sym.append(front_sym_val)
        amplitudes_persp_sym.append(pers_sym_val)
        amplitudes_front_asym.append(front_asym_val)
        amplitudes_persp_asym.append(pers_asym_val)


    print("#########################################################################################################################################################")
    print("ICA rejected components:", rejected_components)
    print("\nComputing Grand Averages...")

    # grand average over erps per task
    grand_avg_erp_front_sym, grand_avg_erp_front_asym, grand_avg_erp_persp_sym, grand_avg_erp_persp_asym = s_11_grand.compute_grand_erp(grand_erps)

    # grand average SPN per task
    grand_avg_spn_front, grand_avg_spn_persp = s_11_grand.compute_grand_spn(grand_spns)

    # grand average perspective cost
    grand_avg_cost = s_11_grand.compute_grand_cost(grand_costs)

    # grand average amplitudes
    grand_avg_cost_amp, grand_avg_spn_front_amp, grand_avg_spn_persp_amp = s_11_grand.compute_grand_amps(grand_cost_amps, grand_spn_amps)

    print(f"Averaged amplitudes across all subjects: \n Frontoparallel: {grand_avg_spn_front_amp} \n Perspective: {grand_avg_spn_persp_amp} \n Perspective Cost: {grand_avg_cost_amp}")


    ############ Plotting Results + Calculating Stastics :)

    # ERP vs SPN — Frontoparallel
    s_11_grand.plot_spn_vs_erps(erp_sym=grand_avg_erp_front_sym, erp_asym=grand_avg_erp_front_asym, spn=grand_avg_spn_front)

    # ERP vs SPN — Perspective
    s_11_grand.plot_spn_vs_erps(erp_sym=grand_avg_erp_persp_sym, erp_asym=grand_avg_erp_persp_asym, spn=grand_avg_spn_persp)

    # SPNs vs Perspective Cost
    s_11_grand.plot_spns_vs_pc(spn_front=grand_avg_spn_front, spn_persp=grand_avg_spn_persp, perspective_cost=grand_avg_cost)

    # Topography of SPNs and Perspective Cost
    s_11_grand.plot_topography(spn_front=grand_avg_spn_front, spn_persp=grand_avg_spn_persp, perspective_cost=grand_avg_cost)
    
    # Plotting average SPN amplitudes and Perspective Cost amplitude
    s_13_stat.plot_spn_amplitude(grand_avg_cost_amp, grand_avg_spn_front_amp, grand_avg_spn_persp_amp, grand_cost_amps, grand_spn_amps['regfront'], grand_spn_amps['regperp'], alpha=0.02)
    
    # Calculate Statistics
    s_13_stat.run_statistics(spn_front_values=grand_spn_amps['regfront'], perspective_cost_values=grand_cost_amps, alpha=0.02)
    

    ############ Further Analysis - Additional Statistical Tests for ERPs + Time Frequency Analysis

    #  Additional Statistical Tests
    s_14_additional_stat.additional_t_test(amplitudes_persp_sym, amplitudes_front_sym, "sym")
    s_14_additional_stat.additional_t_test(amplitudes_persp_asym, amplitudes_front_asym, "asym")
    
    
    # Time-Frequency Analysis
    grand_avg_tfrs = {}
    for cond, tfr_list in grand_tfrs.items():
        grand_avg_tfrs[cond] = mne.grand_average(tfr_list)

    # Plot grand averages for both spn conditions and their difference
    s_12_timefreq.plot_tfr(grand_avg_tfrs["regfront_SPN"], "Grand Avg SPN Front", vmin=-0.04, vmax=0.04)
    s_12_timefreq.plot_tfr(grand_avg_tfrs["regperp_SPN"], "Grand Avg SPN Perspective", vmin=-0.04, vmax=0.04)
    tfr_diff = grand_avg_tfrs["regfront_SPN"].copy()
    tfr_diff.data = grand_avg_tfrs["regfront_SPN"].data - grand_avg_tfrs["regperp_SPN"].data
    s_12_timefreq.plot_tfr(tfr_diff, "Grand Avg SPN Difference", vmin=-0.04, vmax=0.04)

    # calculate effect size in alpha band
    s_12_timefreq.calculate_effect_size(grand_tfrs["regfront_SPN"], grand_tfrs["regperp_SPN"])
    #s_12_timefreq.run_statistics_tfr(grand_tfrs["regfront_SPN"], grand_tfrs["regperp_SPN"], alpha=0.05, n_perm=1000)






# def alternative_testing_pipeline():
#     erp_data = {}
#     amplitudes_front_sym = []
#     amplitudes_persp_sym = []
#     amplitudes_front_asym = []
#     amplitudes_persp_asym = []

#     for subject in subjects:
#         print("#######################################################################")
#         print("start subject", subject)
#         erp_data[subject] = {}
#         for task in tasks:
#             # get raw data and plot
#             raw = s_00_fetch_data.load_data(subject, task)
#             # raw.plot(block=True, scalings=40e-6, title='Raw Data')

#             # resample and plot
#             resample_raw = s_01_downsample.downsample_data(raw, config.sample_rate)
#             # resample_raw.plot(block=True, scalings=40e-6, title='Data after Resampling')

#             # filter and plot
#             filter_raw = s_02_filter.filter(resample_raw)
#             # filter_raw.plot(block=True, scalings=40e-6,  title='Data after Filtering')

#             # data annotation of bad channels and bad segmetns and plot
#             # s_03_data_annotation.remove_bad_channels(filter_raw, subject, task)
#             # s_03_data_annotation.detect_bad_channels(filter_raw)
#             # s_03_data_annotation.detect_bad_annotationa(filter_raw)
#             # filter_raw.plot(block=True, scalings=40e-6, title='Data after After Annotation (No Change!)')

#             # # rereferencing and plot -> move before ica
#             reref_raw = s_04_rereference.rereferencing(filter_raw)
#             # reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

#             # ica and plot
#             clean_raw = s_05_ica.ica(reref_raw)
#             # clean_raw.plot(block=True, scalings=40e-6, title='Data after ICA Cleaning')

#             # interpolation of bad and plot
#             inter_raw = s_06_interpolation.interpolate_bad_channels(clean_raw)
#             # inter_raw.plot(block=True, scalings=40e-6, title='Data after Interpolation of Bad Channels')

#             # # rereferencing and plot -> move before ica
#             # reref_raw = s_06_rereference.rereferencing(inter_raw)
#             # reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

#             # epoching and plot
#             epochs = s_07_epochs.epoching(inter_raw)

#             # erp and baseline correct and plot
#             erp_sym, erp_asym = s_08_erp.compute_erp_all(epochs)

#             # Für additional statistische tests
#             if task == "regfront":
#                 erp_data[subject]["front"] = {
#                     "sym": erp_sym,
#                     "asym": erp_asym
#                 }
#             if task == "regperp":
#                 erp_data[subject]["pers"] = {
#                     "sym": erp_sym,
#                     "asym": erp_asym
#                 }

#         evoked_front_sym = erp_data[subject]["front"]["sym"]
#         evoked_pers_sym = erp_data[subject]["pers"]["sym"]
#         evoked_front_asym = erp_data[subject]["front"]["asym"]
#         evoked_pers_asym = erp_data[subject]["pers"]["asym"]

#         front_sym_val, pers_sym_val, front_asym_val, pers_asym_val = s_14_additional_stat.erp_to_amplitude(evoked_front_sym, evoked_pers_sym, evoked_front_asym, evoked_pers_asym)
#         amplitudes_front_sym.append(front_sym_val)
#         amplitudes_persp_sym.append(pers_sym_val)
#         amplitudes_front_asym.append(front_asym_val)
#         amplitudes_persp_asym.append(pers_asym_val)


#     s_14_additional_stat.additional_t_test(amplitudes_persp_sym, amplitudes_front_sym, "sym")
#     s_14_additional_stat.additional_t_test(amplitudes_persp_asym, amplitudes_front_asym, "asym")


if __name__ == "__main__":
    main_pipeline()