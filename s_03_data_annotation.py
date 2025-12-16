import mne
import os
import config
import matplotlib.pyplot as plt
import numpy as np



def remove_bad_channels(raw, subject, task):

    # load existing annotations if any
    load_and_apply_annotations(raw, subject, task)

    #print("Before adding new annotations: ", raw.annotations)

    raw.info['bads'] = config.bads

    # manually annotate data
    raw.plot(block=True, scalings=40e-6, title='Mark Bad Channels and Annotate Bad Segments - Close Window When Finished!')

    #print(f"Identified bad channels: {raw.info['bads']}")

    # save annotations for future use
    save_bad_annotations(raw, subject, task, overwrite=True)
    
    #print("After adding or not adding new anntotations: ", raw.annotations)
    return None




# path to annotations file
def get_anno_path(subject, task):
    os.makedirs(config.anno_root, exist_ok=True) # creates directory for annotations if not aleady exisiting

    return os.path.join(config.anno_root, f"sub-{subject}_task-{task}_bad-annot.fif")


# only save bad annotations
# dont save event annotations since we get redundancy that way again
def save_bad_annotations(raw, subject, task, overwrite=True):
    bad_anno = raw.annotations[[a['description'].startswith("BAD") for a in raw.annotations]]

    if len(bad_anno) == 0:
        print("No new annotations to save")
        return

    fif_path = get_anno_path(subject, task)
    print(f"Saving annotations to {fif_path}")
    bad_anno.save(fif_path, overwrite=overwrite)


# load annotations (so that we dont have to reannotate everything)
def load_and_apply_annotations(raw, subject, task):
    fif_path = get_anno_path(subject, task)

    if not os.path.exists(fif_path):
        print(f"No separate annotation file for sub-{subject} and task {task}")
        return

    # Remove existing BAD annotations
    keep = [a['description'] for a in raw.annotations]
    good_mask = [not desc.startswith("BAD") for desc in keep]
    raw.set_annotations(raw.annotations[good_mask])

    loaded = mne.read_annotations(fif_path)

    # Match orig_time
    loaded = mne.Annotations(
        onset=loaded.onset,
        duration=loaded.duration,
        description=loaded.description,
        orig_time=raw.annotations.orig_time,
    )

    raw.set_annotations(raw.annotations + loaded)
    print("Loaded annotations")

