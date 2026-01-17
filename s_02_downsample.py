import matplotlib.pyplot as plt

# downsample to given new sampling frequency new_sfreq
def downsample_data(raw, new_sfreq):
    
    raw_resampled = raw.copy().resample(sfreq=new_sfreq)

    print(f"Original sampling frequency: {raw.info['sfreq']} Hz")
    print(f"Resampled frequency: {raw_resampled.info['sfreq']} Hz")

    # visualize difference
    #plot_raw_downsampling(raw, raw_resampled, ch_name='Cz')

    return raw_resampled


# plot the difference for a short segment for a specific channel
# visualize difference before and after downsampling
# duration = seconds of data to visualize
# start_time = where to start the segment
def plot_raw_downsampling(raw, raw_resampled, ch_name=None, duration=0.5, start_time=0.0):
 
    sfreq_orig = raw.info["sfreq"]
    n_orig = int(duration * sfreq_orig)

    start_sample_orig = int(start_time * sfreq_orig)
    stop_sample_orig = start_sample_orig + n_orig

    data_orig, times_orig = raw[ch_name, start_sample_orig:stop_sample_orig]

    sfreq_res = raw_resampled.info["sfreq"]
    n_res = int(duration * sfreq_res)

    start_sample_res = int(start_time * sfreq_res)
    stop_sample_res = start_sample_res + n_res

    data_res, times_res = raw_resampled[ch_name, start_sample_res:stop_sample_res]

    #plt.figure(figsize=(8, 3))
    #plt.plot(times_orig, data_orig[0], color='blue', label="Original")
    #plt.plot(times_res, data_res[0], '-o', color='orange', label="Downsampled")

    #plt.xlabel("Time (s)")
    #plt.ylabel("Amplitude (µV)")
    #plt.title(f"Downsampling at Channel {ch_name}")
    #plt.legend()
    #plt.tight_layout()
    #plt.show()
