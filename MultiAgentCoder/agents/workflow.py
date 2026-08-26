from agents.planner import PlannerAgent
from agents.architect import ArchitectAgent
from agents.html_agent import HTMLAgent
from agents.css_agent import CSSAgent


class Workflow:

    def __init__(self):

        self.planner = PlannerAgent()
        self.architect = ArchitectAgent()
        self.html = HTMLAgent()
        self.css = CSSAgent()

    def run(self, prompt):

        print("Planning Project...")
        plan = self.planner.plan(prompt)

        print("Creating Project...")
        folder = self.architect.create_project(plan)

        print("Generating HTML...")
        self.html.generate(folder, plan)

        print("Generating CSS...")
        self.css.generate(folder, plan)

        print("Completed HTML + CSS")

        return {
    "folder": folder
}