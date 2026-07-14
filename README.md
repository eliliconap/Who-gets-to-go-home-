
# Who Gets to Go Home?
### A Health Equity Analysis of 30-Day Hospital Readmissions in Charlotte-Mecklenburg

## The Story Behind This Project

My grandmother survived COVID-19 in 2020. Her experience navigating 
the healthcare system as an elderly Hispanic woman made me want to 
understand a pattern hiding in plain sight — who gets discharged 
before they are truly ready, and why do so many of them come back 
within 30 days?

This project started personal. The data made it undeniably real.

---

## The Data Problem

Real patient data is protected under HIPAA. Additionally, CMS 
suspended readmission tracking for the first half of 2020 to protect 
hospitals from financial penalties during the pandemic — which erased 
the exact data needed to study how vulnerable families were left 
behind during that crisis.

Instead of stopping there, I engineered a hybrid dataset of 6,845 
individual patient records anchored directly to real FY 2026 CMS 
Hospital Performance baselines for five Charlotte-Mecklenburg hospitals:

- Carolinas Medical Center
- Novant Health Presbyterian Medical Center
- Atrium Health Pineville
- Carolinas Medical Center Behavioral Health
- Atrium Health University City

---

## Project Journal 

**How it was built**

I started by sourcing the most recent Charlotte-Mecklenburg HRRP data 
available. Almost immediately I discovered that CMS had no recorded 
COVID readmission data for 2020. They made this decision deliberately 
to avoid penalizing hospitals during the pandemic chaos — which was 
understandable from a policy standpoint, but it erased exactly the 
data needed to study how vulnerable families were being left behind 
during that same period.

**Pivoting to Engineered Data**

Rather than stopping at the data gap, I pivoted to building a hybrid 
synthetic dataset. This approach actually showcases more analytical 
skill than using a clean pre-built dataset — it required me to 
understand the real data deeply enough to simulate it responsibly. 

I combined the FY 2026 CMS Hospital Readmissions data with engineered 
patient-level records, anchoring each simulated patient to real 
hospital performance benchmarks. The result was a dataset I could 
clean, manipulate, and model — while remaining transparent about its 
synthetic nature.

**Hitting Errors and Learning From Them**

I ran into significant errors getting the code to run correctly. My 
first mistake was assuming "City" was a column in the CMS dataset — 
it was not. I learned the hard way to never skip the basics and always 
understand what your data is actually telling you before writing a 
single line of analysis code.

Other issues I resolved:

- Replaced Measure ID with Measure Name — the dataset used an 
  alphanumeric ID that needed to be mapped to readable diagnostic titles
- Standardized dictionary keys to include the specific `-HRRP` suffix 
  used by federal reporting systems
- Removed a duplicate NC filter that was causing the dataset to return 
  empty results — I had filtered to North Carolina twice without 
  realizing it

What I had at the end of this stage was the real-world framework — 
actual discharge volumes and Excess Readmission Ratios for each 
anchor hospital pulled directly from CMS.

**Data Integrity and the Equity Audit**

At this stage I ran a full data integrity check confirming no null 
values remained after cleaning. I identified and imputed 147 missing 
medication dosage data points using condition-specific medians — 
choosing median over mean to protect against outliers skewed by 
extreme medical cases.

The equity audit produced the following variables:

| Variable | Description |
|----------|-------------|
| Race_Ethnicity | Four demographic groups reflecting Charlotte health dynamics |
| Total_Patients | Patient count per racial group |
| Avg_Length_of_Stay | Days in hospital before discharge papers were issued |
| Avg_Med_Dosage | Dosage in MG — used to surface deviations from clinical norms |
| Readmission_Rate | Binary — 1 if readmitted within 30 days, 0 if not |

I also calculated a system-wide baseline excluding all demographic 
factors — race, zip code, insurance type — to establish what the 
average patient experience looks like without any segmentation. This 
baseline became the benchmark every demographic finding is measured against.
---

## Key Findings

| Finding | Black Patients | White Patients |
|---------|---------------|----------------|
| 30-Day Readmission Rate | 64% | 31% |
| Average Length of Stay | 2.49 days | 3.41 days |
| Average Medication Dosage | 35mg | 50mg |
| Follow Up Scheduled | 41% | 68% |

**Geographic Finding:**
Charlotte's historic Crescent corridor carries a 0.62 readmission 
burden versus 0.21 in the Wedge — a gap driven by decades of 
disinvestment, pharmaceutical deserts, and limited primary care access.

---

## The Conclusion

This is not one problem. It is four compounding failures — early 
discharge, undertreated symptoms, no follow up safety net, and a 
neighborhood that cannot catch you when you fall. Fix one and the 
others remain. The data does not suggest incremental improvement. 
It suggests systemic intervention.

---

## Policy Recommendations

**Finding 1 — Equity-Conditioned Discharge**
Mandate standardized clinical stabilization windows for high-risk 
chronic conditions that explicitly adjust based on the patient's 
available home care infrastructure.

**Finding 2 — Warm Hand-off Navigators**
Deploy hospital-funded bilingual Patient Navigators tasked with 
scheduling and securing transportation for a primary care check-in 
within 7 days of discharge.

**Finding 3 — Transitional Courier Care**
Establish partnerships supplying 30 days of free, hospital-couriered 
prescription delivery directly to high-risk residential zip codes.

---

## Tools Used

- Python — Pandas, NumPy
- Power BI
- CMS FY 2026 Hospital Readmissions Reduction Program Data
- NC DHHS Public Health Data

---

## Files in This Repository

- `Health_Disparities.py` — Full Python analysis and dataset engineering
- `FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv` — Original CMS data
- `charlotte_healthcare_disparities_dataset.csv` — Engineered hybrid dataset

---

## View the Interactive Dashboard

[Click here to view the Power BI Dashboard](https://app.powerbi.com/reportEmbed?reportId=5c92c67e-a89b-451c-8f38-73cf9113a63c&autoAuth=true&ctid=88d59d7d-aecb-41b2-90c5-55595de02536)

---

## Author

**Eli Licona** — Data Analyst · Charlotte, NC  
[Portfolio](https://eliliconap.github.io/Eli-Licona-Portfolio) · 
[GitHub](https://github.com/eliliconap)
