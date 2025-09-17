"""
Fast Track Academy Setup

Setup script for the Fast Track Academy platform.
"""

from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fast-track-academy",
    version="1.0.0",
    author="Fast Track Academy Team",
    author_email="contact@fast-track-academy.com",
    description="A sophisticated platform showcasing achievements, creating DutyBots, and enabling classroom dashboards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Daisy321woah/Fast-Track-Academy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "web": [
            "flask>=2.3.0",
            "fastapi>=0.100.0",
        ],
        "social": [
            "tweepy>=4.14.0",
            "facebook-sdk>=3.1.0",
            "requests>=2.31.0",
        ],
        "nlp": [
            "nltk>=3.8.0",
            "spacy>=3.6.0",
        ],
        "analytics": [
            "matplotlib>=3.7.0",
            "plotly>=5.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fast-track-bot=bot.bot_core:main",
            "fast-track-interpreter=scanned_books.interpreter:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/Daisy321woah/Fast-Track-Academy/issues",
        "Source": "https://github.com/Daisy321woah/Fast-Track-Academy",
        "Documentation": "https://github.com/Daisy321woah/Fast-Track-Academy/blob/main/README.md",
    },
)