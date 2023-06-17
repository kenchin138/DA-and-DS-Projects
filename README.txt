## Kaplan Meier and Cox Proportional Hazards Survival Analysis 

Originally developed in the medical field to determine survival rates of a patient, the method can be applied in most problems where the dependent variable is time. In real estate, survival analysis can be used to predict the time a property stays on market before selling. 

Experimental results from the literature show that survival analysis brings some advantages when compared to linear regression analysis. Because time to sale data is right censored, regression will be negatively biased for homes that stay on the market for a long time. Survival curves also offer descriptive quantitative views on the influence that specific house features have on the time on market.

This analysis will apply the two most popular survival modelling techniques, Kaplan-Meier and Cox Proportional Hazards, on real estate sales from Feb 2015. The goal of the analysis is to:

	1. To help to give a client an informed decision on pricing when given a desired time to sell
	2. Find suitable property features that can explain the time it takes for a property to sell

## Sources
The data was collected using Zillow API and cleaned prior to its use for this project. 
