# RouterSense Interview Task Submission

**Candidate:** Naman Singh  
**Project:** RouterSense — Smart Health Monitoring Using Network Data and Machine Learning  
**Submission Scope:** Q1 — App Evaluation and Data Collection, with supporting artifacts prepared for downstream Q2 use

---

## Overview

This repository contains my solution for **Q1: App Evaluation and Data Collection** from the RouterSense interview task. The goal of Q1 is to evaluate a provided list of iOS and Android apps and compile the findings into a CSV with additional fields relevant to identifying and studying **AI companion platforms**. The required fields include app classification, website accessibility, login requirements, age verification, subscription constraints, and supported languages. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1}

The task emphasizes making strong use of AI agents while also **verifying outputs carefully**. My workflow reflects that requirement: I used AI-assisted processing and dataset construction, but preserved a structure that supports manual verification for fields that cannot be reliably inferred from store metadata alone. :contentReference[oaicite:2]{index=2}

---

## What I Did

I completed the following work for Q1:

- Parsed the provided **App Store** and **Google Play** JSON datasets
- Extracted core metadata for each app into a structured tabular format
- Unified iOS and Android records into a single combined dataset
- Added all Q1-required output fields from the task instructions
- Generated a first-pass classification and metadata enrichment pipeline
- Produced two CSV outputs:
  - a **full augmented union dataset**
  - a **submission-oriented draft dataset**
- Prepared a Jupyter notebook that reproduces the entire pipeline locally

This workflow is designed to make the dataset both:
- **traceable and reproducible**
- **easy to refine through manual verification**

---

## Input Files

The notebook expects the following input files in the **working directory**:

### 1. `app_store_apps_details.json`
This is the iOS/App Store dataset containing app metadata such as:
- title
- app ID
- description
- developer
- developer website
- content rating
- supported languages
- pricing metadata
- store URL

### 2. `google_play_apps_details.json`
This is the Android/Google Play dataset containing app metadata such as:
- title
- app ID
- description
- developer
- developer website
- content rating
- pricing / in-app purchase information
- store URL
- availability metadata

These two files are the raw data sources used to generate the final CSV outputs.

---

## Output Files

The notebook produces two main CSV files in the **current working directory**.

### 1. `q1_augmented_full_union.csv`
This is the **full combined dataset**.

It contains:
- all usable rows extracted from both the iOS and Android source files
- normalized fields from each store
- all Q1-required fields added as columns
- heuristic / first-pass enrichment wherever possible from the raw metadata

This file is best understood as the **master working dataset**.

Use this file if you want:
- the complete merged inventory
- the most information preserved from the raw inputs
- a base file for further filtering, manual checking, or analysis

### 2. `q1_submission_draft.csv`
This is the **submission-oriented draft**.

It is derived from the full augmented dataset and is intended to serve as the cleaner, more practical CSV for the Q1 deliverable. Depending on the filtering and formatting choices in the notebook, this file is the one I would treat as the main draft for professor submission after final manual verification.

Use this file if you want:
- a cleaner Q1-facing output
- a draft closer to the final deliverable
- a practical review sheet for manual corrections

---

## Meaning of the Required Q1 Fields

The task requires the following additional fields to be included in the CSV. :contentReference[oaicite:3]{index=3}

### `app_type`
Classifies the app as one of:
- `companion`
- `general_purpose`
- `mixed`
- `other`

Interpretation used:
- `companion`: primarily social, relational, emotional, roleplay, boyfriend/girlfriend/friend style interaction
- `general_purpose`: broad assistant or LLM-style utility
- `mixed`: combines both companion and broad-assistant functionality
- `other`: does not fit the above categories

### `web_accessible`
Whether the app can be meaningfully interacted with through a website.

Important distinction:
- `True` means the AI/chat experience is actually usable on the web
- `False` means the website is only a landing page or marketing site

### `web_url`
The interactive web URL, if applicable.

### `login_required`
Whether login is required to meaningfully interact with the AI.

Interpretation used:
- `True` if login is required immediately or after only a very small number of messages
- `False` only if longer usage is possible without login

### `login_methods`
Examples:
- email/password
- Google
- Apple
- Facebook
- TikTok

