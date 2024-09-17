from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
def parse_requirements(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()

setup(
    name="pySidraData",
    version="0.1.0",
    description="A Python client for interacting with IBGE API for aggregate data.",
    author="Fernando Barbosa",
    author_email="fernando.liaison@gmail.com",
    license="MIT",
    packages=find_packages(where="pySidraData"),
    package_dir={"": "pySidraData"},
    install_requires=parse_requirements("requirements.txt"),
    extras_require={
        "dev": [
            "pre-commit",
            "flake8",
            "black",
            "isort"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Homepage": "https://github.com/nandevers/pySidraData",
        "Repository": "https://github.com/nandevers/pySidraData",
    },
)
