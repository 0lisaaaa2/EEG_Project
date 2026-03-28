# EEG-Project

## Exploring the Perspective Cost of Viewing Objects in Virtual Reality: A Replication Analysis

### Description

This project aims to replicate the findings of the original study by Karakashevska et al. on symmetry processing in a VR environment. The goal is to reproduce the Sustained Posterior Negativity (SPN) in the EEG data and further examine the perspective cost between the viewing conditions frontoparallel and perspective.

To do this analysis, we used the original dataset provided by Karakashevska et al. on OpenNeuro and applied our own individual pipeline. This allows us to test the robustness of the original findings.

### Link to original dataset and study

Dataset: <https://openneuro.org/datasets/ds005841/versions/1.0.0>

Original Paper by Karakashevska et al.: <https://doi.org/10.1016/j.cortex.2025.05.008>

### Project Structure

- **requirements.txt** - States versions of Python libraries used.
- **config.py** - Defines paths and global configuration variables.
- **fix_events.py** - Extracts and saves events into `events.tsv` files (run once before pipeline execution). Overwrites original content of events.tsv files.
- **main.py** - Main script that runs the full analysis pipeline.

Pipeline modules executed by 'main.py':

- s_00_fetch_data.py
- s_01_downsample.py
- s_02_filter.py
- s_04_rereference.py
- s_05_ica.py
- s_06_interpolation.py
- s_07_epochs.py
- s_08_erp.py
- s_09_spn.py
- s_10_cost.py
- s_11_grand.py
- s_12_stat.py
- s_13_timefreq.py
- s_14_additional_stat.py

### Workflow Overview

1. **Download** the original dataset from the OpenNeuro link above.
2. **Install** the necessary Python libraries specified in the requirements.txt if not already installed.

    ```pip install -r requirements.txt```

3. **Specify the BIDS root directory of the dataset** in the *config.py* file. The default is "ds005841-download", as this is the default name after downloading.
4. **Run the file fix_events.py** in your terminal, if events not already all saved in the events.tsv files.

    ```python fix_events.py```

5. **Run the file *main.py*** in your terminal. This executes the full analysis pipeline.

    ```python main.py```
