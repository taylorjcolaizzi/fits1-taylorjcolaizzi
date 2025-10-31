import numpy as np
import matplotlib.pyplot as plt
from ROOT import TFile, TH1F, TF1, TRandom3, gROOT

# Load histogram from ROOT file
file = TFile.Open("histo25.root")
hist = file.Get("randomHist1")

for key in file.GetListOfKeys():
    print(key.GetName())

# Perform NLL fit using ROOT
model = TF1("model", "gaus", hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
hist.Fit(model, "LL")  # Log-likelihood fit

# Extract best-fit parameters
mean_fit = model.GetParameter(1)
sigma_fit = model.GetParameter(2)
n_events = int(hist.Integral())

# Define Gaussian PDF
def gaussian(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu)/sigma)**2) / (sigma * np.sqrt(2*np.pi))

# Compute NLL for a histogram
def compute_nll(hist, mu, sigma):
    nll = 0
    for i in range(1, hist.GetNbinsX()+1):
        x = hist.GetBinCenter(i)
        n = hist.GetBinContent(i)
        f = gaussian(x, mu, sigma)
        if f > 0 and n > 0:
            nll -= 2 * n * np.log(f)
    return nll

# Compute NLL for original data
nll_data = compute_nll(hist, mean_fit, sigma_fit)

# Generate toy experiments
def generate_toy_hist(hist, mu, sigma, n_events):
    rand = TRandom3(0)
    toy = TH1F("toy", "Toy", hist.GetNbinsX(), hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    for _ in range(n_events):
        x = rand.Gaus(mu, sigma)
        toy.Fill(x)
    return toy

# Run pseudo experiments
n_toys = 1000
nll_toys = []
for _ in range(n_toys):
    toy_hist = generate_toy_hist(hist, mean_fit, sigma_fit, n_events)
    nll = compute_nll(toy_hist, mean_fit, sigma_fit)
    nll_toys.append(nll)

# Plot NLL distribution
plt.hist(nll_toys, bins=50, alpha=0.7, label="Toy NLLs")
plt.axvline(nll_data, color='red', linestyle='dashed', linewidth=2, label="Data NLL")
plt.xlabel("-2 ln L")
plt.ylabel("Frequency")
plt.title("NLL Distribution from Toy Experiments")
plt.legend()
# plt.savefig("result3.pdf")
plt.close()

# Estimate p-value
n_extreme = sum(1 for nll in nll_toys if nll >= nll_data)
p_value = n_extreme / n_toys
print(f"Estimated p-value: {p_value:.4f}")

# Scan -2lnL vs mean
means = np.linspace(mean_fit - 2*sigma_fit, mean_fit + 2*sigma_fit, 100)
nll_scan = [compute_nll(hist, m, sigma_fit) for m in means]
nll_min = min(nll_scan)

plt.plot(means, nll_scan, label="-2 ln L")
plt.axhline(nll_min + 4, color='gray', linestyle='dotted', label="-2 ln L_min + 4")
plt.xlabel("Mean")
plt.ylabel("-2 ln L")
plt.title("NLL Contour for histo25")
plt.legend()
plt.savefig("result4a.pdf")
plt.close()

mean_fit = model.GetParameter(1)
mean_error = model.GetParError(1)

# Find where NLL crosses min + 1
nll_min = min(nll_scan)
threshold = nll_min + 1

# Find indices where NLL crosses the threshold
indices = [i for i, val in enumerate(nll_scan) if val <= threshold]
mean_low = means[min(indices)]
mean_high = means[max(indices)]
mean_error_scan = (mean_high - mean_low) / 2

# --- Extract error from NLL scan ---
nll_min = min(nll_scan)
threshold = nll_min + 1

# --- Get error from fitter ---
mean_error_fit = model.GetParError(1)

# --- Print comparison ---
print("\n--- Error Comparison ---")
print(f"Fitter-reported error on mean: ±{mean_error_fit:.4f}")
print(f"NLL scan error on mean: ±{mean_error_scan:.4f}")
print(f"Mean range from NLL scan: [{mean_low:.4f}, {mean_high:.4f}]")

# ~~~~~ do it for histo1k.root

# --- Load histogram for chi-square analysis ---
file_chi2 = TFile.Open("histo1k.root")
hist_chi2 = file_chi2.Get("randomHist1")

if not hist_chi2:
    raise RuntimeError("Histogram 'histo' not found in histo1k.root")

# --- Perform chi-square fit ---
model_chi2 = TF1("model_chi2", "gaus", hist_chi2.GetXaxis().GetXmin(), hist_chi2.GetXaxis().GetXmax())
hist_chi2.Fit(model_chi2, "Q")  # Quiet fit using chi-square
mean_fit_chi2 = model_chi2.GetParameter(1)
sigma_fit_chi2 = model_chi2.GetParameter(2)
mean_error_fit_chi2 = model_chi2.GetParError(1)

# --- Compute chi-square manually for scan ---
def compute_chi2(hist, mu, sigma):
    chi2 = 0
    for i in range(1, hist.GetNbinsX()+1):
        x = hist.GetBinCenter(i)
        n = hist.GetBinContent(i)
        err = hist.GetBinError(i)
        f = gaussian(x, mu, sigma) * hist.GetBinWidth(i) * hist.Integral()  # scale to expected counts
        if err > 0:
            chi2 += ((n - f)**2) / (err**2)
    return chi2

# --- Scan chi-square vs mean ---
means_chi2 = np.linspace(mean_fit_chi2 - 2*sigma_fit_chi2, mean_fit_chi2 + 2*sigma_fit_chi2, 100)
chi2_scan = [compute_chi2(hist_chi2, m, sigma_fit_chi2) for m in means_chi2]
chi2_min = min(chi2_scan)
threshold_chi2 = chi2_min + 1

# --- Extract error from chi-square scan ---
indices_chi2 = [i for i, val in enumerate(chi2_scan) if val <= threshold_chi2]
mean_low_chi2 = means_chi2[min(indices_chi2)]
mean_high_chi2 = means_chi2[max(indices_chi2)]
mean_error_scan_chi2 = (mean_high_chi2 - mean_low_chi2) / 2

# --- Plot chi-square scan ---
plt.plot(means_chi2, chi2_scan, label="χ²")
plt.axhline(chi2_min + 1, color='gray', linestyle='dotted', label="χ²_min + 1")
plt.xlabel("Mean")
plt.ylabel("χ²")
plt.title("Chi-square Contour Scan")
plt.legend()
plt.savefig("result4_chi2.pdf")
plt.close()

# --- Print comparison ---
print("\n--- Chi-square Error Comparison ---")
print(f"Fitter-reported error on mean (χ² fit): ±{mean_error_fit_chi2:.4f}")
print(f"Chi-square scan error on mean: ±{mean_error_scan_chi2:.4f}")
print(f"Mean range from χ² scan: [{mean_low_chi2:.4f}, {mean_high_chi2:.4f}]")