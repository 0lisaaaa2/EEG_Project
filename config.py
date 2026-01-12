
# specify BIDS root directory
bids_root = "ds005841-download"
# root of derivates directory in which the pipeline will store the processing results
deriv_root = "output/ds005841"

anno_root = "annotations"

# only analyze subject 001 and regfront for now
subjects = ["001", "002"]
#subjects = ["001", "002", "003", "004", "005", "007", "008", "009", "011", "012", "013", "014", "016", "018", "020", "021", "022", "023", "025", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "040", "041", "042", "043", "044", "045", "046", "047", "048"]
#subjects = ["006", "010", "015", "017", "019", "024", "026", "039"] #6,10,19, 26, 39 max() arg is an empty sequence, 15, 24 One PCA component captures most of the explained variance (99.96785153337908%), your threshold results in 1 component. You should select a higher value, 17 werte nan
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

