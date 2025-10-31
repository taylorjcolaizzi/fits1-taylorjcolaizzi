#include "TH1F.h"
#include "TF1.h"
#include "TFile.h"
#include "TStyle.h"
#include "TRandom2.h"
#include "TROOT.h"


// fit1b.C
void fit1b(int entries=10, int ntrials = 1000, bool save=false) {
  // Parameters:
  // entries : number of random numbers in histogram | LOW STATISTICS!
  // ntrials : number of histograms used in calculation

  gROOT->Reset();  // useful to reset ROOT to a cleaner state

  TFile *tf=0;
  if (save) tf=new TFile("histo.root","recreate");

  TH1F *randomHist1 = new TH1F("randomHist1", "Random Histogram;x;frequency", 100, 0, 100);
  TH1F *randomHist2 = new TH1F("randomHist2", "Random Histogram;x;frequency", 100, 0, 100);
  TRandom2 *generator=new TRandom2(0);  // parameter == seed, 0->use clock

  // data storage
  double mean_ChiSquare[1000]; //chi-square fits
  double mean_NLL[1000];       //negative log likelihood fits
  double chi_uncertainty[1000];
  double NLL_uncertainty[1000];

  for (int j=0 ; j<ntrials ; j++) {
    randomHist1->Reset(); // reset histogram bin content to 0
    randomHist2->Reset();
    for (int i=0 ; i<entries ; i++){
      randomHist1->Fill(generator->Gaus(50,10)); // params: mean, sigma
      randomHist2->Fill(generator->Gaus(50,10));
    }
    randomHist1->Fit("gaus"); // chi-square method
    randomHist2->Fit("gaus", "L"); // NLL method
    // create a pointer to the fit result, so we can do methods on it
    TF1 *fitfunc1 = randomHist1->GetFunction("gaus");
    TF1 *fitfunc2 = randomHist2->GetFunction("gaus");

    mean_ChiSquare[j] = fitfunc1->GetParameter(1); //mean value
    mean_NLL[j] = fitfunc2->GetParameter(1);
    chi_uncertainty[j] = fitfunc1->GetParError(1);
    NLL_uncertainty[j] = fitfunc2->GetParError(1);
  }

  // now that we have the reduced_chi_square data, we can put it into another histogram.

  TH1F *chi_squareHist1 = new TH1F("chi_squareHist1", "Mean of Chi-Square Fits;Mean;Frequency", 100, 0, 100);
  TH1F *NLL_Hist1 = new TH1F("NLL_Hist1", "Means of NLL Fits;Mean;Frequency", 100, 0, 100);
  TH1F *chi_errorHist1 = new TH1F("chi_errorHist1", "Error in Chi-Square Means;Error;Frequency", 100, 0, 100);
  TH1F *NLL_errorHist1 = new TH1F("NLL_errorHist1", "Error in NLL Means;Error;Frequency", 100, 1, 5);

  for (int i=0 ; i<1000 ; i++) {
    chi_squareHist1->Fill(mean_ChiSquare[i]);
    NLL_Hist1->Fill(mean_NLL[i]);
    chi_errorHist1->Fill(chi_uncertainty[i]);
    NLL_errorHist1->Fill(NLL_uncertainty[i]);
  }

  TCanvas *c1 = new TCanvas("c1", "1x2 Plots", 800, 600);
  c1->Divide(1, 2);

  c1->cd(1);
  chi_squareHist1->Draw();

  c1->cd(2);
  NLL_Hist1->Draw();

  c1->Update();
  c1->Draw();

  c1->SaveAs("result2.pdf");

  TCanvas *c2 = new TCanvas("c2", "error plots", 800, 600);
  c2->Divide(1, 2);

  c2->cd(1);
  chi_errorHist1->Draw();

  c2->cd(2);
  NLL_errorHist1->Draw();

  c2->Update();
  c2->Draw();

  c2->SaveAs("exercise_2_extra.pdf");

  if (save) {
    tf->Write();
    tf->Close();
  }
  cout << "Use .q to exit root" << endl;
}
