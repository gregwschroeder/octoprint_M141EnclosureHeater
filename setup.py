# coding=utf-8
from setuptools import setup, find_packages
from os import path

# Read the README for the long description.
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="OctoPrint-M141EnclosureHeater",
    version="0.1.0",
    description="Plugin for OctoPrint that listens for M141 commands to extract a temperature and send a REST API call to arm an enclosure heater.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your_github_username/OctoPrint-M141EnclosureHeater",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "OctoPrint>=1.4.0",
        "requests"
    ],
    license="AGPLv3",
    classifiers=[
        "Framework :: OctoPrint",
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        "octoprint.plugin": [
            "M141EnclosureHeater = octoprint_M141EnclosureHeater"
        ]
    }
)
