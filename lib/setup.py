import os
import subprocess
from setuptools import setup, find_packages

subprocess.call("asciidoc -b docbook ../README.adoc", shell=True)
readme = subprocess.check_output("pandoc -r docbook -w rst ../README.xml", shell=True)
os.remove("../README.xml")

setup(
    name = "qprompt",
    version = "0.1.5",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for quick CLI prompts.",
    license = "MIT",
    keywords = "cli",
    url = "https://github.com/jeffrimko/Qprompt",
    py_modules=["qprompt"],
    long_description=readme,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
)
