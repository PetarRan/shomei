#!/usr/bin/env python3
"""
Setup script for shōmei.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read version from __init__.py
def get_version():
    init_file = Path(__file__).parent / "shomei" / "__init__.py"
    with open(init_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    return "0.1.0"

setup(
    name="shomei",
    version=get_version(),
    description="Show off your coding contributions without leaking corporate IP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="shomei contributors",
    author_email="",
    url="https://github.com/petarran/shomei",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0.0",
        "gitpython>=3.1.0",
        "colorama>=0.4.6",
        "pyyaml>=6.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "shomei=shomei.cli:cli",
        ],
    },
    keywords="git, github, contributions, privacy, corporate, sanitize",
    project_urls={
        "Bug Reports": "https://github.com/petarran/shomei/issues",
        "Source": "https://github.com/petarran/shomei",
        "Documentation": "https://github.com/petarran/shomei/issues",
    },
)
