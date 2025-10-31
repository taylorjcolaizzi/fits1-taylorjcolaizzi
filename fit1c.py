import ROOT as r
import numpy as np
import matplotlib.pyplot as plt

def fit1c(entries=1000, save=False):
    # Open the ROOT TFile
    filename = "histo25.root"  # Replace with your actual file name
    tfile = r.TFile(filename)

    # list the file contents
    tfile.ls()

    # Retrieve the histogram from the TFile
    histname = "randomHist1"  # Replace with your actual histogram name
    histogram = tfile.Get(histname)

    randomHist1 = r.TH1F("randomHist1", "Random Histogram;x;frequency", 100, 0, 100)
    pseudoHist1 = r.TH1F("pseudoHist1", "PseudoExperiments;x;frequency", 100, 0, 100)
    randomHist1.Sumw2() # store sum of squares of errors
    generator=r.TRandom2(0)  # parameter == seed, 0->use clock

    # a basic function to convert ROOT histograms into numpy arrays
    def hist2np(h):
        nbin=h.GetNbinsX()
        x=np.zeros(nbin)
        y=np.zeros(nbin)
        ey=np.zeros(nbin)
        for i in range(1,nbin+1):  # bin index is 1..N
            x[i-1]=h.GetBinCenter(i)
            y[i-1]=h.GetBinContent(i)
            ey[i-1]=h.GetBinError(i)
        return x,y,ey
    
    # Plot the histogram data with error bars
    x,y,yerr = hist2np(histogram)

    plt.errorbar(x, y, yerr=yerr, fmt='.');
    plt.show()

    hdata=r.TH1F("hdata","data distibution;;Events/0.1",20,-10,10)
    hmodel=r.TH1F("hmodel","model distibution;;Events/0.1",20,-1,1)
    model=r.TF1("model","1.05-x",-1,1)
    hmodel.SetLineColor(r.kRed)
    for i in range(len(x)): 
        hdata.Fill(x[i],y[i])
    for i in range(1,hmodel.GetNbinsX()+1):
        xi=hmodel.GetBinCenter(i)
        hmodel.Fill(xi,model.Eval(xi))

    tc=r.TCanvas()
    hdata.Draw("e")
    hmodel.Draw("hist,same")
    tc.Draw()
    tc.SaveAs("test_figure.pdf")


    tc=r.TCanvas()
    tc.Divide(1)
    tc.cd(1)
    histogram.Draw("e") # just regular histogram with error bars
    tc.Draw()
    tc.SaveAs("raw_histo25_plot.pdf")

    from math import log
    def calcNLL(data,model):
        NLL=0.0
        for i in range(1,data.GetNbinsX()+1):
            nExpected = model.GetBinContent(i)
            nObs = data.GetBinContent(i)
            prob = r.TMath.Poisson(nObs,nExpected)  # Poisson P(nobs; mu=nExpected)
            NLL -= log(prob)
        return NLL

    for i in range(entries):
        randomHist1.Fill(generator.Gaus(50,10)) # params: mean, sigma

    #simple fits may be performed automatically
    r.gStyle.SetOptFit(1111) # show reduced chi2, probability, and params
    randomHist1.Fit("gaus")
    randomHist1.DrawCopy("e")  # "e" shows bin errors

    tc.Update()
    tc.Draw()
    tc.SaveAs("fitted_histo25_plot.pdf")
    # Using DrawCopy vs Draw allows us to delete the original histogram
    # without removing it from the display.  If we save the histogran to a
    # file and close the file, it will be deleted from memory.

    # Above we used a built in function, gaus, in the fit
    # This function will be associated with the histogram
    # and may be retrieved to get parameter information
    # Refer to http://root.cern.ch/root/html/TF1.html
    # for a complete list of TF1 methods

    fitfunc = randomHist1.GetFunction("gaus")
    print("\nFit Params and errors")
    for i in range(3):
        print(f'{fitfunc.GetParameter(i):.2f} +- {fitfunc.GetParError(i):.2f}')

    print(f'Fit Probability: {fitfunc.GetProb():.2f}') # returns chi^2 p-value

    return randomHist1
# **************************************

if __name__ == "__main__":
    fit1c()
    input("hit Enter to exit")


# example of plotting a similar histogram with error bars using numpy/matplotlib
# then using lmfit to perform the fit

import numpy as np
from matplotlib import pyplot as plt

entries=1000

vals=np.random.normal(loc=50, scale=10, size=entries)
y,binEdges=np.histogram(vals, bins=50, range=(1,100))
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
ey         = np.sqrt(y)
width      = binEdges[1]-binEdges[0]
plt.bar(bincenters, y, width=width, color='r', yerr=ey)
plt.show(block=False)
