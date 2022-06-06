# -*- coding: utf-8 -*-

import re
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def find_version(*file_path_parts):
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, *file_path_parts), "r") as fp:
        version_file_text = fp.read()

    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file_text,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


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
