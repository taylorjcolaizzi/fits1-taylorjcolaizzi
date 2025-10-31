#include <iostream>
#include <vector>
#include <cmath>
#include "TH1F.h"
#include "TF1.h"
#include "TCanvas.h"
#include "TLine.h"
#include "TRandom3.h"
#include "TFile.h"

double computeNLL(TH1F* hData, TF1* fModel) {
    double nll = 0.0;
    int nBins = hData->GetNbinsX();

    for (int i = 1; i <= nBins; ++i) {
        double ni = hData->GetBinContent(i);
        double xi = hData->GetBinCenter(i);
        double mui = fModel->Eval(xi) * hData->GetBinWidth(i);

        if (mui > 0) {
            nll += mui - ni * std::log(mui);
        }
    }
    return nll;
}

void nll_consistency_check() {
    // Step 1: Load histogram from file
    TFile* file = TFile::Open("histo25.root", "READ");
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Cannot open file histo25.root" << std::endl;
        return;
    }

    TH1F* hData = dynamic_cast<TH1F*>(file->Get("randomHist1"));
    if (!hData) {
        std::cerr << "Error: Histogram 'hData' not found in histo25.root" << std::endl;
        file->Close();
        return;
    }

    hData->SetDirectory(0); // Detach from file so it persists after file close
    file->Close();

    // Step 2: Fit the histogram with a model
    TF1* fModel = new TF1("fModel", "gaus", hData->GetXaxis()->GetXmin(), hData->GetXaxis()->GetXmax());
    hData->Fit(fModel, "L");

    // Step 3: Compute NLL for the data
    double dataNLL = computeNLL(hData, fModel);
    std::cout << "Data NLL: " << dataNLL << std::endl;

    // Step 4: Generate toy experiments
    std::vector<double> nllValues;
    int nToys = 1000;
    TRandom3 rand(0);

    for (int i = 0; i < nToys; ++i) {
        TH1F* hToy = new TH1F("hToy", "Toy Data", hData->GetNbinsX(),
                              hData->GetXaxis()->GetXmin(), hData->GetXaxis()->GetXmax());

        for (int bin = 1; bin <= hToy->GetNbinsX(); ++bin) {
            double xi = hToy->GetBinCenter(bin);
            double mui = fModel->Eval(xi) * hToy->GetBinWidth(bin);
            int ni = rand.Poisson(mui);
            hToy->SetBinContent(bin, ni);
        }

        double toyNLL = computeNLL(hToy, fModel);
        nllValues.push_back(toyNLL);
        delete hToy;
    }

    // Step 5: Plot NLL distribution
    double minNLL = *std::min_element(nllValues.begin(), nllValues.end());
    double maxNLL = *std::max_element(nllValues.begin(), nllValues.end());

    TH1F* hNLLDist = new TH1F("hNLLDist", "NLL Distribution", 100, minNLL, maxNLL);
    for (double val : nllValues) {
        hNLLDist->Fill(val);
    }

    TCanvas* c1 = new TCanvas("c1", "NLL Consistency Check", 800, 600);
    hNLLDist->GetXaxis()->SetTitle("NLL");
    hNLLDist->GetYaxis()->SetTitle("Frequency");
    hNLLDist->Draw();

    TLine* line = new TLine(dataNLL, 0, dataNLL, hNLLDist->GetMaximum());
    line->SetLineColor(kRed);
    line->SetLineWidth(2);
    line->Draw("same");

    std::cout << "Red line shows data NLL over toy distribution." << std::endl;
}