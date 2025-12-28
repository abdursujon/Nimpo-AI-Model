# Nimpo – Data Readiness & Quality Intelligence Platform

## 1. Purpose

Nimpo is an AI system that determines whether a dataset is **fit for production use**, **model training**, or **decision-making**, and recommends corrective actions.

Nimpo does **not** predict business outcomes.  
It predicts **data quality, risk, and readiness**.

---

## 2. Real-World Problem Being Solved

In production:
- Bad data silently breaks models
- Engineers waste time manually inspecting datasets
- Models degrade due to drift and hidden data issues

Nimpo automates:
- Dataset inspection
- Quality scoring
- Risk detection
- Remediation guidance
- Drift awareness

This is a real problem in:
- ML platforms
- Data engineering teams
- AI pipelines
- Enterprise analytics

---

## 3. Core Responsibility of Nimpo

Given a dataset, Nimpo must answer:

1. Is this dataset usable?
2. What is wrong with it?
3. How risky is it?
4. How does it compare to previous datasets?
5. What should be done next?

---

## 4. High-Level Architecture

- **Spring API** → deterministic analysis + feature extraction
- **Nimpo Model** → learns from those features and predicts outcomes

The API produces **numbers and metadata**.  
The model produces **decisions and recommendations**.

---

## 5. Primary Outputs of Nimpo

- Dataset quality score (1-10)
- Issue classification (labels)
- Risk indicators
- Recommended remediation actions
- Drift indicators
- Confidence score

Example:
```json
{
  "qualityScore": 6,
  "riskLevel": "MEDIUM",
  "issues": ["HIGH_NULL_RATE", "SCHEMA_INSTABILITY"],
  "recommendations": ["IMPUTE_COLUMNS", "DROP_LOW_VALUE_COLUMNS"],
  "driftDetected": true
}
