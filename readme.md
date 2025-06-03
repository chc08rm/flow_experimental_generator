# Flow Experimental Generator

## In brief:

This is a Python script built on questionary and pandas, which asks the user a series of questions to generate:

*   A human readable flow chemistry experimental for use in a lab notebook
*   A CSV file containing reaction parameters relevant to a flow chemist; this may be used for databasing reactions, or machine learning applications.

## Usage:

### For interactive mode:

```python
python generator.py
```

If you already have a CSV file from a previous round of answering the questions, you can specify its location and obtain an experimental from it. 

The precedure for writing an experimental looks like this:

\[\]

The CSV (with your chosen name) and a text file called "output.txt," are saved in your working directory.

### For non-interactive mode:

```python
  python generator.py -n your_directory_here
```

Non-interactive mode takes a directory containing generator-compatible csv files and outputs text files containing an experimental write-up.