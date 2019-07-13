import os
import re
import sys
from console_message import ok, info, warning, error


def __check_dictionary_folder(dictionary_folder):
    file_count = 0
    for folder_file in os.listdir(dictionary_folder):
        if folder_file.endswith(".txt"):  # Process the file if it is a txt file
            file_count += 1
    if file_count == 0:
        warning("\tThe folder \"%s\" contains no txt files!" % dictionary_folder)
        info("Nothing more to do. Exiting without applying dictionary files.")
        sys.exit(0)
    else:
        info("\tFound %i txt dictionary files in the folder \"%s\".\n" % (file_count, dictionary_folder))


def __prepare_xml_output_folder(processed_folder):
    processed_folder = processed_folder + "tei-prep/" if processed_folder[-1:] == "/" else processed_folder + "/tei-prep/"
    if not os.path.isdir(processed_folder):
        info("\t\tDirectory \"%s\" doesn't yet exist. Trying to create it." % processed_folder)
        assert isinstance(processed_folder, str)
        try:
            os.mkdir(processed_folder)
        except OSError:
            error("\t\tCreation of the output directory \"%s\" failed" % processed_folder)
            sys.exit(1)
        else:
            ok("\t\tSuccessfully created the output directory \"%s\".\n" % processed_folder)
    return processed_folder


# Read the dictionary txt files from "./dictionaries".
# Those files should all have a list of wrod pairs
# in the format "word,tag\n".
def __build_dict(dict_folder):
    info("\tBuilding complete dictionary.")
    __check_dictionary_folder(dict_folder)
    dictionary = {}
    check_alpha_num = re.compile(r"[^A-z0-9]")

    # Loop over each file in the folder
    for folder_file in os.listdir(dict_folder):

        # Process it if it is a txt file
        if folder_file.endswith(".txt"):

            # Start an entry count for this file
            file_entries = 0
            info("\t\tFound " + folder_file)

            # Open the dictionary file
            with open(dict_folder + folder_file) as fp:
                line = fp.readline()
                lineCount = 1

                # Loop through each line in the file
                while line:
                    line = line.strip()  # Strip any accidental whitespace
                    entry = line.split(',')  # Split on the ","
                    # Process the line if it has a valid entry with only two items, and the second is only alphanumeric
                    if len(entry) == 2 and not check_alpha_num.findall(entry[1].strip()):
                        dictionary[entry[0].strip()] = entry[1].strip()  # Create the new entry in the dictionary (any old one is overwritten)
                        file_entries += 1
                    else: # Notify the user of the error
                        warning("\t\tThere is an error in line " + str(lineCount) + " of " + folder_file + ".")
                        error(line)

                    lineCount += 1
                    line = fp.readline()

            ok("\t\tFinished parsing " + folder_file + ": " + str(file_entries) + " entries.\n")
    ok("\tFinished loading dictionaries. " + str(len(dictionary)) + " entries in total.\n")
    return dictionary


# Apply the dictionary to all the text transcriptions.
# This reads the files line by line and applies the substitution
# then writes the altered line to a new file.

# This is not optimized at all, so might get really slow with a large dictionary.
# If so, maybe just read the whole file in as a string, then loop over the entry
# replacements, and then write the whole thing to a new file.
def __apply_dictionary(dictionary, xml_path, output_path):
    info("\tApplying dictionary to xml files.")
    output_path = __prepare_xml_output_folder(output_path)
    num_tei_files = 0

    # Loop over each file in the folder
    for folder_file in os.listdir(xml_path):
        # Process it if it is an xml file
        if folder_file.endswith(".xml"):
            info("\t\tFound " + folder_file)
            # Create an output file
            write_file = open(output_path + folder_file[0:-4] + ".xml", "w")

            # Open the file that will be read
            with open(xml_path + folder_file) as fp:
                line = fp.readline()

                # Loop over every line (see line 62)
                while line:

                    # Check if any of the keys in the dictionary occur in the line
                    for key, value in dictionary.iteritems():
                        # If a key exists, then replace it
                        if key in line:
                            line = line.replace(key, "\n<" + value + ">" + key + "</" + value + ">\n")
                    write_file.write(line)
                    line = fp.readline()

            # Write the new file
            write_file.close()
            ok("\t\tWrote new file " + output_path + folder_file[0:-4] + ".xml\n")
            num_tei_files += 1
    ok("\tFinished applying dictionary to all xml files.")
    ok("\tThe processed files have been output to the folder \"%s\"." % output_path)
    return output_path, num_tei_files


def process_dictionary(dictionary_path, xml_path, output_path):
    info("Processing the dictionaries.")
    full_dictionary = __build_dict(dictionary_path)
    output_path, num_tei_files = __apply_dictionary(full_dictionary, xml_path, output_path)
    return len(full_dictionary), output_path, num_tei_files
