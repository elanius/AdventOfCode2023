from setuptools import setup

setup(
    name="advent_of_code_2023",
    version="0.1.0",
    packages=["trebuchet"],
    package_dir={
        "": ".",
        "trebuchet": "advent_of_code/day_01",
    },
    install_requires=[
        "pytest>=6.0",  # Specify the version of pytest you need
    ],
    author="Stanislav Alexovic",
    author_email="stanislav.alexovic@gmail.com",
    description="A package for Advent of Code 2023 challenges.",
    url="https://github.com/elanius/AdventOfCode2023",
)
