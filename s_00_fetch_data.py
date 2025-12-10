import mne
from mne_bids import BIDSPath, read_raw_bids
import numpy as np

import config

def load_data(sub, task):

    bids_path = BIDSPath(
        subject=sub,
        task=task,
        datatype="eeg",
        suffix="eeg",
        extension=".bdf",
        root=config.bids_root
    )

    raw = read_raw_bids(bids_path)
    raw.load_data()
    return raw