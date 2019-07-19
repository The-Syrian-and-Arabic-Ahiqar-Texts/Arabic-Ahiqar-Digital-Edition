import os
import re
import sys
from docx import Document
from libs.console_message import ok, info, warning, error


def __prepare_xml_output_folder(processed_folder):
    processed_folder = processed_folder + "xml/" if processed_folder[-1:] == "/" else processed_folder + "/xml/"
    if not os.path.isdir(processed_folder):
        info("\tDirectory \"%s\" doesn't yet exist. Trying to create it." % processed_folder)
        assert isinstance(processed_folder, str)
        try:
            os.mkdir(processed_folder)
        except OSError:
            error("\tCreation of the output directory \"%s\" failed" % processed_folder)
            sys.exit(1)
        else:
            ok("\tSuccessfully created the output directory \"%s\".\n" % processed_folder)
    return processed_folder


def convert_to_xml(unprocessed_folder, processed_folder):
    # type: (str, str) -> str
    """
Read every txt file in the folder and wrap any lines like f.1a
in a <pb> milestone. Otherwise wrap the whole line in an <ab>.
    :param unprocessed_folder: The folder containing unprocessed docx files
    :param processed_folder: The output folder for the processed xml files
    :rtype: None
    """
    info("\nConverting the docx files to xml.")
    processed_folder = __prepare_xml_output_folder(processed_folder)
    folio_designation = re.compile(r'.*[f|p].*\..*[0-9].*')
    leave_alpha_num = re.compile('[^A-z0-9.]')

    # Get all files in the folder
    for folder_file in os.listdir(unprocessed_folder):
        if folder_file.endswith(".docx"):  # Process the file if it is a txt file
            info("\tFound " + folder_file)

            # Create an output file for the updated file
            write_file = open(processed_folder + folder_file[0:-5] + ".xml", "w", encoding='utf8')

            # Open the file to be read
            doc = Document(unprocessed_folder + folder_file)
            for para in doc.paragraphs:
                line = str(para.text.strip())  # Strip any whitespace
                if folio_designation.match(line):  # If line matches folio regex, wrap it in a <pb>
                    line = leave_alpha_num.sub('', line)
                    write_file.write("<pb n=\"" + line + "\"/>\n")
                else:  # Otherwise wrap it in a <ab>
                    write_file.write("<ab>" + line + "</ab>\n")

            # Close the file
            write_file.close()
            ok("\tWrote new file " + processed_folder + folder_file[0:-5] + ".xml\n")

    return processed_folder
