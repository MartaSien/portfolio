import os, shutil
from operator import itemgetter
from jinja2 import Environment, FileSystemLoader
import json
from pathlib import Path
import markdown


_PROJECTS_DIR = "projects"


class SiteGenerator(object):
    def __init__(self):
        self.projects = []
        self.env = Environment(loader=FileSystemLoader("template"))
        self.get_projects()
        self.empty_public()
        self.copy_static()
        self.render_project_details_md()
        self.render_mainpage()

    def get_projects(self):
        """Request and parse all json files in projects folder, saving them in self.projects"""
        folder_path = Path(_PROJECTS_DIR)
        for file_path in folder_path.iterdir():
            if file_path.suffix == ".json":
                print(f"Project added: {file_path}")
                data = json.loads(file_path.read_bytes())
                data["Filename"] = file_path.stem
                self.projects.append(data)
        self.projects = sorted(self.projects, key=itemgetter("Priority"))
    
    def empty_public(self):
        """Ensure the public directory is empty before generating"""
        try:
            shutil.rmtree("./public")
            os.mkdir("./public")
        except:
            print("Error cleaning up old files.")
    
    def copy_static(self):
        """Copy static assets to the public directory"""
        try:
            shutil.copytree("template/static", "public/static")
        except:
            print("Error copying static files.")
    
    def render_mainpage(self):
        """Create the main landing webpage."""
        print("Creating page to static file.")
        template = self.env.get_template("_main_layout.html")
        with open("public/index.html", "w+", encoding="utf-8") as file:
            html = template.render(title="MartaSien", projects=self.projects)
            file.write(html)
    
    def render_project_details_md(self):
        """Create details subpage for each project."""
        print("Creating project detail subpages (md).")
        template = self.env.get_template("_project_layout.html")
        folder_path = Path(f"{_PROJECTS_DIR}/md")
        for file_path in folder_path.iterdir():
            description = markdown.markdown(file_path.read_text(encoding="utf-8"))
            webpage_name = "public/" + file_path.stem + ".html"
            print(f"Creating page: {webpage_name}.")
            with open(webpage_name, "w+", encoding="utf-8") as file:
                html = template.render(project_description=description, projects=self.projects)
                file.write(html)


if __name__ == "__main__":
    SiteGenerator()
