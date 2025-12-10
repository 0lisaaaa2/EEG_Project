
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

# stim_channel = "Status"

# maybe calculate 4 erps now, and aggregate into 2 erps later?
conditions = ["SYM", "ASYM"]

steps = [
    # Preprocessing
    "preprocessing/_01_data_quality",
    "preprocessing/_04_frequency_filter",
    "preprocessing/_06a1_fit_ica",
    "preprocessing/_06a2_find_ica_artifacts",
    "preprocessing/_08a_apply_ica",
    "preprocessing/_07_make_epochs",
    "preprocessing/_09_ptp_reject",

    # Sensor-space ERP
    "sensor/_01_make_evoked"
]

interpolate_bads_grand_average = False
run_source_estimation = False