### `age_verification_required`
Whether the platform enforces any age gate.

### `age_verification_method`
Examples:
- self-declaration
- date-of-birth gate
- ID upload

### `subscription_required_for_long_chat`
Whether a paid plan is needed to sustain long conversations at scale.

### `all_features_available_without_subscription`
Whether all important/core features are available on the free tier.

### `subscription_features`
Examples:
- unlimited messaging
- premium characters
- longer memory
- faster responses
- voice features
- NSFW unlocks
- premium media generation

### `subscription_cost`
Monthly subscription cost, including currency where known.

### `languages_supported`
Languages visibly supported by the platform interface or listing.

---

## What Was Automated vs. What Still Requires Manual Verification

A key part of my solution is distinguishing between:

- fields that can be reasonably inferred from structured metadata
- fields that require **live product verification**

### Automated / first-pass fields
These can often be estimated from app title, description, content rating, pricing metadata, language lists, developer website, and store metadata:
- app title / platform / developer / store link
- app_type
- possible website presence
- likely subscription presence
- listed languages
- pricing hints from store metadata

### Fields that still require manual verification
These cannot always be determined reliably from store JSON alone:
- whether the website is actually interactive
- exact login gating behavior
- exact login methods available on the live site
- exact age verification mechanism
- whether a subscription is specifically required for very long chats
- which features are truly restricted behind paywalls

Because of this, the generated CSV should be treated as a **strong draft**, not as a claim that every live-site behavioral field has already been perfectly verified.

---

## Methodology

My approach for Q1 was:

1. Read both raw JSON files
2. Flatten and normalize important metadata fields from iOS and Android records
3. Merge both inventories into one union dataset
4. Add the required Q1 columns
5. Use structured heuristics to generate a first-pass classification
6. Save:
   - one master dataset
   - one submission-oriented draft
7. Leave room for manual auditing of fields that depend on live platform behavior

This balances:
- speed
- reproducibility
- transparency
- honesty about uncertainty

---

## Reproducibility

The full pipeline is contained in the Jupyter notebook:

- `q1_revised_full_solution.ipynb`

To reproduce the outputs:

1. Place these files in the same working directory:
   - `app_store_apps_details.json`
   - `google_play_apps_details.json`
   - `q1_revised_full_solution.ipynb`

2. Open the notebook locally

3. Run all cells

4. The notebook will save:
   - `q1_submission_draft.csv`
   - `q1_augmented_full_union.csv`

in the **current working directory**

---

## Recommended Final Review Before Submission

Before sending the CSV to the professor, I recommend manually checking the most important uncertain fields for the top candidate platforms:

- `web_accessible`
- `web_url`
- `login_required`
- `login_methods`
- `age_verification_required`
- `age_verification_method`
- `subscription_required_for_long_chat`
- `all_features_available_without_subscription`
- `subscription_features`
- `subscription_cost`

A practical strategy is:
- sort/filter the draft CSV by apps most likely to be relevant
- visit their websites directly
- update the uncertain fields
- then submit the corrected version

---

## Notes on AI Usage

This task explicitly encouraged the use of AI agents, while also stating that the candidate is responsible for verifying outputs. :contentReference[oaicite:4]{index=4}

I used AI assistance for:
- structuring the workflow
- building the data-processing notebook
- defining classification logic
- generating draft output fields
- organizing the final deliverables

At the same time, I preserved a workflow that makes it easy to:
- inspect assumptions
- verify uncertain entries manually
- revise app-level fields based on direct platform behavior

---

## Repository Contents

Typical relevant files in this repository:

- `q1_revised_full_solution.ipynb`
- `app_store_apps_details.json`
- `google_play_apps_details.json`
- `q1_augmented_full_union.csv`
- `q1_submission_draft.csv`
- `README.md`

---

## Final Summary

In short, this repository contains a reproducible Q1 pipeline that:

- ingests the provided iOS and Android app datasets
- builds a unified app evaluation dataset
- adds all task-required Q1 fields
- generates both a full master dataset and a submission-oriented draft
- supports manual verification for live-site-dependent fields

This gives a practical and scalable foundation for selecting candidate AI companion platforms for further evaluation and downstream automation work in Q2. :contentReference[oaicite:5]{index=5}
