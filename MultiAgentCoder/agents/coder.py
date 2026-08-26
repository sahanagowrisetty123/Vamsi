import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)


class CoderAgent:

    def generate_code(self, folder, plan):

        project = plan.get("project", "Website")
        framework = plan.get("framework", "Bootstrap 5")
        theme = plan.get("theme", "Modern")
        features = ", ".join(plan.get("features", []))

        prompt = f"""
Create a COMPLETE production-ready website.

Project Name:
{project}

Framework:
{framework}

Theme:
{theme}

Features:
{features}

The website MUST include:

✔ Bootstrap 5.3 CDN
✔ Bootstrap Icons
✔ Google Font Poppins
✔ Responsive Navbar
✔ Responsive Hero Section
✔ Responsive Content
✔ Responsive Cards
✔ Responsive Footer
✔ Mobile First
✔ Tablet Support
✔ Laptop Support
✔ Desktop Support
✔ Beautiful Color Palette
✔ Professional Spacing
✔ Shadows
✔ Rounded Corners
✔ Animations
✔ Hover Effects
✔ CSS Variables
✔ Media Queries
✔ No Overflow
✔ No Horizontal Scroll

Special Rules

If Calculator:

• Professional Calculator
• Glassmorphism
• Dark Theme
• Keyboard Support
• AC
• DEL
• Decimal
• Responsive Buttons
• Responsive Display
• Bootstrap Card
• Button Hover Animation

If Todo:

• Add Task
• Delete Task
• Mark Complete
• Local Storage
• Responsive Cards
• Empty State

If Portfolio:

• Hero
• About
• Skills
• Services
• Projects
• Contact
• Footer
• Scroll Animation

Return EXACTLY:

### index.html

<complete html>

### style.css

<complete css>

### script.js

<complete javascript>

Return only code.
"""

        try:

            response = client.chat.completions.create(
               model="llama-3.1-8b-instant",
                messages=[
                   {
    "role": "system",
    "content": """
You are an Award-Winning Senior Frontend Architect, UI/UX Designer and Full Stack Engineer.

Your job is to generate PRODUCTION READY websites.

STRICT RULES:

• Always use Bootstrap 5.3 CDN
• Always use Bootstrap Icons
• Always use Google Fonts (Poppins)
• Mobile First Design
• Fully Responsive
• Responsive Navbar
• Responsive Footer
• Hero Section
• Cards
• Sections with proper spacing
• Beautiful animations
• Hover effects
• Glassmorphism where suitable
• Professional gradients
• Modern UI
• Responsive Typography
• Responsive Images
• Flexbox
• Bootstrap Grid
• Media Queries
• No horizontal scrolling
• Clean Semantic HTML5
• SEO friendly
• Accessibility
• Cross-browser compatible

Return ONLY these files:

### index.html

### style.css

### script.js

Never explain.
Never use markdown.
Never omit code.
Generate complete files.
"""
},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,
                max_tokens=8192
            )

            text = response.choices[0].message.content

            text = (
                text.replace("```html", "")
                .replace("```css", "")
                .replace("```javascript", "")
                .replace("```js", "")
                .replace("```", "")
            )

            html = ""
            css = ""
            js = ""

            html_match = re.search(
                r"### index\.html(.*?)### style\.css",
                text,
                re.DOTALL | re.IGNORECASE,
            )

            css_match = re.search(
                r"### style\.css(.*?)### script\.js",
                text,
                re.DOTALL | re.IGNORECASE,
            )

            js_match = re.search(
                r"### script\.js(.*)",
                text,
                re.DOTALL | re.IGNORECASE,
            )

            if html_match:
                html = html_match.group(1).strip()

            if css_match:
                css = css_match.group(1).strip()

            if js_match:
                js = js_match.group(1).strip()

            if not html:
                raise Exception("HTML generation failed.")

            with open(
                os.path.join(folder, "index.html"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(html)

            with open(
                os.path.join(folder, "style.css"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(css)

            with open(
                os.path.join(folder, "script.js"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(js)

            print("Project generated successfully.")

            return True

        except Exception as e:
            print("Generation Error:", e)
            raise