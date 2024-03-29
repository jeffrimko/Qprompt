from os.path import isfile
from setuptools import setup, find_packages

readme = open("README.rst").read() if isfile("README.rst") else ""
print(readme)

setup(
    name = "qprompt",
    version = "0.16.4-alpha.1",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for quick CLI user prompts, input, and menus.",
    license = "MIT",
    keywords = "cli menu prompt input user library",
    url = "https://github.com/jeffrimko/Qprompt",
    py_modules=["qprompt"],
    install_requires=["iterfzf"],
    long_description=readme,
    data_files = [("", ["LICENSE"])],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
