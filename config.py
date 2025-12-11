
# specify BIDS root directory
bids_root = "ds005841-download"
# root of derivates directory in which the pipeline will store the processing results
deriv_root = "output/ds005841"

# only analyze subject 001 for now
subjects = ["001"]
tasks = ["regfront", "regperp"]  # lumfront, lumperp, regfront, regperp, signalscreen, signalvr

# Filter frequencys specification
highpass = 0.1
lowpass = 40
notch = 50
sample_rate = 256 # resample to 256 Hz
