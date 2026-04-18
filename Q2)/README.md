# Q2: Automation Approach and Proof of Concept

**Candidate:** Naman Singh  
**Chosen platform:** Kindroid: Your Personal AI  
**Approach:** Semi-automated web automation using Python + Playwright

---

## Overview

This submission addresses **Q2: Automation Approach and Proof of Concept** from the RouterSense interview task.

The goal of Q2 is to demonstrate a workflow that can:

- take a list of input messages
- send them to an AI companion platform
- capture the responses
- save those responses in a structured output file

For this proof of concept, I selected **Kindroid** as the target platform and implemented a **browser automation approach using Python and Playwright**.

---

## Chosen Platform

I selected **Kindroid** as the platform for the proof of concept.

### Why I selected Kindroid

I selected Kindroid because:

- it appears in the provided app datasets for both iOS and Android
- it clearly markets itself as a personal AI / AI companion platform
- it has a live web product in addition to mobile apps
- it supports authentication on the web
- it is suitable for browser automation as a proof of concept

This makes it a strong candidate for a web-based automation PoC.

---

## Brief Description of the Chosen Approach

I implemented a **semi-automated web automation proof of concept using Python and Playwright**.

The workflow:

- opens the Kindroid website in a browser
- allows a manual login step
- loads a predefined list of input messages from a file
- sends those messages one by one
- captures the bot responses
- saves outputs into a CSV file
- captures screenshots during execution for traceability

### What “semi-automated” means here

The script automates:

- opening the site
- waiting for the user to complete login if needed
- reading input messages from a file
- sending messages one by one
- detecting the assistant response
- saving structured outputs
- capturing screenshots

The script does **not** fully automate credential entry or account creation. Instead, it uses a **manual login step**, which is a practical design choice because many live platforms use OAuth flows, anti-bot protections, session checks, or captchas.

---

## Why I Believe This Approach Is Effective

I believe this approach is effective because:

- web automation is easier to prototype and validate than full iOS/Android automation
- Playwright works well with modern JavaScript-heavy websites
- manual login reduces fragility in authentication flows
- the rest of the workflow remains fully scriptable
- it provides structured, auditable outputs suitable for research workflows

This proof of concept focuses on the key operational need:  
**reliably automating repeated interactions after a session has been established.**

---

## Why I Believe This Approach Is Scalable

This approach is also scalable because the same architecture can be generalized across multiple platforms.

The core workflow remains the same:

- open platform
- establish or reuse session
- send message
- wait for response
- extract reply
- save structured output

To extend this to multiple platforms, the main changes would be:

- platform-specific selectors
- platform-specific session/login handling
- per-platform retry logic
- per-platform response extraction rules

A more advanced version could store these platform-specific details in configuration files, allowing the same automation engine to work across many AI companion websites.

---

## Methodology

The Q2 PoC works as follows:

1. Launch a browser through Playwright
2. Open the Kindroid website
3. Wait for the user to log in manually and open a chat/preview page
4. Read at least 10 input messages from `q2_messages.txt`
5. Send each message one at a time
6. Wait until the bot response finishes streaming and stabilizes
7. Save the response to a CSV file
8. Capture a screenshot after each completed interaction
9. Keep the browser open at the end for manual inspection

This design prioritizes:

- reproducibility
- practical robustness
- ease of demonstration
- suitability for a fast proof of concept

---

## Input Files

The script expects the following input file:

### `q2_messages.txt`

This file contains the list of input messages, one per line.

Example format:

- Hello.
- How are you feeling today?
- What do you like talking about most?
- Can you ask me a thoughtful question?
- What helps someone feel less lonely?
- Tell me a short story in three sentences.
- What do you remember from our conversation so far?
- How would you respond if I said I had a stressful day?
- Can you suggest one calming activity for tonight?
- Please summarize our conversation in two sentences.

Each non-empty line is treated as one prompt to send to the chatbot.

---

## Output Files

The script generates the following outputs:

### `q2_output_responses.csv`

This is the main structured output file.

It contains:

- `message_index`
- `input_message`
- `bot_response`
- `timestamp_utc`

This CSV is the key Q2 result because it shows that the automation successfully:
- accepted a list of prompts
- sent them to the target platform
- captured the platform’s responses
- stored them in a reusable format

### `screenshots/`

This directory stores screenshots captured during the run.

These screenshots provide:
- visual evidence that the automation worked
- traceability for the responses
- useful artifacts for the demo video and validation

---

## Files Included in the Q2 Package

This Q2 package includes:

- `q2_playwright_kindroid_poc.py`
- `q2_messages.txt`
- `q2_output_responses.csv` after running the script
- `screenshots/`
- `Demo.mp4`
- `q2_RUN_STEPS.md`
- This write-up


---

## Assumptions

This proof of concept assumes:

- the platform is accessible through the web
- the user can manually log in once the browser opens
- a chat page or preview page is reachable before the automation starts sending messages
- the page layout remains stable enough for selector-based interaction and transcript extraction
- the bot response can be detected from the visible transcript area

---

## Limitations

The main limitations are:

- login is not fully automated
- frontend selector changes may require script maintenance
- live websites may change UI behavior over time
- streaming replies can make response extraction more difficult
- browser automation is generally less robust than direct API access when APIs are available
- some sites may rate-limit or restrict automated behavior

These limitations are normal for a browser-based proof of concept and do not change the usefulness of the approach as an initial automation strategy.

---

## Development Notes: Bugs, Challenges, and How They Were Resolved

While building the Q2 proof of concept, the final working solution was reached through several iterations. This section documents the main issues encountered during development and how they were resolved.

### 1. Browser choice and automation environment

At the beginning, the script launched a Playwright-controlled browser window labeled something like **Chrome for Testing** instead of the normal personal browser.

#### Why this happened

Playwright launches its own controlled Chromium environment by default. This is normal behavior and is often more stable for automation than using a regular personal browser profile.

#### Resolution

I kept the default Playwright browser instead of switching to a personal browser profile. This reduced the risk of:

- profile lock issues
- extension interference
- cookie/session conflicts
- instability from personal browser state

This choice made the automation more reproducible and easier to demonstrate.

---

### 2. Messages were being sent, but bot responses were not being captured

One of the earliest issues was that the automation successfully opened the Kindroid page and sent messages, but the terminal output and CSV did not contain the chatbot’s replies.

#### Why this happened

The initial response extraction logic relied on broad page selectors such as generic `div` and `p` elements. On the Kindroid page, these selectors often matched:

- homepage text
- pricing text
- footer text
- large page-level containers

As a result, the script captured unrelated text such as:

- marketing content
- site branding
- subscription information

instead of the actual chatbot reply.

#### Resolution

The response extraction logic was redesigned to work from the **main visible transcript area** rather than generic page text. The revised approach:

- identified the main transcript container visually
- parsed the transcript into speaker turns
- ignored UI noise such as `Ember Preview`, `Kindroid`, and `Loading...`
- extracted only the latest assistant reply rather than the whole page text

This was the key fix that made response capture reliable.

---

### 3. The script falsely believed the message had not been sent

At one stage, the script threw errors saying that the user’s message had not appeared, even though the message was visibly present in the Kindroid transcript.

#### Why this happened

The earlier logic assumed that user messages would appear in a separate **right-side user bubble**. However, in the Kindroid preview layout being used, the page structure did not expose the message in that expected way for automation.

The script therefore checked the wrong part of the DOM and concluded that the message had not been sent.

#### Resolution

The send-verification logic was changed to verify message delivery by checking the **main transcript text** instead of looking for a right-side user bubble.

The revised logic:

- sent the message
- waited for the transcript to update
- verified whether the new user message appeared in the full conversation transcript

This made message delivery verification much more reliable.

---

### 4. The script sometimes failed after the first message

Another issue was that the first message could be sent successfully, but later messages were not always sent correctly.

#### Why this happened

The earlier version reused the textarea state from the previous iteration instead of safely re-locating the message input each time. Dynamic web apps often re-render input boxes after a message is submitted, which can make previously stored locators stale or unreliable.

#### Resolution

The `send_message` workflow was updated to:

- re-find the message input box on every loop iteration
- click it again
- clear it safely
- re-type the new message
- press Enter
- verify that the transcript changed

This made repeated multi-message interaction much more stable.

---

### 5. Bot replies were captured too early while they were still streaming

At a later stage, the script successfully captured replies, but they were often incomplete. Screenshots also showed only the first few lines of the assistant’s answer.

#### Why this happened

Kindroid streams its responses progressively. The early versions of the script saved the response as soon as a changed reply was detected, even though the model was still generating more text.

#### Resolution

A reply-stabilization mechanism was added.

The improved logic:

- waited until a new assistant reply appeared
- continued polling the reply
- only treated it as final when the text stopped changing for several seconds
- waited a little longer before taking the screenshot

This significantly improved both:

- the completeness of the saved response text
- the quality of the screenshots

---

### 6. Screenshots and CSV rows could be lost if a later step failed

During debugging, one failure could stop the loop before useful artifacts were saved.

#### Why this happened

Some earlier versions only saved outputs at the end or saved them too late in the loop. If a later check failed, partial progress was not always preserved.

#### Resolution

The script was updated to save incrementally:

- append each completed prompt-response pair immediately
- write the CSV after every successful message
- capture a screenshot after every successful message

This ensured that even partial runs still produced useful deliverables.

---

### 7. The terminal output became too noisy during debugging

At one point, the terminal contained a large amount of debug information, including element dumps and diagnostic output from many selectors.

#### Why this happened

Heavy debugging was necessary to understand how Kindroid’s page structure worked and why the initial selector logic failed.

#### Resolution

Once the extraction logic became stable, the terminal output was cleaned up. The final version restores a simpler and more readable format:

- `Sending message X/Y: ...`
- `Bot response:`
- the extracted assistant reply
- a separator line

This produced a cleaner demo and a more professional final run.

---

### 8. Browser-closing behavior at the end was inconvenient during debugging

The earlier script closed the browser automatically at the end, which made it harder to manually inspect the final page state.

#### Resolution

The final version keeps the browser open after completion and waits for user input before terminating the Python process. This made final inspection easier and improved the demo experience.

---

## Summary of Key Engineering Lessons

The main engineering lessons from building this PoC were:

- **Live websites are much messier than static examples.**  
  Browser automation often fails when it assumes a clean DOM structure.

- **Transcript-based extraction was more reliable than bubble-based extraction.**  
  The chatbot UI did not expose messages in the simple left/right DOM structure initially expected.

- **Streaming responses require stabilization logic.**  
  A response should not be captured the moment it first changes.

- **Incremental saving is important.**  
  Saving CSV rows and screenshots after each successful message makes the workflow more robust.

- **Manual login is a practical compromise for a PoC.**  
  Fully automating authentication would have made the system more fragile without adding much value for this task.

---

## Optional Extension to Multiple Platforms

A stronger multi-platform system could be built by defining a configuration for each platform containing:

- base URL
- login URL
- input box selectors
- send trigger method
- response selectors or transcript parsing rules
- wait/retry strategy
- optional session persistence behavior

The same Playwright engine could then be reused across different AI companion platforms with limited platform-specific adjustments.

Possible future enhancements include:

- persistent session storage
- configurable per-platform selector files
- structured logging
- HTML snapshot capture
- response latency measurement
- moderation/safety event logging
- failure recovery and retries

---

## Reproducibility

To reproduce the Q2 output:

1. Place the script and `q2_messages.txt` in the same folder
2. Create a Python virtual environment
3. Install dependencies:
   - `playwright`
   - `pandas` if needed
4. Run:
   - `python q2_playwright_kindroid_final.py`
5. Log in manually when prompted
6. Open or create the Kindroid chat/preview
7. Press Enter in the terminal
8. Allow the script to complete the message sequence

At the end, the script will generate:

- `q2_output_responses.csv`
- `screenshots/`

---

## Final Summary

In summary, this Q2 submission demonstrates a practical automation proof of concept for interacting with an AI companion platform.

I selected **Kindroid** and implemented a **Playwright-based web automation workflow** that:

- reads a list of input prompts
- sends them to the platform
- captures the resulting bot responses
- stores them in a structured CSV
- records screenshots for traceability

I believe this approach is effective because it is practical, easy to audit, and suitable for real-world research engineering. I also believe it is scalable because the same architecture can be generalized to multiple platforms by replacing platform-specific selectors and session logic.

This proof of concept demonstrates a realistic path toward large-scale automated interaction with AI companion platforms for downstream evaluation and analysis.