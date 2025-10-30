#include "TH1F.h"
#include "TF1.h"
#include "TFile.h"
#include "TStyle.h"
#include "TRandom2.h"
#include "TROOT.h"


// fit1a.C
void fit1a(int entries=1000, int ntrials=1000, bool save=false) {
  // Parameters:
  // entries : number of random numbers in histogram
  // ntrials : number of histograms used in calculation


  gROOT->Reset();  // useful to reset ROOT to a cleaner state

  TFile *tf=0;
  if (save) tf=new TFile("histo.root","recreate");

  TH1F *randomHist1 = new TH1F("randomHist1", "Random Histogram;x;frequency", 100, 0, 100);
  TRandom2 *generator=new TRandom2(0);  // parameter == seed, 0->use clock

  double storedChiSquare[1000]; // store reduced chi_square here.
  double storedMean[1000]; // store mean values.
  double chi_square;
  double ndegrees_freedom;
  double reduced_chi_square;

  for (int j=0 ; j<ntrials ; j++) {
    randomHist1->Reset(); // reset histogram bin content to 0
    for (int i=0 ; i<entries ; i++){
      randomHist1->Fill(generator->Gaus(50,10)); // params: mean, sigma
    }
    randomHist1->Fit("gaus");
    // create a pointer to the fit result, so we can do methods on it
    TF1 *fitfunc = randomHist1->GetFunction("gaus");
    // fit_mean = fitfunc->Mean(); // gets mean value
    fit_mean = fitfunc->GetParameter(1); //mean value
    fit_normalization = fitfunc->GetParameter(0);
    fit_sigma = fitfunc->GetParameter(2); // sigma

    chi_square = fitfunc->GetChisquare();
    ndegrees_freedom = fitfunc->GetNDF();
    reduced_chi_square = chi_square / ndegrees_freedom;

    storedChiSquare[j] = reduced_chi_square;
  }

  // now that we have the reduced_chi_square data, we can put it into another histogram.

  TH1F *chi_squareHist1 = new TH1F("chi_squareHist1", "Reduced Chi-Square Histogram;Chi;Frequency", 100, 0, 2);
  for (int i=0 ; i<1000 ; i++) {
    chi_squareHist1->Fill(storedChiSquare[i]);
  }
  // simple fits may be performed automatically
  // gStyle->SetOptFit(111);  // show reduced chi2 and params
  gStyle->SetOptFit(1111); // show reduced chi2, probability, and params
  chi_squareHist1->Fit("gaus");  
  chi_squareHist1->DrawCopy("e");  // "e" shows bin errors
  // Using DrawCopy vs Draw allows us to delete the original histogram
  // without removing it from the display.  If we save the histogran to a
  // file and close the file, it will be deleted from memory.


  // Above we used a built in function, gaus, in the fit
  // This function will be associated with the histogram
  // and may be retrieved to get parameter information
  // Refer to http://root.cern.ch/root/html/TF1.html
  // for a complete list of TF1 methods

  TF1 *fitchi = chi_squareHist1->GetFunction("gaus");
  cout << "\nFit Params and errors" << endl;
  cout << fitchi->GetParameter(0) << " +- " << fitchi->GetParError(0) << endl;
  cout << fitchi->GetParameter(1) << " +- " << fitchi->GetParError(1) << endl;
  cout << fitchi->GetParameter(2) << " +- " << fitchi->GetParError(2) << endl;
  cout << "Fit Probability: " << fitchi->GetProb() << endl; // returns chi^2 p-value

  if (save) {
    tf->Write();
    tf->Close();
  }
  cout << "Use .q to exit root" << endl;
}
