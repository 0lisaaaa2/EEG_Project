

"""
authors only calculate spn for posterior electrode cluster
-> where SPN is expected to be most pronounced

for erp, include all electrodes, restrict only in spn calculation

"""


left_post = ["P3", "P5", "P7", "P9", "PO7", "PO3", "O1"]
right_post = ["P4", "P6", "P8", "P10", "PO8", "PO4", "O2"]
posterior_channels = left_post + right_post