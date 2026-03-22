"""Setup configuration for mazegen package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mazegen",
    version="1.0.0",
    author="42 Student",
    description="A maze generator with solver and ASCII visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/42/a_maze_ing",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mazegen=a_maze_ing:main",
        ],
    },
)
