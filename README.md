# BASTFOIL Scraper

This is a compound scraper module for BLASTFOIL database population. It gathers airfoil data from different sources and stores it in a single database.

> [!NOTE]
> All instructions in this README assume your Python 3.11.6+ installation is in your PATH and is aliased under `python`. If this is not the case, you will need to replace `python` with the alias or path that points to the correct Python executable.

## Installation

```bash
git clone https://github.com/BLASTFOIL/bfscraper.git
cd bfscraper
# Consider using a virtual environment prior to installing.
python -m pip install .
```

## Usage

Calling the module will automatically scrape all sources and store the data in a single database.

```bash
python -m bfscraper [<limit>]
```

The `limit` argument is optional and will limit the number of airfoils scraped from each source. If not specified, all airfoils will be scraped.

## Sources

This is the list of domains that are currently supported for scraping:

- [BigFoil](https://bigfoil.ae.illinois.edu)
- [AirfoilTools](https://airfoiltools.com) (included in the BigFoil source)

## Disclaimer

All information presented herein is delivered without guarantee or warranty of any kind. The user assumes the entire risk of use of this information. In no event shall any person be liable for any direct, indirect, consequential or incidental damages arising from the use of, or reliance on, this information. This information is subject to change without notice.

This tool is not, in any way, related to any of the sources mentioned above. It is an independent project that aims to gather data from different sources and store it in a single database for ease of access.
