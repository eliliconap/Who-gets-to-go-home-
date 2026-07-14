import pandas as pd
import numpy as np


# Step I: Load and clean the raw CMS data
# pulling the official government file and immediately cleaning up the column headers.
# raw files always have trailing spaces, so stripping them first keeps us safe from errors.

cms_data = pd.read_csv("/Users/elilicona/Downloads/PortfolioProjects/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv")
cms_df = pd.DataFrame(cms_data)
cms_df.columns = cms_df.columns.str.strip()  

# Filtering down to North Carolina hospitals so we can focus our scope
nc_hospitals_df = cms_df[cms_df['State'] == 'NC'].copy()  


# Step II: Define hospital targets and map clinical codes
# The CMS dataset uses complex diagnostic codes ending in '-HRRP'. 
# This dictionary maps those codes to clean, plain-English titles for our final visuals.

measure_map = {
    'READM-30-AMI-HRRP': 'Readmission Rate - Heart Attack',
    'READM-30-HF-HRRP': 'Readmission Rate - Heart Failure',
    'READM-30-PN-HRRP': 'Readmission Rate - Pneumonia',
    'READM-30-COPD-HRRP': 'Readmission Rate - COPD'
}       

# Isolating Charlotte's primary healthcare systems (Atrium and Novant networks)
# This lets us run a hyper-local clinical equity audit on our own city.

clt_hospital_keywords = [
    'CAROLINAS MEDICAL CENTER', 
    'PRESBYTERIAN MEDICAL CENTER', 
    'PINEVILLE', 
    'UNIVERSITY CITY'
]

clt_mask = nc_hospitals_df['Facility Name'].str.upper().str.contains('|'.join(clt_hospital_keywords), na=False)
clt_cms = nc_hospitals_df[clt_mask].copy()  

# Filter down to just the target diagnoses we mapped above
clt_cms = clt_cms[clt_cms['Measure Name'].isin(measure_map.keys())].copy()
clt_cms['Clean Metric Title'] = clt_cms['Measure Name'].map(measure_map)


# Step III: Sanitize data types and handle CMS specific edge cases
# We force these to NaN (empty values) so we can run calculations without crashing.

clt_cms['Number of Discharges'] = pd.to_numeric(clt_cms['Number of Discharges'], errors='coerce')
clt_cms['Excess Readmission Ratio'] = pd.to_numeric(clt_cms['Excess Readmission Ratio'], errors='coerce')

# Drop missing values to ensure our baseline calculation is perfect
clt_cms = clt_cms.dropna(subset=['Number of Discharges', 'Excess Readmission Ratio'])

print(f"Compressed local records found: {len(clt_cms)} unique hospital-illness benchmarks.")
print("\nHospitals included in your Charlotte baseline:")
print(clt_cms['Facility Name'].unique())


# Step IV: Expand hospital summaries into patient level records
# This is where the magic happens. We're taking aggregated hospital stats and 
# reconstructing individual patient rows to model granular clinical patterns.

print("\nExpanding hospital summaries into individual patient-level records...")
patient_records = []

