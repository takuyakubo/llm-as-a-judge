"""Setup script for LLM as a Judge."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-as-a-judge",
    version="0.1.0",
    author="Takuya Kubo",
    author_email="takuyakubo@example.com",
    description="A Python framework for evaluating documents using LLMs as judges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takuyakubo/llm-as-a-judge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.990",
        ],
    },
    entry_points={
        "console_scripts": [
            "llm-judge=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json"],
    },
)