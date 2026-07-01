##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os.path as op

import auxly
import auxly.filesys as fsys
from auxly import shell
from ubuild import main, menu
from qprompt import Menu

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

@menu
def cleanup():
    with fsys.Cwd(".", __file__):
        for path in ["dist", "build", "src/qprompt.egg-info", "src/__pycache__"]:
            fsys.delete(path)
    with fsys.Cwd("doc"):
        shell.call("make clean")

@menu("v")
def check_version():
    with fsys.Cwd(".", __file__):
        shell.call("_Check_Versions.py")

@menu("t")
def run_tests():
    with fsys.Cwd("tests", __file__):
        shell.call("_Run_Tests.py")

@menu
def package_menu():
    Menu(install_package_locally, build_package).main(header="Package", submenu=True)

@menu
def docs_menu():
    Menu(readme_excerpt, all_docs, open_docs).main(header="Docs", submenu=True)

@menu
def browse_menu():
    def github(): auxly.open("https://github.com/jeffrimko/qprompt")
    def pypi(): auxly.open("https://pypi.org/project/qprompt/")
    def docs(): auxly.open("https://qprompt.readthedocs.io/")
    def actions(): auxly.open("https://github.com/jeffrimko/Qprompt/actions")
    Menu(github, pypi, docs, actions).main(header="Browse", submenu=True)

def install_package_locally():
    with fsys.Cwd(".", __file__):
        shell.call("pip install -e .")

def build_package():
    # NOTE: Publishing to PyPI is handled by GitHub Actions trusted
    # publishing; publish a GitHub release to trigger it. This builds
    # the sdist/wheel locally for inspection only.
    with fsys.Cwd(".", __file__):
        shell.call("python -m build")

def readme_excerpt():
    """Generates doc/source/readme_excerpt.rst from the README sections up to
    (but not including) the Documentation section."""
    readme = fsys.File("README.md").read()
    start = readme.index("## Introduction")
    end = readme.index("## Documentation")
    excerpt = readme[start:end]
    tempmd = fsys.File("temp_readme_excerpt.md", del_at_exit=True)
    tempmd.write(excerpt)
    rst = shell.strout(f"pandoc -r markdown -w rst --shift-heading-level-by=1 {tempmd}")
    fsys.File(r"doc\source\readme_excerpt.rst").write(rst + "\n")
    print("Readme excerpt generated.")

def all_docs():
    readme_excerpt()
    with fsys.Cwd("doc", __file__):
        shell.call("make html")

def open_docs():
    index = r"doc\build\html\index.html"
    if not op.isfile(index):
        all_docs()
    auxly.open(index)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    main(default="t")
