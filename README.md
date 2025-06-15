# Flow Chemistry Experimental Generator

© 2025 Raminder S. Mulla. Released under the MIT License. 

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


### Outputs:
A typical output looks like this with user inputs highlighted:

Using interactive mode, two files are generated in your working directory. The first is a text file with taking the name of the experiment. Below is a representative example, with user selectable inputs and choices highlighted:

![Selection_419](https://github.com/user-attachments/assets/69f4b2e5-fafc-4ae1-8552-ae69635bd27a)


The second is a CSV file with columns capturing key parameters. For some users it may be more convenient to edit the CSV file directly to generate a prep. Just be sure not to do it in a traditional spreadsheet editor since they add formatting marks which the code cannot handle. For this reason, I suggest using [Tablecruncher.](https://tablecruncher.com/).

The CSV fields are documented here:

[csv-example.pdf](https://github.com/user-attachments/files/20747763/csv-example.pdf)

