# -*- coding: utf-8 -*-

from os import path

from setuptools import find_packages, setup

# Read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="crypto-rdb",
    version="latest",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    author="Sungho Joo, Dongmin Lee",
    author_email="triangle124@gmail.com, kid33629@gmail.com",
    description="A repository for implementations related to Crypto-RDB project",
    keywords="crypto-rdb",
    url="https://github.com/sungho-joo/crypto-rdb",
    project_urls={
        "Documentation": "https://github.com/sungho-joo/crypto-rdb",
        "Source Code": "https://github.com/sungho-joo/crypto-rdb",
    },
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
