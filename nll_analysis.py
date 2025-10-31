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
plt.title("NLL Contour Scan")
plt.legend()
plt.savefig("result4.pdf")
plt.close()


# ~~~~~ do it for histo1k.root

# Load histogram from ROOT file
file = TFile.Open("histo1k.root")
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
means = np.linspace(mean_fit - .1*sigma_fit, mean_fit + .1*sigma_fit, 100)
nll_scan = [compute_nll(hist, m, sigma_fit) for m in means]
nll_min = min(nll_scan)

plt.plot(means, nll_scan, label="-2 ln L")
plt.axhline(nll_min + 4, color='gray', linestyle='dotted', label="-2 ln L_min + 4")
plt.xlabel("Mean")
plt.ylabel("-2 ln L")
plt.title("NLL Contour Scan")
plt.legend()
plt.savefig("result5.pdf")
plt.close()