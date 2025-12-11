from config import subjects, tasks
import config
import s_00_fetch_data, s_02_downsample
import matplotlib.pyplot as plt

if __name__ == "__main__":
    for subject in subjects:
        for task in tasks:
            raw = s_00_fetch_data.load_data(subject, task)
            print(raw)
            resample_raw = s_02_downsample.downsample_data(raw, config.sample_rate)
            print("success!")
