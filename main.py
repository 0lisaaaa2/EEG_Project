from config import subjects, tasks
import config
import s_00_fetch_data, s_01_filter, s_02_downsample, s_03_data_annotation, s_04_ica, s_05_interpolation, s_06_rereference, s_07_epochs, s_08_erp, s_09_spn, s_10_cost

if __name__ == "__main__":

    spn_results = {}

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
            filter_raw.plot(block=True, scalings=40e-6, title='Data after After Annotation (No Change!)')

            # rereferencing and plot
            reref_raw = s_06_rereference.rereferencing(filter_raw)
            reref_raw.plot(block=True, scalings=40e-6, title='Data after Rereferencing')

            #ica and plot
            clean_raw = s_04_ica.ica(reref_raw)
            clean_raw.plot(block=True, scalings=40e-6, title='Data after ICA Cleaning')

            # interpolation of bad and plot
            inter_raw = s_05_interpolation.interpolate_bad_channels(clean_raw)
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

        # perspective cost
        spn_front, spn_front_amp = spn_results[(subject, 'regfront')]
        spn_persp, spn_persp_amp = spn_results[(subject, 'regperp')]

        perspective_cost_spn = s_10_cost.comput_perspective_cost_spn(spn_front, spn_persp)
        perspective_cost_amp = s_10_cost.comput_perspective_cost_amp(spn_front_amp, spn_persp_amp)

        s_10_cost.plot_spns_vs_pc(spn_front, spn_persp, perspective_cost_spn)
        print(f"Subject {subject} - Perspective Cost SPN Amplitude: {perspective_cost_amp}")

