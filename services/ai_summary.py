from groq import Groq
from flask import current_app
import json


def generate_ai_summary(total, high_pct, medium_pct, low_pct):

    client = Groq(
        api_key=current_app.config["GROQ_API_KEY"]
    )

    prompt = f"""
You are a Chief Data & Strategy Officer preparing a formal board-level churn intelligence briefing.

This is a strategic executive document — NOT a short summary.

Customer Risk Statistics:
- Total Customers: {total}
- High Risk: {high_pct}%
- Medium Risk: {medium_pct}%
- Low Risk: {low_pct}%

Your response MUST:

• Be between 450–700 words total
• Provide deep business interpretation
• Discuss revenue risk implications
• Explain customer lifecycle impact
• Analyze operational and marketing implications
• Include strategic foresight
• Avoid generic language
• Avoid short summaries
• Avoid bullet brevity

Return ONLY valid JSON in EXACT format:

{{
  "summary": "Minimum 300–400 word executive analysis paragraph block.",
  "insights": [
    "Detailed strategic insight 1 (2-3 sentences)",
    "Detailed strategic insight 2 (2-3 sentences)",
    "Detailed strategic insight 3 (2-3 sentences)",
    "Detailed strategic insight 4 (2-3 sentences)"
  ],
  "actions": [
    "Strategic retention initiative 1 (detailed explanation)",
    "Strategic retention initiative 2 (detailed explanation)",
    "Strategic retention initiative 3 (detailed explanation)",
    "Strategic retention initiative 4 (detailed explanation)",
    "Strategic retention initiative 5 (detailed explanation)"
  ]
}}

Do NOT include markdown.
Do NOT include commentary.
Return only JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1800
    )

    raw_text = response.choices[0].message.content

    try:
        ai_data = json.loads(raw_text)
    except:
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        ai_data = json.loads(raw_text[start:end])

    return ai_data
