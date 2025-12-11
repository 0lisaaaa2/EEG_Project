from config import subjects, tasks
import s_00_fetch_data
import config
import s_00_fetch_data, s_01_filter, s_02_downsample, s_03_remove_bad_channels, s_04_ica
import matplotlib.pyplot as plt


if __name__ == "__main__":
    for subject in subjects:
        for task in tasks:
            #get raw data and plot
            raw = s_00_fetch_data.load_data(subject, task)
            raw.plot(block=True, scalings=40e-6)

            #resample and plot
            resample_raw = s_02_downsample.downsample_data(raw, config.sample_rate)
            resample_raw.plot(block=True, scalings=40e-6)

            #filter and plot
            filter_raw = s_01_filter.filter(resample_raw)
            filter_raw.plot(block=True, scalings=40e-6)

            #bad channels
            #raw.info["bads"] = s_03_remove_bad_channels.auto_find_bad_channels(raw)
            #raw.info["bads"] = ["Fz", "PO4", "CP6"]
            #raw.plot(block=True, scalings=40e-6)

            #ica and plot
            clean_raw = s_04_ica.ica(filter_raw)
            clean_raw.plot(block=True, scalings=40e-6)