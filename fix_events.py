import os 
import mne
import pandas as pd
import numpy as np

subjects = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048"]
tasks = ["regfront", "regperp"]

subjects_test = ["001"]

data_dir = r"ds005841-download"  
output_dir = r"ds005841-download"

event_dict_front = {
    1: "REF_LIGHT",
    2: "REF_DARK",
    3: "RAND_LIGHT",
    4: "RAND_DARK"
}

event_dict_perp = {
    5: "REF_LIGHT", 
    6: "REF_DARK",
    7: "RAND_LIGHT",
    8: "RAND_DARK"
}

aggregation = {
    "REF_DARK": "SYM",
    "REF_LIGHT": "SYM",
    "RAND_DARK": "ASYM",
    "RAND_LIGHT": "ASYM"
}

trigger_aggregation ={
    "SYM": 1,
    "ASYM": 2
}


# overwrite tsv file with correct event annotations
def process_subject_task(sub, task):
    bdf_file = os.path.join(data_dir, f"sub-{sub}", "eeg", f"sub-{sub}_task-{task}_eeg.bdf")
    
    raw = mne.io.read_raw_bdf(bdf_file, preload=True)
    
    # Extract events from the status channel
    events = mne.find_events(raw, stim_channel="Status", initial_event=True)
    
    if task == "regfront":
            event_dict = event_dict_front
    else:
        event_dict = event_dict_perp
    
    # filter out events not belonging to evnt_dict
    all_events = events
    mask = np.isin(all_events[:, 2], list(event_dict.keys()))
    events = all_events[mask]
    
    # Convert to aggregated trial types and trigger IDs
    onsets = events[:, 0] / raw.info['sfreq']
    durations = [0.5] * len(events)
    trial_types = [aggregation[event_dict[e]] for e in events[:, 2]]
    aggregated_trigger_ids = [trigger_aggregation[tt] for tt in trial_types]
    
    # Build DataFrame
    df_events = pd.DataFrame({
        "onset": onsets,
        "duration": durations,
        "trial_type": trial_types,
        "trigger_id": aggregated_trigger_ids
    })
    
    # Save TSV
    tsv_path = os.path.join(data_dir, f"sub-{sub}", "eeg", f"sub-{sub}_task-{task}_events.tsv")
    df_events.to_csv(tsv_path, sep="\t", index=False)
    print(f"Saved events TSV for sub-{sub} task-{task} → {tsv_path}")

for sub in subjects_test:
    for task in tasks:
        process_subject_task(sub, task)