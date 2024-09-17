from setuptools import setup, find_packages

setup(
    name="pySidraData",
    version="0.1.0",
    description="A Python client for interacting with IBGE API for aggregate data.",
    author="Fernando Barbosa",
    author_email="fernando.liaison@gmail.com",
    license="MIT",
    packages=find_packages(where="pySidraData"),
    package_dir={"": "pySidraData"},
    install_requires=[
        "requests>=2.0",
        "pandas>=1.0"
    ],
    extras_require={
        "dev": ["pre-commit", "flake8", "black", "isort"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/nandevers/pySidraData",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