for _, row in clt_cms.iterrows():
    hospital_name = row['Facility Name']
    diagnosis_clean = row['Clean Metric Title']
    discharge_count = int(row['Number of Discharges'])
    real_err = float(row['Excess Readmission Ratio'])
    
    for i in range(discharge_count):
        
        # Demographic distribution modeling actual Charlotte population baselines
        race = np.random.choice(["White", "Black", "Hispanic", "Asian"], p=[0.53, 0.32, 0.10, 0.05])
        payer = np.random.choice(["Private", "Medicare", "Medicaid"], p=[0.30, 0.50, 0.20])
        
        # Charlotte's Crescent vs. Wedge Geographic (Important for later in the audit)
        # Minority and Medicaid-covered cohorts statistically cluster in Crescent zip codes,
        # while private-payer cohorts map heavily to the Wedge.
        if race in ["Black", "Hispanic"] or payer == "Medicaid":
            zip_code = np.random.choice(["28216", "28208", "28205", "28212"], p=[0.4, 0.3, 0.2, 0.1])
            geographic_zone = "Crescent"
        else:
            zip_code = np.random.choice(["28277", "28211", "28226", "28202"], p=[0.4, 0.3, 0.2, 0.1])
            geographic_zone = "Wedge"
            
        # Modeling early discharge pressures (Length of Stay)
        # Crescent patients show historical trends of shorter stays (1.2 days fewer) 

        base_los = 5 if "Heart Failure" in diagnosis_clean else (4 if "Pneumonia" in diagnosis_clean else 3)
        if geographic_zone == "Crescent":
            los = max(1, int(np.random.normal(base_los - 1.2, 1.0)))
        else:
            los = max(1, int(np.random.normal(base_los, 1.1)))
            
        # Simulating clinical treatment disparities (Medication Dosage)
        # Accounting for documented historical under-prescribing trends in minority groups.
        base_dosage = 50.0 
        if race == "Black":
            dosage = round(max(10.0, np.random.normal(base_dosage - 15.0, 7.5)), 1)
        elif race == "Hispanic":
            dosage = round(max(10.0, np.random.normal(base_dosage - 7.0, 7.5)), 1)
        else:
            dosage = round(max(10.0, np.random.normal(base_dosage, 5.0)), 1)
            
        # Simulating post-discharge care transition barriers
        # Crescent-area patients face higher transportation and scheduling hurdles.
        if geographic_zone == "Crescent":
            follow_up = np.random.choice([1, 0], p=[0.42, 0.58]) 
        else:
            follow_up = np.random.choice([1, 0], p=[0.76, 0.24])
            
        # Compound Risk Calculation (Anchored directly to the hospital's real official ERR)
        # We start with the hospital's real performance, then apply penalties for systemic barriers.
        risk_score = (real_err - 1.0) * 2.5
        if los < 3: risk_score += 1.6          
        if dosage < 35.0: risk_score += 1.9       
        if follow_up == 0: risk_score += 2.2      
        if geographic_zone == "Crescent" and payer == "Medicaid": risk_score += 1.2 
        
        # Compressing our cumulative risk score into a clean 0-1 probability curve
        prob_readmit = 1 / (1 + np.exp(-(risk_score - 2.4)))
        readmitted = np.random.choice([1, 0], p=[prob_readmit, 1 - prob_readmit])
        
        patient_records.append({
            "Hospital_Name": hospital_name,
            "Condition": diagnosis_clean,
            "Race_Ethnicity": race,
            "Insurance_Payer": payer,
            "Zip_Code": zip_code,
            "Geographic_Zone": geographic_zone,
            "Length_of_Stay_Days": los,
            "Med_Dosage_MG": dosage,
            "Follow_Up_Scheduled": follow_up,
            "Readmitted_30_Days": readmitted,
            "Real_Hospital_ERR": real_err  
        })

# Creating our final structured dataset
hybrid_df = pd.DataFrame(patient_records)

# Deliberately planting 2% missing values to showcase our data cleaning skills in Step 5
hybrid_df.loc[hybrid_df.sample(frac=0.02).index, 'Med_Dosage_MG'] = np.nan

# Save the master dataset locally
hybrid_df.to_csv("charlotte_healthcare_disparities_dataset.csv", index=False)

print(f"SUCCESS! New dataset compiled with {len(hybrid_df)} patient rows.")


# Step V: Clean the synthetic data and run the final equity audit
# Reloading the data to test our end-to-end cleaning and analysis pipeline.

df = pd.read_csv("charlotte_healthcare_disparities_dataset.csv")

print("--- Step one: Initial Data Integrity Check ---")
print(df.isnull().sum())

# Resolving missing medication data using group-by medians.
# Grouping by condition is essential—COPD and Heart Failure use totally different dosage scales.

df['Med_Dosage_MG'] = df.groupby('Condition')['Med_Dosage_MG'].transform(lambda x: x.fillna(x.median()))

print("\n--- After Cleaning: Missing Values Remaining ---")
print(f"Missing values in Med_Dosage_MG: {df['Med_Dosage_MG'].isnull().sum()}")

print("\n--- Step two: The Equity Disparity Audit ---")

# Aggregating by demographic cohort to isolate operational performance gaps
disparity_audit = df.groupby('Race_Ethnicity').agg(
    Total_Patients=('Readmitted_30_Days', 'count'),
    Avg_Length_of_Stay=('Length_of_Stay_Days', 'mean'),
    Avg_Med_Dosage=('Med_Dosage_MG', 'mean'),
    Readmission_Rate=('Readmitted_30_Days', 'mean')
).reset_index()

# Polishing the metric formats for executive dashboard reporting
disparity_audit['Readmission_Rate'] = (disparity_audit['Readmission_Rate'] * 100).round(2).astype(str) + '%'
disparity_audit['Avg_Length_of_Stay'] = disparity_audit['Avg_Length_of_Stay'].round(2)
disparity_audit['Avg_Med_Dosage'] = disparity_audit['Avg_Med_Dosage'].round(2)

print(disparity_audit.to_string(index=False))

print("\n--- System-Wide Baseline (Standard Without Race) ---")
# Calculating the flat baseline system averages used for our dashboard card callouts
overall_stay = df['Length_of_Stay_Days'].mean()
overall_med = df['Med_Dosage_MG'].mean()
overall_readmit = df['Readmitted_30_Days'].mean()

print(f"Standard Length of Stay: {round(overall_stay, 2)} days")
print(f"Standard Med Dosage:     {round(overall_med, 2)} MG")
print(f"Standard Readmit Rate:   {round(overall_readmit * 100, 2)}%")