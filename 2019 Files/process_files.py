import os
import sys
import argparse
from libs.console_message import error, ok, info
from libs import docx_to_xml, apply_dict
import time


def is_valid_input_folder(arg):
    arg = arg + "/" if arg[-1:] != '/' else arg
    if not os.path.isdir(arg):
        assert isinstance(arg, str)
        error("\tThe folder \"%s\" does not exist!" % arg)
        sys.exit(1)
    else:
        file_count = 0
        for folder_file in os.listdir(arg):
            if folder_file.endswith(".docx"):  # Process the file if it is a txt file
                file_count += 1
        if file_count == 0:
            error("\tThe folder \"%s\" contains no docx files!" % arg)
            sys.exit(1)
        else:
            info("\tFound %i docx files in the folder \"%s\".\n" % (file_count, arg))

    return arg


def is_valid_dictionary_folder(arg):
    arg = arg + "/" if arg[-1:] != '/' else arg
    if not os.path.isdir(arg):
        assert isinstance(arg, str)
        error("\tThe folder \"%s\" does not exist!" % arg)
        sys.exit(1)

    return arg


def is_valid_output_folder(arg):
    arg = arg + "/" if arg[-1:] != '/' else arg
    if not os.path.isdir(arg):
        info("\tThe output folder \"%s\" does not exist yet, trying to create it." % arg)
        assert isinstance(arg, str)
        try:
            os.mkdir(arg)
        except OSError:
            error("\tCreation of the output folder \"%s\" failed" % arg)
            sys.exit(1)
        else:
            ok("\tSuccessfully created the output folder \"%s\"." % arg)

    return arg


def main():
    start_time = time.time()

    info("Converting files...")

    # Get Command line arguments
    parser = argparse.ArgumentParser(description='Prepare docx files for usage as tei.')
    parser.add_argument("-i", dest="unprocessed_folder", required=False, default="./input/",
                        help="the folder containing docx files for input; the default is \"./input/\".", metavar="INFOLDER",
                        type=lambda x: is_valid_input_folder(x))

    parser.add_argument("-d", dest="dictionary", required=False, default="./dictionaries/",
                        help="the folder containing dictionary files for xml transformation; the default is \"./dictionaries/\".", metavar="DICTFOLDER",
                        type=lambda x: is_valid_dictionary_folder(x))

    parser.add_argument("-o", dest="processed_folder", required=False, default="./output/",
                        help="the folder where the processed files will be placed; the default is \"./output/\".", metavar="OUTFOLDER",
                        type=lambda x: is_valid_output_folder(x))

    args = parser.parse_args()

    # Parse the docx files
    xml_dir = docx_to_xml.convert_to_xml(unprocessed_folder=args.unprocessed_folder, processed_folder=args.processed_folder)

    # Apply the dictionary to the xml files
    num_dictionary_entries, tei_path, num_tei_files = apply_dict.process_dictionary(args.dictionary, xml_dir, args.processed_folder)
    ok("Conversion and processing of files is complete.")
    info("All tasks completed in in %f seconds." % (time.time() - start_time))
    info("%i dictionary entries were applied to %i files." % (num_dictionary_entries, num_tei_files))
    info("The fully processed files are available in \"%s\"." % tei_path)


if __name__ == "__main__":
    main()
