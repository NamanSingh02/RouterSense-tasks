# Q2 Run Steps

## 1. Put these files in one folder
Make sure these files are together:

- `q2_playwright_kindroid_poc.py`
- `q2_messages.txt`

## 2. Create a virtual environment

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install playwright pandas
python -m playwright install
```

## 4. Run the script
```bash
python q2_playwright_kindroid_poc.py
```

## 5. What happens next
The script will:

1. open Kindroid in a visible browser
2. wait for you to log in manually
3. ask you to press Enter in the terminal once the chat page is ready
4. send messages from `q2_messages.txt`
5. capture responses
6. save results into `q2_output_responses.csv`
7. save screenshots into `screenshots/`

## 6. First-time setup tip
If you are not already inside a chat after login:

- open or create a Kindroid manually
- make sure the message input box is visible
- only then go back to the terminal and press Enter

## 7. Output files
After the run, check:

- `q2_output_responses.csv`
- `screenshots/`

## 8. If the site layout changes
The most likely thing to break is the page selector.

Open `q2_playwright_kindroid_poc.py` and update the selector lists:
- `MESSAGE_BOX_SELECTORS`
- `SEND_BUTTON_SELECTORS`
- `ASSISTANT_MESSAGE_SELECTORS`

That is usually enough to restore the script.
