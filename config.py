
# specify BIDS root directory
bids_root = "ds005841-download"
# root of derivates directory in which the pipeline will store the processing results
deriv_root = "output/ds005841"

# only analyze subject 001 for now
subjects = ["001"]
tasks = ["regfront", "regperp"]  # lumfront, lumperp, regfront, regperp, signalscreen, signalvr

sample_rate = 256 # resample to 256 Hz