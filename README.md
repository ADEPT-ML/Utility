# ADEPT Utilities 🛠️

This repository contains (Python) utilities to facilitate working with the raw data used in the ADEPT project.

<p align="center">
  <a href="https://github.com/ADEPT-ML/Server">Main Repo</a> | 
  <a href="blank">Documentation</a> |
  <a href="https://www.tu-dortmund.de/en/university/sustainabilitiy/">Sustainabilitiy at TU Dortmund</a>
</p>

## List of utilies

- [combinator](#combinator)

---

## Combinator

This utility can be used to combine different .xls files. Its main purposes are:
- Combining data from the same building but with different (overlapping) time frames (when new data has been published)
- Combining data from two different buildings over the same time period (as this is not directly supported in ADEPT)

### Prerequisites

- Python >= 3.10
- venv (recommended)
  ```sh
  # init venv
  python3 -m venv venv
  source venv/bin/activate
  ```


### Installation

```sh
# install requirements, start combinator
pip3 install -r requirements.txt
cd combinator
python3 combinator.py
# -> follow the instructions in the terminal
```