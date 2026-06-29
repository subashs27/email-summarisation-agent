import json
import os
from datetime import date

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are an Email Summarization Agent.

Your job:
1. Summarize the email in 2-3 sentences.
2. Extract key points.
3. Extract action items (who should do what).
4. Identify deadlines.
5. Classify urgency as Low, Medium, or High.

Return ONLY valid JSON in this format:

{
    "summary": "",
    "key_points": [],
    "action_items": [],
    "deadlines": [],
    "urgency": ""
}
"""


def read_email(path="email.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def summarize_email(email_text):
    prompt = f"""
{SYSTEM_PROMPT}

Email:

{email_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def save_outputs(data):
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Email Summary ({date.today()})\n")
        f.write("=" * 40 + "\n\n")

        f.write("SUMMARY\n")
        f.write(data["summary"] + "\n\n")

        f.write("KEY POINTS\n")
        for p in data["key_points"]:
            f.write(f"- {p}\n")

        f.write("\nACTION ITEMS\n")
        for a in data["action_items"]:
            f.write(f"- {a}\n")

        f.write("\nDEADLINES\n")
        for d in data["deadlines"]:
            f.write(f"- {d}\n")

        f.write(f"\nURGENCY: {data['urgency']}\n")


def main():
    email_text = read_email()

    print("EMAIL TEXT:")
    print(repr(email_text))

    result = summarize_email(email_text)

    save_outputs(result)

    print("Summary saved to summary.json and summary.txt")
    print(result)
    print("GEMINI RESPONSE:")


if __name__ == "__main__":
    main()