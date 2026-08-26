import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class PlannerAgent:

    def plan(self, user_prompt):

        system_prompt = """
You are an Expert Software Architect.

Your job is to analyze the user's request.

Return ONLY valid JSON.

Example:

{
    "project":"Portfolio Website",

    "framework":"Bootstrap 5",

    "theme":"Modern Dark",

    "pages":[
        "index.html"
    ],

    "styles":[
        "style.css"
    ],

    "scripts":[
        "script.js"
    ],

    "features":[
        "Responsive",
        "Hero",
        "About",
        "Projects",
        "Skills",
        "Contact",
        "Footer",
        "Animations"
    ]
}

Rules:

Return ONLY JSON.

No explanation.

No markdown.
"""

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.2,

            max_tokens=1024

        )

        content = response.choices[0].message.content.strip()

        content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)