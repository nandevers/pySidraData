# pySidraData

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Build Status](https://github.com/nandevers/pySidraData/workflows/Build/badge.svg)](https://github.com/nandevers/pySidraData/actions)
[![Coverage Status](https://coveralls.io/repos/github/nandevers/pySidraData/badge.svg?branch=main)](https://coveralls.io/github/nandevers/pySidraData?branch=main)

`pySidraData` is a Python client for interacting with the IBGE (Instituto Brasileiro de Geografia e Estatística) API for aggregate data. It provides an easy-to-use interface to fetch, manipulate, and analyze data from the IBGE database.

## Features

- Fetch and explore root data from the IBGE API.
- Retrieve metadata for specific aggregate IDs.
- Convert data to a Pandas DataFrame for analysis.
- Easy-to-use and extendable structure.
- Supports Python 3.6 and above.

## Installation

You can install `pySidraData` using pip:

```bash
pip install pySidraData
```

Alternatively, you can install it from the source:

```bash
git clone https://github.com/nandevers/pySidraData.git
cd pySidraData
pip install .
```

## Usage

Here's a quick example of how to use `pySidraData`:

```python
from pySidraData import Client

# Initialize the client
client = Client()

# Get root data
root_data = client.get_root_data()
for research in root_data.research_list:
    print(f"Research ID: {research.id}, Name: {research.nome}")
    for aggregate in research.agregados:
        print(f"  Aggregate ID: {aggregate.id}, Name: {aggregate.nome}")

# Get metadata for a specific aggregate ID
metadata = client.get_metadata('8418')
print(metadata)

# Convert root data to a Pandas DataFrame
df = client.get_root_data_as_dataframe()
print(df.head())
```

## Documentation

The full documentation for `pySidraData` can be found [here](https://github.com/nandevers/pySidraData/wiki).

## Contributing

We welcome contributions to `pySidraData`! If you have an idea for a feature or have found a bug, please check our [contributing guidelines](https://github.com/nandevers/pySidraData/blob/main/CONTRIBUTING.md) before you start. Here are some ways you can contribute:

- **Reporting Bugs**: Use the [issue tracker](https://github.com/nandevers/pySidraData/issues) to report any bugs you find.
- **Feature Requests**: If you have an idea for a new feature, please submit it as an issue with the label `enhancement`.
- **Pull Requests**: If you want to contribute code, fork the repository and create a pull request with your changes.
- **Documentation**: Help improve our documentation or add new examples.

We use `pre-commit` hooks to ensure code quality. Please install the hooks before making commits:

```bash
pip install pre-commit
pre-commit install
```

### Setting Up the Development Environment

To set up the development environment, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/nandevers/pySidraData.git
    cd pySidraData
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the package in editable mode with development dependencies:

    ```bash
    pip install -e .[dev]
    ```

4. Run the tests to make sure everything is set up correctly:

    ```bash
    python -m unittest discover tests
    ```

### Running Tests

We use `unittest` for testing. To run the tests, use the following command:

```bash
python -m unittest discover tests
```

Make sure all tests pass before submitting a pull request.

### Code Style

We follow PEP 8 for code style. Please ensure your code is formatted correctly before submitting a pull request. You can use `flake8` to check for any style issues:

```bash
flake8 pySidraData/
```

## License

`pySidraData` is licensed under the MIT License. See the [LICENSE](https://github.com/nandevers/pySidraData/blob/main/LICENSE) file for more information.

## Acknowledgements

This project was inspired by the need to easily interact with the IBGE API for data analysis and research purposes. Special thanks to the IBGE for providing an accessible API.

## Contact

If you have any questions or suggestions, feel free to open an issue or reach out to the maintainer at fernando.liaison@gmail.com.

Happy coding! We hope `pySidraData` makes your data analysis work easier and more enjoyable.
