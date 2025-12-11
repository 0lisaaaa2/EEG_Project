import mne
import os
import pandas as pd


def remove_bad_channels(raw):

    raw.plot(block=True, scalings=40e-6)

    print(f"Identified bad channels: {raw.info['bads']}")

    # # Drop bad channels from the raw data
    # raw_cleaned = raw.copy().drop_channels(raw.info['bads']) -> do we want to do this before ica?



    filename = r"D:\lisa-\Universität_2\Master\2. Semester\EEG\EEG_Project\bad_annotations.csv"
    save_bad_annotations(raw, filename, overwrite=False)

    print(raw.annotations)


    return None


def save_bad_annotations(raw, filename, overwrite=False):
    """
    Extracts BAD_ annotations from raw,
    and saves them to a CSV file.

    If the file already exists:
        • overwrite=True  → replace the file
        • overwrite=False → append new rows to existing file
    """

    # --- Extract only BAD annotations ---
    #bad_anno = [a for a in raw.annotations if a['description'].startswith("BAD_")]
    bad_anno = raw.annotations

    if len(bad_anno) == 0:
        print("No BAD_ annotations found.")
        return

    # Convert to DataFrame for easy CSV handling
    df_new = pd.DataFrame({
        'onset':     [a['onset'] for a in bad_anno],
        'duration':  [a['duration'] for a in bad_anno],
        'description': [a['description'] for a in bad_anno],
    })

    # --- If file exists, decide between overwriting vs appending ---
    if os.path.exists(filename) and not overwrite:
        print(f"Appending to existing annotation file: {filename}")
        df_old = pd.read_csv(filename)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_csv(filename, index=False)
    else:
        print(f"Saving new annotation file: {filename}")
        df_new.to_csv(filename, index=False)



def load_and_apply_annotations(raw, filename):
    """
    Load annotations from CSV and add them to raw.
    """
    df = pd.read_csv(filename)

    loaded_anno = mne.Annotations(
        onset=df['onset'].tolist(),
        duration=df['duration'].tolist(),
        description=df['description'].tolist()
    )

    raw.set_annotations(raw.annotations + loaded_anno)
    print(f"Loaded {len(df)} annotations into raw.")

