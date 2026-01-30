from config import subjects, tasks
import config
from collections import defaultdict
import mne
import s_00_fetch_data, s_01_filter, s_02_downsample, s_03_data_annotation, s_05_ica, s_06_interpolation, s_04_rereference, s_07_epochs, s_08_erp, s_09_spn, s_10_cost, s_11_grand, s_12_timefreq, s_13_stat

if __name__ == "__main__":

    spn_results = {}

    grand_tfrs = defaultdict(list)  # keys: task, values: list of TFRs

    grand_spns = defaultdict(list)   # keys: task, values: list of Evoked
    grand_erps = defaultdict(list)   # keys: task, values: list of Evoked
    grand_costs = []                # list of perspective cost Evokeds
    grand_cost_amps = []
    grand_spn_amps = defaultdict(list)  # keys: task, values: list of SPN amplitudes

    for subject in subjects:
        print("#######################################################################")
        print("start subject", subject)
        for task in tasks:
            #get raw data and plot
            raw = s_00_fetch_data.load_data(subject, task)
            #raw.plot(block=True, scalings=40e-6, title='Raw Data')

            #resample and plot
            resample_raw = s_02_downsample.downsample_data(raw, config.sample_rate)
            #resample_raw.plot(block=True, scalings=40e-6, title='Data after Resampling')

            #filter and plot
            filter_raw = s_01_filter.filter(resample_raw)
            #filter_raw.plot(block=True, scalings=40e-6,  title='Data after Filtering')

            # data annotation of bad channels and bad segmetns and plot
            #s_03_data_annotation.remove_bad_channels(filter_raw, subject, task)
            #s_03_data_annotation.detect_bad_channels(filter_raw)
            #s_03_data_annotation.detect_bad_annotationa(filter_raw)
            #filter_raw.plot(block=True, scalings=40e-6, title='Data after After Annotation (No Change!)')

            # # rereferencing and plot -> move before ica
            reref_raw = s_04_rereference.rereferencing(filter_raw)
            #reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

            #ica and plot
            clean_raw = s_05_ica.ica(reref_raw)
            #clean_raw.plot(block=True, scalings=40e-6, title='Data after ICA Cleaning')

            # interpolation of bad and plot
            inter_raw = s_06_interpolation.interpolate_bad_channels(clean_raw)
            #inter_raw.plot(block=True, scalings=40e-6, title='Data after Interpolation of Bad Channels')

            # # rereferencing and plot -> move before ica
            # reref_raw = s_06_rereference.rereferencing(inter_raw)
            # reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

            # epoching and plot
            epochs = s_07_epochs.epoching(inter_raw)

            # erp and baseline correct and plot
            erp_sym, erp_asym = s_08_erp.compute_erp_all(epochs)

            # time frequency analysis
            tfr_sym = s_12_timefreq.compute_tfr(epochs, "SYM")
            tfr_asym = s_12_timefreq.compute_tfr(epochs, "ASYM")
            tfr_spn = tfr_sym.copy()
            tfr_spn.data = tfr_sym.data - tfr_asym.data

            grand_tfrs[f"{task}_SYM"].append(tfr_sym)
            grand_tfrs[f"{task}_ASYM"].append(tfr_asym)
            grand_tfrs[f"{task}_SPN"].append(tfr_spn)

            # s_12_timefreq.plot_tfr(tfr_sym, "SYM — Posterior Time-Frequency")
            # s_12_timefreq.plot_tfr(tfr_asym, "ASYM — Posterior Time-Frequency")
            # s_12_timefreq.plot_tfr(tfr_spn, "SPN (SYM − ASYM) — Time-Frequency")

            # tfr_sym = s_12_timefreq.compute_tfr_allelectrodes(epochs, "SYM")
            # tfr_asym = s_12_timefreq.compute_tfr_allelectrodes(epochs, "ASYM")


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
        grand_spn_amps['regfront'].append(spn_front_amp)
        grand_spn_amps['regperp'].append(spn_persp_amp)
        
        #s_10_cost.plot_spns_vs_pc(spn_front, spn_persp, perspective_cost_spn)
        print(f"Subject {subject} - Perspective Cost SPN Amplitude: {perspective_cost_amp}")


    print("\nComputing grand averages...")

    # grand average over erps per task
    grand_avg_erp_front_sym, grand_avg_erp_front_asym, grand_avg_erp_persp_sym, grand_avg_erp_persp_asym = s_11_grand.compute_grand_erp(grand_erps)
    
    # Grand average SPN per task
    grand_avg_spn_front, grand_avg_spn_persp = s_11_grand.compute_grand_spn(grand_spns)

    # Grand average perspective cost
    grand_avg_cost = s_11_grand.compute_grand_cost(grand_costs)

    # Average amplitudes
    grand_avg_cost_amp, grand_avg_spn_front_amp, grand_avg_spn_persp_amp = s_11_grand.compute_grand_amps(grand_cost_amps, grand_spn_amps)

    print(f"Averaged amplitudes across all subjects: \n Frontoparallel: {grand_avg_spn_front_amp} \n Perspective: {grand_avg_spn_persp_amp} \n Perspective Cost: {grand_avg_cost_amp}")

    # Average timefrequency data
    grand_avg_tfrs = {}
    for cond, tfr_list in grand_tfrs.items():
        grand_avg_tfrs[cond] = mne.grand_average(tfr_list)

    s_12_timefreq.plot_tfr(grand_avg_tfrs["regfront_SYM"], "Grand Avg SYM Front")
    s_12_timefreq.plot_tfr(grand_avg_tfrs["regfront_ASYM"], "Grand Avg ASYM Front")
    s_12_timefreq.plot_tfr(grand_avg_tfrs["regfront_SPN"], "Grand Avg SPN Front")
    s_12_timefreq.plot_tfr(grand_avg_tfrs["regperp_SPN"], "Grand Avg SPN Perspective")


    # Plotting the results :)

    # ERP vs SPN — Frontoparallel
    s_11_grand.plot_spn_vs_erps(erp_sym=grand_avg_erp_front_sym, erp_asym=grand_avg_erp_front_asym, spn=grand_avg_spn_front)

    # ERP vs SPN — Perspective
    s_11_grand.plot_spn_vs_erps(erp_sym=grand_avg_erp_persp_sym, erp_asym=grand_avg_erp_persp_asym, spn=grand_avg_spn_persp)

    # SPNs vs Perspective Cost
    s_11_grand.plot_spns_vs_pc(spn_front=grand_avg_spn_front, spn_persp=grand_avg_spn_persp, perspective_cost=grand_avg_cost)
    
    s_11_grand.plot_topography(spn_front=grand_avg_spn_front, spn_persp=grand_avg_spn_persp, perspective_cost=grand_avg_cost)

    # Amplitude bar char
    s_11_grand.plot_spn_amplitude(grand_avg_cost_amp, grand_avg_spn_front_amp, grand_avg_spn_persp_amp)

    # Statistics
    s_13_stat.run_statistics(spn_front_values=grand_spn_amps['regfront'], perspective_cost_values=grand_cost_amps, alpha=0.02) # alpha = 0.011?
    s_13_stat.plot_spn_amplitude(grand_avg_cost_amp, grand_avg_spn_front_amp, grand_avg_spn_persp_amp, grand_cost_amps, grand_spn_amps['regfront'], grand_spn_amps['regperp'], alpha=0.02)
    

