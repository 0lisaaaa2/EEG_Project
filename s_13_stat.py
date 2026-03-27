import scipy.stats as stats
from scipy.stats import t
import matplotlib.pyplot as plt
import numpy as np

# run one sided t-tests for the two main hypotheses
def run_statistics(spn_front_values, perspective_cost_values, alpha):
    # Hypothesis 1
    res1 = stats.ttest_1samp(spn_front_values, 0, alternative="less")
    dz1 = cohens_dz(spn_front_values, 0)
    print(f"Hypothesis 1: t={res1.statistic}, p={res1.pvalue}, dz={dz1}")

    if res1.pvalue < alpha:
        print("H0 rejected: Significant SPN present\n")
    else:
        print("H0 not rejected: No evidence for SPN\n")

    # Hypothesis 2
    # A - Test against zero
    res2 = stats.ttest_1samp(perspective_cost_values, 0, alternative="greater")
    dz2 = cohens_dz(perspective_cost_values, 0)
    print(f"Hypothesis 2A: t={res2.statistic}, p={res2.pvalue}, dz={dz2}")

    if res2.pvalue < alpha:
        print("H0 rejected: Perspective cost significantly > 0\n")
    else:
        print("H0 not rejected: Perspective cost not different from 0\n")

    # B - Test against 0.35 μV
    res3 = stats.ttest_1samp(perspective_cost_values, -0.35e-6, alternative="greater") # convert 0.35 microvolts to volts
    dz3 = cohens_dz(perspective_cost_values, -0.35e-6)
    print(f"Hypothesis 2B (0.35 μV): t={res3.statistic}, p={res3.pvalue}, dz={dz3}")

    if res3.pvalue < alpha:
        print("H0 rejected: Perspective cost is significantly smaller than 0.35 µV\n")
    else:
        print("H0 not rejected: Perspective cost may be meaningful\n")

    return None


def cohens_dz(x, mu0=0):
    x = np.array(x)  # convert list to array
    diff = x - mu0
    return diff.mean() / diff.std(ddof=1)


# amplitude bar chart with CI
def plot_spn_amplitude(grand_avg_cost, grand_avg_front, grand_avg_perp, all_subject_cost, all_subject_front, all_subject_perp, alpha=0.02):
    labels = ['Frontoparallel', 'Perspective', 'Perspective Cost']
    means = [grand_avg_front * 1e6, grand_avg_perp * 1e6, grand_avg_cost * 1e6]  # µV

    # Convert subject data to µV
    subj_data = [np.array(all_subject_front) * 1e6, np.array(all_subject_perp) * 1e6, np.array(all_subject_cost) * 1e6]   

    # Calculate CI
    ci_list = []
    for data in subj_data:
        n = len(data)
        sem = np.std(data, ddof=1) / np.sqrt(n)
        t_multiplier = t.ppf(1 - alpha/2, df=n-1)
        ci = sem * t_multiplier
        ci_list.append(ci)

    plt.figure(figsize=(8, 6))
    plt.bar(labels, means, color=['black', 'gray', 'red'], yerr=ci_list, capsize=8, error_kw={'elinewidth':1.5, 'ecolor':'lightgray'})
    plt.axhline(0, linestyle='--', linewidth=1)
    plt.axhline(-0.35, linestyle='--', linewidth=1, color='red')
    plt.ylabel('SPN Amplitude (µV)')
    plt.title(f'Average SPN Amplitudes Across All Subjects (CI {100*(1-alpha):.0f}%)')
    plt.tight_layout()
    plt.show()