#CollateX instructions
You can first need to download the [collatex-tools-1.7.1.jar](https://oss.sonatype.org/service/local/repositories/releases/content/eu/interedition/collatex-tools/1.7.1/collatex-tools-1.7.1.jar).

The command should be formatted as follows: `java -jar collatex-tools-1.7.1.jar Ahiqar-Two_Witnesses.json -f tei -o Test-Output.xml`.

You must put the name of the input file or files directly after `java -jar collatex-tools-1.7.1.jar`.

The switch `-f` tells CollateX the output format you want.  This can be `json`, `csv`, `dot`, `graphml`, or `tei`.

The switch `-o` tells CollateX where you want to store your output.  It is probably a good idea to match the file extension to the file format you selected: `.json`, `.csv`, `.dot`, `.graphml`, or `.tei` (you may want to save the tei file as `.xml`.

Further documentation can be found at <https://collatex.net/doc/#cli>.

###Using CollateX with Excel

If you want to view the results of CollateX in an Excel spreadsheet, you will need to go through several steps.

1.	You must generate output in the CSV file format: `java -jar collatex-tools-1.7.1.jar Ahiqar-Two_Witnesses.json -f csv -o Excel-output.csv`
2. You cannot open the resulting CSV file `Excel-output.csv` in Excel.  Instead you must import it.
3. Create a new empty Excel file.
4. Click on `File` and then `import`.
5. The type of file you wish to import is CSV, select that, then click the Import button.
6. Select the CSV file you just created (`Excel-output.csv`) and click Get Data.
7. The data type should be "Delimited" __not__ "Fixed width", which seems to be the default on my machine.
8. The "File origin" __must be__ "Unicode (UTF-8)", the default setting for this was also incorrect on my maching.
9. Now with "Delimited" and "Unicode (UTF-8)" selected, click on the Next > button.
10. Now uncheck the "Tab" select box and check the "Comma" select box, then click on the Next > button.
11. Finally, you should click on each column and set the "Column data format" to "Text", then click on the Finish button.
12. It will now ask you where to put the data.  It is probably best to just put it in a "New sheet", but it likely doesn't matter much. 

-
Prepared for Aly Elrefaei by [Bronson Brown-deVost](bronsonbdevost@aim.com).   
1 March 2018.