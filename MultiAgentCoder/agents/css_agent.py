import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class CSSAgent:

    def generate(self, folder, plan):

        html_path = os.path.join(folder, "index.html")

        with open(html_path, "r", encoding="utf8") as f:
            html = f.read()

        project = plan["project"]
        theme = plan["theme"]

        prompt = f"""
You are a Senior CSS Engineer.

Generate ONLY style.css.

Project:
{project}

Theme:
{theme}

Below is the HTML.

========================

{html}

========================

Rules:

1. DO NOT modify HTML.
2. Use Bootstrap classes already present.
3. Write ONLY custom CSS.
4. Make the website fully responsive.
5. Mobile First Design.
6. Add Media Queries.

Breakpoints:

320px
576px
768px
992px
1200px
1400px

Use:

✔ CSS Variables

✔ Modern Color Palette

✔ Professional Typography

✔ Poppins Font

✔ Animations

✔ Hover Effects

✔ Glassmorphism where suitable

✔ Cards

✔ Buttons

✔ Shadows

✔ Border Radius

✔ Flexbox

✔ CSS Grid

✔ Smooth Scrolling

✔ Responsive Images

✔ Responsive Sections

✔ No Overflow

✔ No Horizontal Scroll

✔ Dark Theme if appropriate

Calculator:

• Responsive Calculator

• Beautiful Buttons

• Nice Display

Portfolio:

• Modern Hero

• Skills Cards

• Project Cards

• Contact Form

Todo:

• Beautiful Task Cards

• Mobile Friendly

Return ONLY CSS.

No markdown.

No explanation.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a Senior CSS Architect.

Generate only CSS.

Never generate HTML.

Never generate JavaScript.

Generate production-quality responsive CSS.

Use media queries.

Bootstrap compatible.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=4096
        )

        css = response.choices[0].message.content

        css = (
            css.replace("```css", "")
               .replace("```", "")
               .strip()
        )

        css_path = os.path.join(folder, "style.css")

        with open(css_path, "w", encoding="utf8") as f:
            f.write(css)

        return css_path