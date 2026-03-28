import mne
import os
import config
from pyprep.prep_pipeline import PrepPipeline

"""
EEG preprocessing:
- automatic bad channel detection (PyPREP)
- save/load results to avoid recomputation
"""

# =========================
# BAD CHANNEL DETECTION
# =========================
def detect_bad_channels(raw):
    # mark EXG channels as non-EEG
    exg_chs = [ch for ch in raw.ch_names if ch.startswith('EXG')]
    raw.set_channel_types({ch: 'misc' for ch in exg_chs})

    raw_prep = raw.copy().pick_types(eeg=True)

    montage = mne.channels.make_standard_montage('standard_1020')

    prep_params = {
        'ref_chs': 'eeg',
        'reref_chs': 'eeg',
        'line_freqs': [50],
    }

    prep = PrepPipeline(raw_prep, prep_params, montage=montage)
    prep.fit()

    bad_channels = prep.interpolated_channels + prep.still_noisy_channels
    print("Detected bad channels:", bad_channels)

    raw.info['bads'].extend(bad_channels)
    raw.info['bads'] = list(set(raw.info['bads']))


# =========================
# PATH HELPER
# =========================
def get_bad_channels_path(subject, task):
    os.makedirs(config.anno_root, exist_ok=True)
    return os.path.join(
        config.anno_root,
        f"sub-{subject}_task-{task}_bad-channels.txt"
    )


# =========================
# SAVE / LOAD BAD CHANNELS
# =========================
def save_bad_channels(raw, subject, task):
    path = get_bad_channels_path(subject, task)

    with open(path, "w") as f:
        for ch in raw.info['bads']:
            f.write(ch + "\n")

    print(f"Saved bad channels to {path}")


def load_bad_channels(raw, subject, task):
    path = get_bad_channels_path(subject, task)

    if not os.path.exists(path):
        print("No saved bad channels found")
        return False

    with open(path, "r") as f:
        bads = [line.strip() for line in f.readlines()]

    raw.info['bads'].extend(bads)
    raw.info['bads'] = list(set(raw.info['bads']))

    print("Loaded bad channels")
    return True


# =========================
# MAIN PIPELINE (CACHED)
# =========================
def auto_preprocess(raw, subject, task, overwrite=False):
    """
    Runs automatic bad channel detection OR loads cached results.
    """

    # Try loading cached results
    if not overwrite:
        loaded = load_bad_channels(raw, subject, task)

        if loaded and len(raw.info['bads']) > 0:
            print("Using cached bad channels")
            return raw

    # Otherwise run detection
    print("Running automatic bad channel detection...")
    detect_bad_channels(raw)

    # Save results
    save_bad_channels(raw, subject, task)

    return raw