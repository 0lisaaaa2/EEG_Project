import mne

"""
Epoch the raw data around events.
"""

# epoch with a time window from -200 ms to 800 ms around the event onset
def epoching(raw, tmin=-0.2, tmax=0.8):

    events, event_id = mne.events_from_annotations(raw)

    # set rejection criteria for peak to peak rejection
    reject_criteria = dict(eeg=200e-6) # 200 µV

    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, reject_by_annotation=True, event_repeated='drop', reject=reject_criteria)
    return epochs