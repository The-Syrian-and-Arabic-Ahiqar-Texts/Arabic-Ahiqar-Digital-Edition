import os
import re


## Read every txt file in the folder and wrap any lines like f.1
## in a <pb> milestone. Otherwise wrap the whole line in an <ab>.
def convert_files():
    folio_designation = re.compile(r'.*f.*\..*[0-9].*')
    leave_alpha_num = re.compile('[^A-z0-9.]')

    unprocessed_folder = "./unprocessed/"
    processed_folder = "./partially-processed-tei/"

    # Get all files in the folder
    for folder_file in os.listdir(unprocessed_folder):
        if folder_file.endswith(".txt"):  # Process the file if it is a txt file
            print("Found " + folder_file)

            # Create an output file for the updated file
            write_file = open(processed_folder + folder_file[0:-4] + ".xml", "w")

            # Open the file to be read
            with open(unprocessed_folder + folder_file) as fp:
                line = fp.readline()

                # Loop through every line
                while line:
                    line = line.strip()  # Strip any whitespace
                    if folio_designation.match(line): # If line matches folio regex, wrap it in a <pb>
                        line = leave_alpha_num.sub('', line)
                        write_file.write("<pb n=\"" + line + "\"/>\n")
                    else:  # Otherwise wrap it in a <ab>
                        write_file.write("<ab>" + line + "</ab>\n")
                    line = fp.readline()

            # Close the file
            write_file.close()
            print("Wrote new file " + processed_folder + folder_file[0:-4] + ".xml")


convert_files()
