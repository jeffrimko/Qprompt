##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import os.path as op
from xml.etree import ElementTree

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
    with fsys.Cwd("lib"):
        shell.call("_Cleanup.bat")
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
    Menu(install_package_locally, upload_to_pypi).main(header="Package", submenu=True)

@menu
def docs_menu():
    Menu(readme_excerpt, all_docs, open_docs).main(header="Docs", submenu=True)

@menu
def browse_menu():
    def github(): auxly.open("https://github.com/jeffrimko/qprompt")
    def pypi(): auxly.open("https://pypi.org/project/qprompt/")
    def docs(): auxly.open("https://qprompt.readthedocs.io/")
    def travis(): auxly.open("https://travis-ci.org/jeffrimko/Qprompt")
    Menu(github, pypi, docs, travis).main(header="Browse", submenu=True)

def install_package_locally():
    with fsys.Cwd("lib", __file__):
        shell.call("_Install_Package.py")

def upload_to_pypi():
    with fsys.Cwd("lib", __file__):
        shell.call("_Upload_PyPI.py")

def readme_excerpt():
    tempxml1 = fsys.File("temp1.xml", del_at_exit=True)
    shell.call(f"asciidoctor -b docbook -o {tempxml1} README.adoc")
    e = ElementTree.parse(str(tempxml1)).getroot()
    ns = {'db': 'http://docbook.org/ns/docbook', 'xml': 'http://www.w3.org/XML/1998/namespace'}
    rst = ""
    tempxml2 = fsys.File("tempxml2.xml", del_at_exit=True)
    for sect in ["_introduction", "_status", "_requirements", "_installation"]:
        elem = e.find(f".//db:section[@xml:id='{sect}']", ns)
        # NOTE: Removing the id attribute prevents "WARNING: malformed
        # hyperlink target" when building Sphinx docs.
        elem.attrib.pop("{http://www.w3.org/XML/1998/namespace}id")
        xml = ElementTree.tostring(elem).decode("utf-8")
        tempxml2.write(xml)
        rst += shell.strout(f"pandoc -r docbook -w rst --base-header-level=2 {tempxml2}")
        rst += "\n\n"
    fsys.File(r"doc\source\readme_excerpt.rst").write(rst)
    print("Readme excerpt generated.")

def all_docs():
    readme_excerpt()
    with fsys.Cwd("doc", __file__):
        shell.call("make html")

def open_docs():
    index = r"doc\build\html\index.html"
    if not op.isfile(index):
        docs()
    auxly.open(index)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    main(default="t")
