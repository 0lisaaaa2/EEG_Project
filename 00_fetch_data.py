import mne
from mne_bids import BIDSPath, read_raw_bids
import numpy as np

bids_root = "ds005841-download"

subject_id = "001"
task = "regfront"    # lumfront, lumperp, regfront, regperp, signalscreen, signalvr -> Was ist signalscreen, signalvr?

bids_path = BIDSPath(
    subject=subject_id,
    task=task,
    datatype="eeg",
    suffix="eeg",
    extension=".bdf",
    root=bids_root
)

#print(bids_path.fpath)

raw = read_raw_bids(bids_path)
raw.load_data()