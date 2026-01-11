def rereferencing(raw):
    """Rereference EEG data to average reference.

    input: raw (EEG Data)
    return: raw_reref (Rereferenced EEG Data)
    """
    raw_reref = raw.copy().set_eeg_reference('average')
    return raw_reref