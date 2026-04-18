import csv
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
MESSAGES_FILE = BASE_DIR / "q2_messages.txt"
OUTPUT_FILE = BASE_DIR / "q2_output_responses.csv"
SCREENSHOT_DIR = BASE_DIR / "screenshots"

HOME_URL = "https://kindroid.ai/"
FALLBACK_URL = "https://kindroid.ai/home/"

MESSAGE_BOX_SELECTORS = [
    "textarea",
    'textarea[placeholder*="message" i]',
    'textarea[placeholder*="chat" i]',
    'div[contenteditable="true"]',
]

UI_NOISE = {
    "Ember Preview",
    "Loading...",
    "Kindroid",
}


def load_messages(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Messages file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_results(rows):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["message_index", "input_message", "bot_response", "timestamp_utc"],
        )
        writer.writeheader()
        writer.writerows(rows)


def first_working_locator(page, selectors, timeout_ms=2500):
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            locator.wait_for(timeout=timeout_ms)
            return locator, selector
        except Exception:
            continue
    return None, None


def clean_text(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_visible_elements(page):
    js = '''
    () => {
        function isVisible(el) {
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            return (
                style &&
                style.visibility !== 'hidden' &&
                style.display !== 'none' &&
                rect.width > 8 &&
                rect.height > 8 &&
                rect.bottom > 0 &&
                rect.right > 0 &&
                rect.top < window.innerHeight &&
                rect.left < window.innerWidth
            );
        }

        const nodes = Array.from(document.querySelectorAll('div, p, span, article, section, textarea'));
        const results = [];

        for (const el of nodes) {
            if (!isVisible(el)) continue;

            const text = (el.innerText || el.value || '').trim();
            if (!text) continue;

            const rect = el.getBoundingClientRect();
            results.push({
                text,
                x: rect.x,
                y: rect.y,
                width: rect.width,
                height: rect.height,
                area: rect.width * rect.height
            });
        }

        return results;
    }
    '''
    try:
        return page.evaluate(js)
    except Exception:
        return []


def extract_user_name(elements):
    for el in elements:
        text = clean_text(el["text"])
        m = re.search(r"Chatting as\s+([A-Za-z0-9_]+)", text)
        if m:
            return m.group(1).strip()
    return None


def get_main_transcript_text(page):
    elements = get_visible_elements(page)
    candidates = []

    for el in elements:
        text = clean_text(el["text"])
        if len(text) < 80:
            continue
        if el["x"] > 300:
            continue
        if el["y"] < 100:
            continue
        if el["width"] < 500 or el["width"] > 1500:
            continue
        if el["height"] < 120 or el["height"] > 900:
            continue
        candidates.append(el)

    if not candidates:
        return ""

    candidates.sort(key=lambda e: (e["area"], len(e["text"])), reverse=True)
    return clean_text(candidates[0]["text"])


def chunk_is_label(chunk: str) -> bool:
    chunk = chunk.strip()
    if not chunk:
        return False
    if chunk in UI_NOISE:
        return False
    if len(chunk) > 40:
        return False
    if "\n" in chunk:
        return False
    if re.search(r'[.!?,:;\"“”]', chunk):
        return False
    words = chunk.split()
    if len(words) > 4:
        return False
    return True


def parse_transcript_into_turns(transcript_text: str):
    chunks = [c.strip() for c in re.split(r"\n{2,}", clean_text(transcript_text)) if c.strip()]
    cleaned = []

    for c in chunks:
        if c in UI_NOISE:
            continue
        if c.startswith("Chatting as "):
            continue
        cleaned.append(c)

    turns = []
    i = 0
    while i < len(cleaned):
        if chunk_is_label(cleaned[i]):
            speaker = cleaned[i]
            j = i + 1
            parts = []
            while j < len(cleaned) and not chunk_is_label(cleaned[j]):
                if cleaned[j] not in UI_NOISE and not cleaned[j].startswith("Chatting as "):
                    parts.append(cleaned[j])
                j += 1
            if parts:
                turns.append((speaker, "\n\n".join(parts).strip()))
            i = j
        else:
            i += 1

    return turns


def latest_assistant_reply(page):
    elements = get_visible_elements(page)
    user_name = extract_user_name(elements)
    transcript = get_main_transcript_text(page)

    if not transcript:
        return ""

    turns = parse_transcript_into_turns(transcript)
    if not turns:
        return ""

    for speaker, content in reversed(turns):
        if user_name and speaker == user_name:
            continue
        if content and content not in UI_NOISE and "Loading..." not in content:
            return clean_text(content)

    return ""


def transcript_contains_user_message(page, msg):
    transcript = get_main_transcript_text(page)
    if not transcript:
        return False
    return clean_text(msg) in transcript


def wait_until_message_appears(page, msg, timeout_seconds=15):
    start = time.time()
    while time.time() - start < timeout_seconds:
        if transcript_contains_user_message(page, msg):
            return True
        page.wait_for_timeout(700)
    return False


def wait_for_new_assistant_reply(page, previous_reply, timeout_seconds=120, stable_seconds=5):
    start = time.time()
    best = ""
    last_seen = ""
    last_change_time = None

    while time.time() - start < timeout_seconds:
        current = latest_assistant_reply(page)

        if current and current != previous_reply:
            if current != last_seen:
                last_seen = current
                best = current
                last_change_time = time.time()
            else:
                if last_change_time and (time.time() - last_change_time) >= stable_seconds:
                    return current

        page.wait_for_timeout(1000)

    return best


def wait_until_reply_stable_for_screenshot(page, stable_seconds=4, max_wait_seconds=25):
    start = time.time()
    last_text = latest_assistant_reply(page)
    unchanged_since = time.time()

    while time.time() - start < max_wait_seconds:
        current = latest_assistant_reply(page)

        if current != last_text:
            last_text = current
            unchanged_since = time.time()
        else:
            if time.time() - unchanged_since >= stable_seconds:
                return

        page.wait_for_timeout(1000)


def send_message(page, msg):
    box, _ = first_working_locator(page, MESSAGE_BOX_SELECTORS, timeout_ms=4000)
    if box is None:
        raise RuntimeError("Could not find message input box")

    try:
        box.click()
    except Exception:
        pass

    entered = False

    try:
        box.fill("")
    except Exception:
        pass

    try:
        box.fill(msg)
        entered = True
    except Exception:
        pass

    if not entered:
        try:
            box.click()
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            page.keyboard.type(msg)
            entered = True
        except Exception:
            pass

    if not entered:
        raise RuntimeError(f"Could not type message: {msg}")

    before_transcript = get_main_transcript_text(page)

    try:
        box.press("Enter")
    except Exception:
        page.keyboard.press("Enter")

    if wait_until_message_appears(page, msg, timeout_seconds=15):
        return

    try:
        box, _ = first_working_locator(page, MESSAGE_BOX_SELECTORS, timeout_ms=2000)
        if box:
            box.click()
            page.keyboard.press("Enter")
    except Exception:
        pass

    if wait_until_message_appears(page, msg, timeout_seconds=10):
        return

    after_transcript = get_main_transcript_text(page)
    if after_transcript != before_transcript:
        return

    raise RuntimeError(f"Message was not detected in transcript: {msg}")


def ensure_output_dir():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    ensure_output_dir()
    messages = load_messages(MESSAGES_FILE)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        print("Opening Kindroid...")
        try:
            page.goto(HOME_URL, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            page.goto(FALLBACK_URL, wait_until="domcontentloaded", timeout=60000)

        if len(messages) < 10:
            print("Warning: The task suggests at least 10 messages.")

        print("\nManual step required:")
        print("1. Log in to Kindroid if needed.")
        print("2. Open or create a Kindroid chat / preview.")
        print("3. Make sure the message box is visible.")
        input("\nWhen the chat page is ready, press Enter here to continue... ")

        box, selector_used = first_working_locator(page, MESSAGE_BOX_SELECTORS, timeout_ms=4000)
        if box is None:
            raise RuntimeError("Could not find message input box")
        print(f"Using message box selector: {selector_used}")

        for i, msg in enumerate(messages, start=1):
            print(f"\nSending message {i}/{len(messages)}: {msg}")

            previous_reply = latest_assistant_reply(page)

            send_message(page, msg)
            reply = wait_for_new_assistant_reply(
                page,
                previous_reply,
                timeout_seconds=120,
                stable_seconds=5,
            )

            wait_until_reply_stable_for_screenshot(
                page,
                stable_seconds=4,
                max_wait_seconds=25,
            )

            timestamp_utc = datetime.now(timezone.utc).isoformat()
            results.append({
                "message_index": i,
                "input_message": msg,
                "bot_response": reply,
                "timestamp_utc": timestamp_utc,
            })

            save_results(results)

            screenshot_path = SCREENSHOT_DIR / f"step_{i:02d}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
            except Exception:
                pass

            print("Bot response:")
            print(reply)
            print("-" * 80)

        print(f"Saved CSV output to: {OUTPUT_FILE}")
        print(f"Saved screenshots to: {SCREENSHOT_DIR}")
        print("Run complete. Browser will stay open.")
        input("Press Enter whenever you want to end the Python script... ")


if __name__ == "__main__":
    main()
