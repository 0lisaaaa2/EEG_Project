
# specify BIDS root directory
bids_root = "ds005841-download"
# root of derivates directory in which the pipeline will store the processing results
deriv_root = "output/ds005841"

anno_root = "annotations"

# only analyze subject 001 and regfront for now
subjects = ["024"]
tasks = ["regfront", "regperp"]  # lumfront, lumperp, regfront, regperp, signalscreen, signalvr

# Filter frequencys specification
highpass = 0.1
lowpass = 40
notch = 50
sample_rate = 256 # resample to 256 Hz

# Bad Channels - Please inspect visually before ICA and add them here
#bads = ["P1", "POz", "Pz", "Status", "EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"]
bads = ["Status", "EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"]

# time window for baseline correction
tmin_baseline = -0.2 
tmax_baseline = 0.0    

# posterior electrode cluster for SPN analysis (defined in paper)
left_post = ["P3", "P5", "P7", "P9", "PO7", "PO3", "O1"]
right_post = ["P4", "P6", "P8", "P10", "PO8", "PO4", "O2"]
posterior_channels = left_post + right_post

# time window for SPN amplitude extraction
# SPN is late ERP effect so in that window it should occur
# values from paper -> make changes? 
tmin_spn = 0.3
tmax_spn = 0.6

