# Flow Experimental Generator

## In brief:

This is a Python script built on [questionary](https://pypi.org/project/questionary/) and [pandas](https://pypi.org/project/pandas/) that asks the user a series of questions to help generate:

*   A human readable flow chemistry experimental for use in a lab notebook
*   A CSV file containing reaction parameters relevant to a flow chemist; this may be used for databasing reactions, or machine learning applications.

## Usage:

### For interactive mode:

```python
python generator.py
```

If you already have a CSV file from a previous round of answering the questions, you can specify its location and obtain an experimental from it. 

The precedure for writing an experimental looks like this:

![Peek 2025-06-10 23-43](https://github.com/user-attachments/assets/ec783f72-c65b-48a4-9adf-0c891bffa6f2)

The CSV (with your chosen name) and an accompanying text file with the terminal output are saved in your working directory.

### For non-interactive mode:

```python
  python generator.py -n your_directory_here
```

Non-interactive mode takes a directory containing generator-compatible csv files and outputs text files containing an experimental write-up. 

If you want, you can make generator compatible csv files using the included examples as templates, which may save you some time.
