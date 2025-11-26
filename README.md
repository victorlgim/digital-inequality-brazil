# Digital Inequality in Brazil  
Quantitative analysis of Brazil’s digital divide using connectivity indicators, inequality metrics, regression modeling and clustering.

---

## Overview  
Digital connectivity in Brazil is not evenly distributed.  
It follows geography, economics and historical investment patterns, creating structural asymmetries between municipalities and regions. This project investigates how infrastructure, competition, and territorial conditions shape digital inequality from 2021 to 2024.

Using public telecom datasets (IBC indicators from Anatel via Base dos Dados), this study builds an end-to-end analytical pipeline including:

- Exploratory data analysis (EDA)  
- Statistical inequality metrics (Gini, Lorenz)  
- OLS regression modeling to explain IBC  
- K-Means clustering to identify structural profiles  
- Temporal analysis to measure whether inequality increases over time  
- Data engineering and reproducible notebooks

The goal is to reveal **how infrastructure gaps translate into digital exclusion**, and to quantify their impact across the Brazilian territory.

---

## Key Findings  
- Municipalities with no fiber backhaul show dramatically lower connectivity levels.  
- Digital inequality is persistent and structurally tied to region and population density.  
- K-Means clustering reveals three “digital profiles”: Critical, Intermediate and High Connectivity.  
- The digital divide widened between top 10% and bottom 10% municipalities from 2021–2024.  
- Competition (HHI) influences speed of improvement but does not overcome lack of infrastructure.

These insights show that digital inequality is both **territorial and infrastructural**, not merely socioeconomic.

---

## Data Sources  

**Primary dataset:**  
Anatel - Índice Brasileiro de Conectividade (IBC)  

Available via Base dos Dados:

- Telecom connectivity indicators  
- Infrastructure presence (fiber, mobile stations)  
- Coverage (4G/5G)  
- Market competition (HHI for SMP/SCM)  
- Municipal and state directories

Period: **2021–2024**

---

## Pipeline Steps  

### 1. Extraction  
SQL query extracts all relevant indicators, joining with municipal and UF directories.

### 2. Processing  
`data_prep.py` generates:

- cleaned dataset  
- region attribution (N, NE, SE, S, CO)  
- fiber categories (none/partial/full)  
- annual IBC deciles  
- numeric type normalization  
- missing value handling

### 3. Exploratory Data Analysis  
- distribution analysis  
- regional boxplots  
- correlation matrix  
- variable relationships

### 4. Inequality Metrics  
Using custom utilities in `src/utils/`:

- Gini coefficient  
- Lorenz curve  
- inequality comparison by region, fiber, HHI  
- long-tail density distribution

### 5. Regression Modeling  
OLS model:
```
ibc ~ coverage_4g5g + density_smp + density_scm + hhi_smp + hhi_scm + stations_density + C(fiber_cat) + C(region) + C(year)
```
Outputs:

- coefficients  
- standard errors  
- p-values  
- model fit  
- interpretation of causal structure  

### 6. Clustering  
K-Means segmentation identifies structural connectivity profiles:

- Critical Connectivity  
- Intermediate Connectivity  
- High Connectivity  

Includes silhouette scoring, centroid interpretation and regional cross-analysis.

### 7. Temporal Analysis  
Measures whether inequality shrinks or widens across years:

- IBC deciles  
- top 10% vs bottom 10% gap  
- temporal barplots and trends  

---

## How to Run  

### 1. Install dependencies  
```
pip install -r requirements.txt
```

### 2. Prepare the dataset  

```
python src/data_prep.py
```

### 3. Execute notebooks  

Open Jupyter or VSCode:

```
notebooks/01_eda.ipynb
notebooks/02_inequality.ipynb
notebooks/03_ibc_modeling.ipynb
notebooks/04_clustering.ipynb
notebooks/05_temporal_analysis.ipynb
```
---

## Technologies Used  
- Python 3.12+
- Pandas, NumPy  
- Matplotlib, Seaborn  
- Statsmodels  
- Scikit-Learn  
- Geopandas (optional)  
- BigQuery
- Jupyter Notebooks  

---

## Goals of This Project  
- Provide a reproducible, data-driven understanding of Brazil’s digital divide.  
- Demonstrate advanced statistical reasoning applied to telecom infrastructure.  
- Build an engineering-friendly project structure with clear separation of concerns.  
- Produce visual, interpretable outputs for policymakers and researchers.  

---

## Discussion & Insights  
For those who want a more narrative and contextual view of the results, I published an article on Medium delving deeper into the patterns observed in the study:

**Medium:**  
[Radiografia da Conectividade no Brasil (2021–2024)](https://medium.com/@uyamdlay/apesar-do-avan%C3%A7o-dos-dados-m%C3%B3veis-e-da-expans%C3%A3o-da-fibra-o-acesso-digital-se-concentra-onde-o-4a12772859c0)



## Author  
Developed by Victor L.  
For contact or discussion: GitHub Issues or LinkedIn.


---