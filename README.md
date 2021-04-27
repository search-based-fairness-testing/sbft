# SBFT: Search-Based Fairness Testing
SBFT is a fairness testing tool for regression-based AI software. It estimates the _fairness degree (D)_ of the system under test. Fariness degree is defined as follows.

Given an AI software system, the **fairness degree** is measured by the
maximum difference in the predicted values by the AI software for all
pairs of instances (*x*<sub>*i*</sub>,*x*<sub>*j*</sub>) that are
identical apart from the sensitive attribute, i.e.,
*x*<sub>*i*</sub><sup>*s*</sup> ≠ *x*<sub>*j*</sub><sup>*s*</sup>.

*D* = max<sub>∀*i*, *j*</sub>\|*y*<sub>*i*</sub>−*y*<sub>*j*</sub>\|; *x*<sub>*i*</sub><sup>*s*</sup> ≠ *x*<sub>*j*</sub><sup>*s*</sup>

# How to use SBFT?

