import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class HTMLAgent:

    def generate(self, folder, plan):

        project = plan["project"]
        theme = plan["theme"]
        framework = plan["framework"]
        features = ", ".join(plan["features"])

        prompt = f"""
You are an Expert HTML Developer.

Create ONLY index.html.

Project:
{project}

Framework:
{framework}

Theme:
{theme}

Features:
{features}

Requirements:

1. HTML5
2. Bootstrap 5.3 CDN
3. Bootstrap Icons CDN
4. Google Font Poppins
5. Responsive Navbar
6. Hero Section
7. Dynamic Sections according to project
8. Responsive Footer
9. Semantic HTML
10. Accessibility
11. Mobile First
12. Link style.css
13. Link script.js
14. Use Bootstrap Grid
15. No inline CSS
16. No inline JavaScript
17. Every important section MUST have an id.

If Calculator:

- Calculator Card
- Display
- Buttons
- Every button must have id
- Display id="display"

If Todo:

- Input
- Add Button
- Task List
- Empty State

If Portfolio:

- Hero
- About
- Skills
- Projects
- Services
- Contact
- Footer

Return ONLY HTML.

No markdown.
No explanation.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a Senior HTML Engineer.

Generate production-quality HTML.

Bootstrap only.

Responsive only.

Never generate CSS.

Never generate JavaScript.

Return ONLY HTML.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4096
        )

        html = response.choices[0].message.content

        html = (
            html.replace("```html", "")
                .replace("```", "")
                .strip()
        )

        html_path = os.path.join(folder, "index.html")

        with open(html_path, "w", encoding="utf8") as f:
            f.write(html)

        return html_path