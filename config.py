
# specify BIDS root directory
bids_root = "ds005841-download"
anno_root = "annotations"

# choose subjects and tasks to process
#subjects = ["001", "002"] # for quick testing purposes
subjects = ["001", "002", "003", "004", "005", "007", "008", "009", "011", "012", "013", "014", "015", "016", "018", "020", "021", "022", "023", "025", "027", "028", "029", "030", "031", "032", "033", "034", "035", "036", "037", "038", "040", "041", "042", "043", "044", "045", "046", "047", "048"]
tasks = ["regfront", "regperp"]

# filter frequencys specification
highpass = 0.1
lowpass = 40
notch = 50

# resampling specification
sample_rate = 256

# bad channels
bads = ["Status", "EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"]

# time window for baseline correction
tmin_baseline = -0.2 
tmax_baseline = 0.0    

# posterior electrode cluster for SPN analysis (defined in paper)
left_post = ["P3", "P5", "P7", "P9", "PO7", "PO3", "O1"]
right_post = ["P4", "P6", "P8", "P10", "PO8", "PO4", "O2"]
posterior_channels = left_post + right_post

# time window for SPN amplitude extraction
tmin_spn = 0.3
tmax_spn = 0.6