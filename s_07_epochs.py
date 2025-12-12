import mne

"""Epoch the raw data around events.

    input: raw (EEG Data), event_id (dict of event labels and their IDs), tmin (start time before event), tmax (end time after event)
    return: epochs (Epoched EEG Data)
    """
def epoching(raw, tmin=-0.2, tmax=0.8):

    events, event_id = mne.events_from_annotations(raw)
    #print("evnets", events)
    #print("event_id", event_id)

    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, reject_by_annotation=True, event_repeated='drop')
    return epochs