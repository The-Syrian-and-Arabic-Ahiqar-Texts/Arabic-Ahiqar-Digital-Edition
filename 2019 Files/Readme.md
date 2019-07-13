# DOCX File Preparation

## Description

The python program here will take a folder full of `docx` files and prepare them for usage in TEI/XML transcriptions. It will read the docx file and parse each new line into an <ab> element; it will also search for lines like "f.12", "f. 134r", or "p. 13" and wrap those in a <pb> element with the unique identifier in the `n` attribute (see line 34 of `libs/docx_to_xml.py` if the pattern matching needs to be extended).

In a second stage it will read a set of txt files with a list of comma separated keyword/tag pairs. This will search each text file for all keywords in thos files and wrap each instance in the specified tag.

## Usage

The program should work on python 2.7 and above. It relies on several dependencies: `python-docx`, `argparse`, and `colorama` (for nicer console output). Most standard python installs will have these, with the exception of `python-docx`; you can install that with your package manager of choice: probably either `pip install python-docx` or `conda install python-docx`.

The program is run with the command `python process_files.py`; adding the `-h` switch `python process_files.py -h` will provide a short description of the command line options. As a default, it expects a `dictionaries` folder with one or more `txt` files as described above. By default it will read all `docx` files in the `input` folder and output the processed files to the `output` folder in two stages: `output/xml` will contain the converted `docx` files without the substitutions from the dictionaries; the `output/tei-prep` folder containes the fully processed files, each of which can be dropped into a properly formatted tei file. All of these settings can be manually set with command line switches `python process_files.py -i /path/to/my/input/files -o /path/to/my/output/files -d /path/to/my/dictionaries`.