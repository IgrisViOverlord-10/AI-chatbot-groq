import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def explain(intent, data, history=None, parameters=None):
    """
    Converts structured analytics into a concise,
    human-friendly business explanation.
    """

    if history is None:
        history = []

    if parameters is None:
        parameters = {}

    recent_history = history[-3:]

    prompt = f"""
You are an AI Business Intelligence Assistant.

Your job is to explain business analytics in simple,
professional English.

IMPORTANT:

The analytics have ALREADY been calculated.

Never:

- perform calculations
- change numbers
- estimate values
- invent percentages
- invent trends
- invent business reasons
- assume inventory
- mention Python
- mention Pandas
- mention JSON
- mention calculations
- mention "provided data"

------------------------------------------------

Conversation History

{json.dumps(recent_history, indent=2)}

------------------------------------------------

Intent

{intent}

------------------------------------------------

Parameters

{json.dumps(parameters, indent=2)}

------------------------------------------------

Analysis Result

{json.dumps(data, indent=2)}

------------------------------------------------

Response Rules

Keep the response SHORT.

Maximum 150 words.

Respond naturally like ChatGPT.

Do NOT sound like a report.

Do NOT use long paragraphs.

Use exactly this format:

### Answer

(Answer the user's question directly in 2-4 sentences.)

**Business Insight**

(One useful insight.)

**Recommendation**

(One practical recommendation.)

If appropriate, finish with:

You can also ask:

• Question 1

• Question 2

• Question 3

Only include follow-up questions if they make sense.

Never use markdown tables.

Never repeat the user's question.

Never use headings like:

- Executive Summary
- Key Insights
- Dashboard Report
- Analysis Result

Just answer naturally.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI Business Intelligence Assistant.

Your personality:

- Friendly
- Professional
- Concise
- Helpful

Always answer naturally like ChatGPT.

Never invent facts.

Only explain the supplied analytics.

Avoid unnecessary business jargon.

Keep answers concise.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content