import mne
import os
import pandas as pd
import config


def remove_bad_channels(raw):

    # load existing annotations if any
    load_and_apply_annotations(raw, config.anno_root)

    #print("Before doing anything new: ", raw.annotations)

    # manually annotate data
    raw.plot(block=True, scalings=40e-6)

    #print(f"Identified bad channels: {raw.info['bads']}")

    # # Drop bad channels from the raw data
    # raw_cleaned = raw.copy().drop_channels(raw.info['bads']) -> do we want to do this before ica?

    # save annotations for future use
    save_bad_annotations(raw, config.anno_root, overwrite=True)
    print("After doing something new: ", raw.annotations)
    return None


def save_bad_annotations(raw, base_path, overwrite=False):
    bad_anno = raw.annotations

    fif_path = base_path + ".fif"
    csv_path = base_path + ".csv"

    # --- Save real MNE annotation file ---
    print(f"Saving MNE annotation file: {fif_path}")
    bad_anno.save(fif_path, overwrite=True)

    # --- Save as CSV for inspection ---
    df = pd.DataFrame({
        "onset": bad_anno.onset,
        "duration": bad_anno.duration,
        "description": bad_anno.description,
    })
    print(f"Saving CSV annotation file: {csv_path}")
    df.to_csv(csv_path, index=False)

def load_and_apply_annotations(raw, base_path):
    fif_path = base_path + ".fif"

    if not os.path.exists(fif_path):
        print(f"No annotation file found at {fif_path}. Skipping load.")
        return

    loaded = mne.read_annotations(fif_path)

    # Match orig_time
    loaded = mne.Annotations(
        onset=loaded.onset,
        duration=loaded.duration,
        description=loaded.description,
        orig_time=raw.annotations.orig_time,
    )

    raw.set_annotations(raw.annotations + loaded)
    print("Loaded annotations into raw.")
