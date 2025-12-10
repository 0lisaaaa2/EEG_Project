
# specify BIDS root directory
bids_root = "ds005841-download"
# root of derivates directory in which the pipeline will store the processing results
deriv_root = "output/ds005841"

# only analyze subject 001 for now
subjects = ["001"]
task = "regfront"  # lumfront, lumperp, regfront, regperp, signalscreen, signalvr
interactive = True
ch_types = ["eeg"]

# event_id = {
#     "RAND_DARK": 4,
#     "RAND_LIGHT": 3,
#     "REF_DARK": 2,
#     "REF_LIGHT": 1,
# }

stim_channel = "Status"

conditions = ["RAND_DARK", "RAND_LIGHT", "REF_DARK", "REF_LIGHT"]

# steps = [
#     "01-import",
#     "02-filter",
#     "03-ica",         # or "03-ref" depending on your config
#     "04-make_epochs",
#     "05-evoked"
# ]

run_source_estimation = False