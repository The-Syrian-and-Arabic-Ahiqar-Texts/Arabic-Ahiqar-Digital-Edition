import subprocess
# TODO, check for DB and reset if exists (work wth Docker).
# Process images: create jp2's, link them to URLS.

print "Building collateX input from raw text files."
buildCollXData = subprocess.check_output([
  'python',
  'build-collateX-input.py'])
print "Finished building collateX input from raw text files."

print "Processing collateX input data for JSON output."
processCollXDataJSON = subprocess.check_output([
  'java',
  '-jar',
  'collatex-tools-1.7.1.jar',
  '../data-files/collate-x-files/collate-x-witnesses.json',
  '-f',
  'json',
  '-o',
  '../data-files/collate-x-files/Ahiqar_collate.json'])
print "Finished processing collateX input data for JSON output."

print "Processing collateX input data for TEI output."
processCollXDataTEI = subprocess.check_output([
  'java',
  '-jar',
  'collatex-tools-1.7.1.jar',
  '../data-files/collate-x-files/collate-x-witnesses.json',
  '-f',
  'tei',
  '-o',
  '../data-files/collate-x-files/Ahiqar_collate.tei'])
print "Finished processing collateX input data for TEI output."

print "Importing raw txt files to database."
buildCollXData = subprocess.check_output([
  'python',
  'parse-manuscript-to-sql.py'])
print "Finished importing raw txt files to database."

print "Importing collateX output into database."
buildCollXData = subprocess.check_output([
  'python',
  'parse-parallel-groups-to-sql.py'])
print "Finished importing collateX output into database."
