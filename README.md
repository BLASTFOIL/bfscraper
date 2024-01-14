# BASTFOIL Scraper

[![Package Build and Test](https://github.com/BLASTFOIL/bfscraper/actions/workflows/build.yml/badge.svg)](https://github.com/BLASTFOIL/bfscraper/actions/workflows/build.yml)
[![GitHub issues](https://img.shields.io/github/issues-raw/BLASTFOIL/bfscraper?logo=github&label=Open%20Issues)](https://github.com/BLASTFOIL/bfscraper/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/BLASTFOIL/bfscraper?logo=github&label=Open%20PRs)](https://github.com/BLASTFOIL/bfscraper/pulls)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FBLASTFOIL%2Fbfscraper%2Fstable%2Fpyproject.toml)

This is a compound scraper module for BLASTFOIL database population. It gathers airfoil data from different sources and stores it in a single database.

> [!NOTE]
> All instructions in this README assume your Python 3.11.6+ installation is in your PATH and is aliased under `python`. If this is not the case, you will need to replace `python` with the alias or path that points to the correct Python executable.

## Installation

```bash
python -m pip install git+https://github.com/BLASTFOIL/bfscraper.git
```

## Usage

Calling the module will automatically scrape all sources and store the data in a single database.

For more information on the command line interface, run:

```bash
python -m bfscraper --help
```

Which will display the following help message:

```txt
Usage: python -m bfscraper [OPTIONS]

  Command line interface.

  Args:     *args: positional arguments.     **kwargs: keyword arguments.

Options:
  -c, --count INTEGER RANGE    Number of airfoils to scrape (-1 for all
                               available).  [default: -1; x>=-1]
  -o, --output FILE            Output file path.  [default: scraped.json]
  -t, --timeout INTEGER RANGE  Request timeout in seconds (-1 for no timeout).
                               [default: -1; x>=-1]
  -l, --limit INTEGER RANGE    Simultaneous requests limit.  [default: 20;
                               x>=1]
  -v, --verbose                Verbose mode.
  --help                       Show this message and exit.
```

The output file will be a JSON file containing the following entry structure:

```json
{
  <unique airfoil ID>: {
      "name": <airfoil name>,
      "family": <airfoil family>,
      "links": {
          "info": <URL of the information page>,
          "files": <URL of the data download links page>
      },
      "download-links": {
          <different format download URLs>
      },
      "dat": <extracted Selig Format airfoil contour>,
      "data-sources": [
          <supported data formats (XFoil, JavaFoil...)>
      ],
      "optimizations": {
          <different optimized parameter values (Cl, Cd...)>
      }
  },
  ...
}
```

## Sources

This is the list of domains that are currently supported for scraping:

- [BigFoil](https://bigfoil.ae.illinois.edu)
- [AirfoilTools](https://airfoiltools.com) (included in the BigFoil source)

## Disclaimer

All information presented herein is delivered without guarantee or warranty of any kind. The user assumes the entire risk of use of this information. In no event shall any person be liable for any direct, indirect, consequential or incidental damages arising from the use of, or reliance on, this information. This information is subject to change without notice.

This tool is not, in any way, related to any of the sources mentioned above. It is an independent project that aims to gather data from different sources and store it in a single database for ease of access.
