from setuptools import setup, find_packages

setup(
    name = "qprompt",
    version = "0.1.2",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for quick CLI prompts.",
    license = "MIT",
    keywords = "cli",
    url = "https://github.com/jeffrimko/Qprompt",
    py_modules=["qprompt"],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
)
