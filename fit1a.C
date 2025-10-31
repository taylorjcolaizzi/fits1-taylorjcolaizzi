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
  double chi_square;
  double ndegrees_freedom;
  double reduced_chi_square;
  double fit_mean[1000];
  double fit_normalization[1000];
  double fit_sigma[1000];
  double fit_probability[1000];
  double fit_mean_error[1000];

  for (int j=0 ; j<ntrials ; j++) {
    randomHist1->Reset(); // reset histogram bin content to 0
    for (int i=0 ; i<entries ; i++){
      randomHist1->Fill(generator->Gaus(50,10)); // params: mean, sigma
    }
    randomHist1->Fit("gaus");
    // create a pointer to the fit result, so we can do methods on it
    TF1 *fitfunc = randomHist1->GetFunction("gaus");


    fit_mean[j] = fitfunc->GetParameter(1); //mean value
    fit_sigma[j] = fitfunc->GetParameter(2); // sigma
    fit_probability[j] = fitfunc->GetProb();
    fit_mean_error[j] = fitfunc->GetParError(1);

    chi_square = fitfunc->GetChisquare();
    ndegrees_freedom = fitfunc->GetNDF();
    reduced_chi_square = chi_square / ndegrees_freedom;

    storedChiSquare[j] = reduced_chi_square;
  }

  // now that we have the reduced_chi_square data, we can put it into another histogram.

  TH1F *chi_squareHist1 = new TH1F("chi_squareHist1", "Reduced Chi-Square Histogram;Chi;Frequency", 100, 0, 2);
  TH1F *meanHist1 = new TH1F("meanHist1", "Mean from Fits; Mean; Frequency", 100, 49, 51);
  TH1F *error_meanHist1 = new TH1F("error_meanHist1", "Error of Mean from Fits; Error; Frequency", 100, 0.3, 0.35);
  TH1F *chi_probHist1 = new TH1F("chi_probHist1", "Chi-Square Probability; Probability; Frequency", 100, 0, 1);
  
  for (int i=0 ; i<1000 ; i++) {
    chi_squareHist1->Fill(storedChiSquare[i]);
    meanHist1->Fill(fit_mean[i]);
    error_meanHist1->Fill(fit_mean_error[i]);
    chi_probHist1->Fill(fit_probability[i]);
  }

  TScatter *scatter = new TScatter(1000, storedChiSquare, fit_probability);

  TCanvas *c1 = new TCanvas("c1", "2x2 Plots", 800, 600);
  c1->Divide(2, 2);

  c1->cd(1);
  chi_squareHist1->Draw();

  c1->cd(2);
  meanHist1->Draw();

  c1->cd(3);
  // scatter->Draw("scat");
  chi_probHist1->Draw();

  c1->cd(4);
  error_meanHist1->Draw();

  c1->Update();
  c1->Draw();

  if (save) {
    tf->Write();
    tf->Close();
  }
  cout << "Use .q to exit root" << endl;
}
