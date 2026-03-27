import mne
import os
import config
from pyprep.prep_pipeline import PrepPipeline
import matplotlib.pyplot as plt
import numpy as np


def detect_bad_channels(raw):
    #mark exg channels not as eeg
    exg_chs = [ch for ch in raw.ch_names if ch.startswith('EXG')]
    raw.set_channel_types({ch: 'misc' for ch in exg_chs})

    raw_prep = raw.copy().pick_types(eeg=True)
    montage = mne.channels.make_standard_montage('standard_1020')
    prep_params = {
        'ref_chs': 'eeg',
        'reref_chs': 'eeg',
        'line_freqs': [50], #in case there is line noise left
    }
    prep = PrepPipeline(raw_prep, prep_params, montage=montage) #verbose=True prints every step
    prep.fit()

    # noisy: high varianz, unusual spectrum, high line noise, low correlation to neighbors;
    # interpolated: completly flat, very noisy, not mathematically stable
    bad_channels = prep.interpolated_channels + prep.still_noisy_channels
    print("Detected bad channels:", bad_channels)

    raw.info['bads'].extend(bad_channels)
    raw.info['bads'] = list(set(raw.info['bads']))


def detect_bad_annotationa(raw):
    # mark exg channels not as eeg
    exg_chs = [ch for ch in raw.ch_names if ch.startswith('EXG')]
    raw.set_channel_types({ch: 'misc' for ch in exg_chs})

    data = raw.get_data(picks='eeg')
    ptp = np.ptp(data, axis=0)  # peak-to-peak pro Kanal

    # Threshold: 99. Perzentil über Kanäle
    threshold = np.percentile(ptp, 99)

    # Bad-Kanäle / Segmente erkennen
    bad_mask = ptp > threshold

    onsets = raw.times[bad_mask]  # Zeitpunkte der Bad-Samples
    durations = np.repeat(1 / raw.info['sfreq'], len(onsets))  # 1 Sample pro Segment
    description = ['bad_amplitude'] * len(onsets)

    annotations = mne.Annotations(onsets, durations, description)
    raw.set_annotations(annotations)


def remove_bad_channels(raw, subject, task):

    # load existing annotations if any
    load_and_apply_annotations(raw, subject, task)

    #print("Before adding new annotations: ", raw.annotations)

    raw.info['bads'] = config.bads

    # manually annotate data
    #raw.plot(block=True, scalings=40e-6, title='Mark Bad Channels and Annotate Bad Segments - Close Window When Finished!')

    #print(f"Identified bad channels: {raw.info['bads']}")

    # save annotations for future use
    save_bad_annotations(raw, subject, task, overwrite=True)
    
    #print("After adding or not adding new anntotations: ", raw.annotations)
    return None




# path to annotations file
def get_anno_path(subject, task):
    os.makedirs(config.anno_root, exist_ok=True) # creates directory for annotations if not aleady exisiting

    return os.path.join(config.anno_root, f"sub-{subject}_task-{task}_bad-annot.fif")


# only save bad annotations
# dont save event annotations since we get redundancy that way again
def save_bad_annotations(raw, subject, task, overwrite=True):
    bad_anno = raw.annotations[[a['description'].startswith("BAD") for a in raw.annotations]]

    if len(bad_anno) == 0:
        print("No new annotations to save")
        return

    fif_path = get_anno_path(subject, task)
    print(f"Saving annotations to {fif_path}")
    bad_anno.save(fif_path, overwrite=overwrite)


# load annotations (so that we dont have to reannotate everything)
def load_and_apply_annotations(raw, subject, task):
    fif_path = get_anno_path(subject, task)

    if not os.path.exists(fif_path):
        print(f"No separate annotation file for sub-{subject} and task {task}")
        return

    # Remove existing BAD annotations
    keep = [a['description'] for a in raw.annotations]
    good_mask = [not desc.startswith("BAD") for desc in keep]
    raw.set_annotations(raw.annotations[good_mask])

    loaded = mne.read_annotations(fif_path)

    # Match orig_time
    loaded = mne.Annotations(
        onset=loaded.onset,
        duration=loaded.duration,
        description=loaded.description,
        orig_time=raw.annotations.orig_time,
    )

    raw.set_annotations(raw.annotations + loaded)
    print("Loaded annotations")

