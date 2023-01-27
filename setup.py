import pathlib
from os import path
from setuptools import setup

HERE = pathlib.Path(__file__).parent
def readme():
    with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
        return f.read()

setup(
    name="tea-web",
    version="0.0.4",
    description="Simple HTTP library for web applications written in Python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="orhanemree (Orhan Emre Dikicigil)",
    author_email="orhanemre.dev@gmail.com",
    license="MIT",
    packages=["tea"],
    package_dir={"":"src"}
) 