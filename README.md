# fits1

This exercise will begin to introduce non linear data fitting.  The examples will be based on the ROOT libraries.  Similar functionality for everything we see can be found in the numpy + scipy + lmfit + matplotlib modules. But the examples we will follow over the next few projects offer several advantages:
* far more natural histogramming tools
* completely automated fitting options ("one liners")
* convenient methods for defining custom functions and controlling the convergence of the fit
* detailed and consistent documentation
* and a low level interface to modify the objective function, running in fully optimized compiled code

You are welcome to modify the provided code for your projects and to use other packages.  Where applicable alternate examples will be included. 

* **fit1.C**: C++ function to generate random data according to a normal distribution with mean=20, sigma=10. <br> A fit is performed using the built in Gaussian model in ROOT.  Then the parameter values, their uncertainteis, and the p-value for the fit are extracted.  To run this code type ```root fit1.C``` or if you are already running ROOT, type ```.X fit1.C```  
* **fit1.py**: The same code using the python interface, run this example using ```python fit1.C```.
* For a contrast see **fit1mpl.py** for a version using matplotlib+scipy.  
* readhist.C(py):  Examples for reading the histogram files given in this example 
* ParamUnceratinties.ipynb : a guided tutorial towards most of what you will be coding in this week's exercise.
* LLexample.ipynb : a notebook giving an example for calculating (N)LLs
* TH1hist2Numpy.ipynb : an example for converting a ROOT histogram to numpy arrays

Note that from ROOT you can type ```new TBrowser()``` or in Python r.TBrowser() to get a graphical browser that allows you to look at what's contained in the TFiles.

Exercise 1: I wrote this one myself.
* Histograms are in the plot that "fit1a.C" creates, which is "result1.pdf".
* The standard deviation of the Mean from Fits is 0.358, and the mean value of the Error of Mean from Fits is 0.3251. We expect these numbers to be similar because for a Normal distribution (Gaussian), the standard deviation of the mean values should be equal to the average value of the uncertainty in the means.
* I did make a scatter plot of the chi-square probability as a function of the reduced chi-square, which is saved as "scatter_plot.pdf".

Exercise 2: I wrote this one myself.
* The results match expected values. After doing 1000 runs of 10 item histograms, we see that the mean values of each is about the same. However, since the chi-square method is not resistant to low statistics, it suffers from having very long non-zero tails. As such, its sigma is high. For the NLL method, we have a similar looking plot. However, there are tiny tails and the sigma is lower.
* NEED TO COME BACK TO FIGURE OUT THE ESTIMATED UNCERTAINTY IN THE FIT PARAMETERS!!!
* We expect both methods to yield the same uncertainty in the fit parameters. However, we see that is not the case. The uncertainty in the mean should be nearly equal to the value of sigma. For the chi-square method, the mean uncertainty in the fit was 29 yet sigma was 10.4; for NLL, it was 2.9 and 3.16. We see clearly that the NLL method is superior because the uncertainty in the fit parameters is much closer to the standard deviation of the data.
* To view plot of uncertainties, please look at the file "exercise_2_extra.pdf".

Exercise 3: I double checked my work with Tristen. I wrote this using Copilot.
* My code is in a file called nll_consistency_check.C. The estimated p-value is ~0.5; however, doing several runs yields values fluctuating between 0.44 and 0.47. Honestly, I had Copilot write this whole part of the exercise.

Exercise PHYS 5630 Only: I also did this with Copilot
* For NLL: Fitter-reported error on mean is 2.0878. NLL scan error on mean is 1.8978. 
* For chi-square: Fitter-reported error on mean is 0.3326. Chi-square scan error on mean is 0.1955.
* We see that the NLL and chi-square methods provide similar results to the fitter. This indicated they're likely consistent with each other, which is expected.