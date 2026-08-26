import os


class ArchitectAgent:

    def create_project(self, plan):

        project = plan["project"]

        folder = os.path.join(
            "generated",
            project.replace(" ", "_")
        )

        os.makedirs(folder, exist_ok=True)

        for page in plan["pages"]:

            open(
                os.path.join(folder, page),
                "w",
                encoding="utf8"
            ).close()

        for css in plan["styles"]:

            open(
                os.path.join(folder, css),
                "w",
                encoding="utf8"
            ).close()

        for js in plan["scripts"]:

            open(
                os.path.join(folder, js),
                "w",
                encoding="utf8"
            ).close()

        return folder