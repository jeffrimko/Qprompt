##==============================================================#
## SECTION: Imports                                             #
##==============================================================#

import auxly
import auxly.filesys as fsys
import os.path as op
from auxly import shell
from ubuild import main, menu
from xml.etree import ElementTree

##==============================================================#
## SECTION: Function Definitions                                #
##==============================================================#

@menu("t", "Run Tests")
def test():
    with fsys.Cwd("tests", __file__):
        shell.call("_Run_Tests.py")

@menu("v", "Check Version")
def version():
    with fsys.Cwd(".", __file__):
        shell.call("_Check_Versions.py")

@menu("i", "Install Package Locally")
def install():
    with fsys.Cwd("lib", __file__):
        shell.call("_Install_Package.py")

@menu("u", "Upload To PyPI")
def upload():
    with fsys.Cwd("lib", __file__):
        shell.call("_Upload_PyPI.py")

@menu("r", "Build Readme Excerpt")
def readme():
    tempxml = "temp.xml"
    shell.call(f"asciidoctor -b docbook -o {tempxml} README.adoc")
    e = ElementTree.parse(tempxml).getroot()
    fsys.delete(tempxml)
    ns = {'db': 'http://docbook.org/ns/docbook', 'xml': 'http://www.w3.org/XML/1998/namespace'}
    rst = ""
    for sect in ["_introduction", "_status", "_requirements", "_installation"]:
        xml = ElementTree.tostring(e.find(f".//db:section[@xml:id='{sect}']", ns)).decode("utf-8")
        fsys.File(tempxml).write(xml)
        rst += shell.strout(f"pandoc -r docbook -w rst --base-header-level=2 {tempxml}")
        rst += "\n\n"
    fsys.File(r"doc\source\readme_excerpt.rst").write(rst)
    fsys.delete(tempxml)
    print("Readme excerpt generated.")

@menu("d", "Build Docs")
def docs():
    readme()
    with fsys.Cwd("doc", __file__):
        shell.call("make html")

@menu("o", "Open Docs")
def open_doc():
    INDEX = r"doc\build\html\index.html"
    if not op.isfile(INDEX):
        docs()
    auxly.open(INDEX)

##==============================================================#
## SECTION: Main Body                                           #
##==============================================================#

if __name__ == '__main__':
    main()
