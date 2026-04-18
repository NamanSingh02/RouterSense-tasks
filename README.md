# RouterSense Interview Task Submission

**Candidate:** Naman Singh  
**Project:** RouterSense — Smart Health Monitoring Using Network Data and Machine Learning  
**Faculty:** Danny Yuxing Huang  
**Submission Scope:** Q1 and Q2

---

## Overview

This repository contains my submission for the RouterSense interview task. The work is divided into two parts:

- **Q1: App Evaluation and Data Collection**
- **Q2: Automation Approach and Proof of Concept**

The overall goal of the assignment was to evaluate AI companion platforms, identify candidate systems for deeper study, and demonstrate a practical automation workflow for interacting with one selected platform.

This repository is organized to support both:
- **reproducibility**
- **manual verification**

I made strong use of AI assistance during the process, while also verifying outputs and iteratively refining the implementation where needed.

---

## Repository Structure

```text
.
├── Q1/
│   ├── q1_revised_full_solution.ipynb
│   ├── q1_submission_draft.csv
│   ├── q1_augmented_full_union.csv
│   ├── app_store_apps_details.json
│   ├── google_play_apps_details.json
│   └── README.md
│
├── Q2/
│   ├── q2_playwright_kindroid_poc.py
│   ├── q2_messages.txt
│   ├── q2_output_responses.csv
│   ├── screenshots/
│   ├── Demo.mp4
│   ├── q2_RUN_STEPS.md
│   └── README.md
│
└── README.md
```



---

## Q1 Summary

Q1 focuses on **evaluating a provided list of iOS and Android apps** and constructing a dataset that helps determine which platforms qualify as AI companion apps and which are suitable for further study.

### What was done in Q1

- parsed the provided **App Store** and **Google Play** datasets
- extracted app metadata into a structured format
- unified iOS and Android rows into one combined dataset
- added all required Q1 fields
- generated a first-pass classification and enrichment workflow
- produced:
  - a **submission draft CSV**
  - a **full augmented union CSV**
- documented the methodology in a notebook and README

### Main Q1 outputs

- `q1_submission_draft.csv`
- `q1_augmented_full_union.csv`

### Q1 purpose

Q1 builds the candidate platform inventory that can later support:
- platform selection
- manual verification
- downstream automation work
- ecosystem analysis

---

## Q2 Summary

Q2 focuses on **automating interactions with one selected AI companion platform**.

For the proof of concept, I selected **Kindroid** and implemented a **semi-automated browser automation workflow using Python and Playwright**.

### What was done in Q2

- selected Kindroid as a suitable web-accessible companion platform
- built a script that:
  - opens the site
  - waits for manual login
  - reads input prompts from a file
  - sends them one by one
  - captures the bot responses
  - saves those responses in CSV form
  - takes screenshots for traceability
- iteratively debugged and improved the script until it handled the live site reliably

### Main Q2 outputs

- `q2_playwright_kindroid_final.py`
- `q2_messages.txt`
- `q2_output_responses.csv`
- `screenshots/`
- `Demo.mp4`

### Q2 purpose

Q2 demonstrates a practical proof of concept for:
- automated message delivery
- structured response collection
- repeatable platform interaction
- future multi-platform scaling

---

## How Q1 and Q2 Fit Together

Q1 and Q2 are closely connected.

- **Q1** identifies and organizes the ecosystem of candidate platforms
- **Q2** demonstrates how one such platform can be automated in practice

Together, they show both:
- **data-oriented evaluation**
- **systems-oriented implementation**

This reflects the broader research workflow likely needed in the RouterSense project:
- identify relevant platforms
- characterize them carefully
- build robust tools for structured interaction and analysis

---

## Inputs

The repository uses the following main inputs.

### Q1 inputs

- `app_store_apps_details.json`
- `google_play_apps_details.json`

These contain raw app metadata from the iOS App Store and Google Play.

### Q2 inputs

- `q2_messages.txt`

This contains the prompts sent to the selected AI companion platform.

---

## Outputs

The repository produces the following main outputs.

### Q1 outputs

- `q1_submission_draft.csv`
- `q1_augmented_full_union.csv`

### Q2 outputs

- `q2_output_responses.csv`
- screenshots inside `screenshots/`
- demo video artifact

---

## Reproducibility

### Q1

To reproduce Q1:

1. Place the Q1 notebook and the two raw JSON files together
2. Open the notebook locally
3. Run all cells
4. Generate:
   - `q1_submission_draft.csv`
   - `q1_augmented_full_union.csv`

### Q2

To reproduce Q2:

1. Place the Q2 script and `q2_messages.txt` together
2. Create a Python virtual environment
3. Install Playwright
4. Run the script
5. Log in manually when prompted
6. Open the Kindroid chat/preview
7. Allow the script to send messages and capture responses

---

## Notes on AI Usage

This task explicitly encouraged the use of AI agents while also requiring careful verification.

I used AI assistance for:
- workflow design
- notebook and script generation
- iterative debugging
- draft documentation
- classification logic
- output structuring

At the same time, I manually checked outputs, refined assumptions, and iterated on failures, especially in Q2 where live browser automation required repeated debugging and adjustment.

---

## Key Engineering Takeaways

The most important lessons from this project were:

- browser automation on live websites is much more fragile than static examples suggest
- transcript-based extraction can be more reliable than simplistic bubble-based assumptions
- streaming responses require stabilization before saving
- incremental saving is important for robustness
- manual login can be a practical compromise for a proof of concept
- structured outputs and clear documentation are essential for research reproducibility

---

## Final Summary

This repository contains a complete submission for both Q1 and Q2 of the RouterSense interview task.

In summary, it demonstrates:

- a structured evaluation workflow for AI companion apps
- a reproducible data-processing pipeline for Q1
- a practical browser automation proof of concept for Q2
- iterative debugging and refinement of a live automation workflow
- clear documentation for review and reproduction

Taken together, these materials show a combination of:
- systems thinking
- data pipeline design
- practical automation
- debugging discipline
- research-oriented documentation
