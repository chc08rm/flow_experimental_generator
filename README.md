# Flow Chemistry Experimental Generator

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

>In a flow reactor were combined ==C1(Cl)=CC(=C(Br)C=N1)Cl (1.0 eq., 0.3M in C1CCOC1)== dosed in at a flow rate of ==17 mL min⁻¹== and ==CCCCCC[Li]== (==1.1 eq., 2.3M== in ==CCCCCC==) dosed in at a flow rate of 2.439 mL min⁻¹ to a ==T-mixer(φ=500 µm).== The resulting mixture was held for a residence time of ==1.0 s== at a bath T of ==-70°C==, with an ==in-line T of -50°C==, prior to being combined with ==C[Si](C)(Cl)C== (==1.2 eq.==, ==1.0M== in ==C1CCOC1==) dosed in at a flow rate of 6.12 mL min⁻¹ to a ==T-mixer(φ=500 µm)==. The resulting mixture was held for a residence time of ==6.0 s== at a bath T of ==-70°C==, prior to being collected into ==NH4Cl==. ==Steady state ==collection was performed by infusing at least 3 residence times of all feed solutions through the reactor. Yields are reported on this basis. ==N1C(Cl)=CC(=C(C=1)[Si](C)(C)C)Cl== was obtained in ==70%== yield by ==1H NMR== measurement.

The second is a CSV file with columns capturing key parameters. For some users it may be more convenient to edit the CSV file directly to generate a prep. Just be sure not to do it in a traditional spreadsheet editor since they add formatting marks which the code cannot handle. For this reason, I suggest using [Tablecruncher.](https://tablecruncher.com/).

The CSV fields are documented here:

