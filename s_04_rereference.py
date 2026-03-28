"""
Rereference EEG data to average reference.
"""

def rereferencing(raw):
    raw_reref = raw.copy().set_eeg_reference('average')
    return raw_reref