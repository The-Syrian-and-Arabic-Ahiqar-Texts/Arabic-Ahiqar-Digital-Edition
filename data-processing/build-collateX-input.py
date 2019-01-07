import os, codecs, re, sys, getopt

def main(argv):
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifolder=","ofolder="])
  except getopt.GetoptError:
    print 'test.py -i <inputfolder> -o <outputfolder>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'test.py -i <inputfolder> -o <outputfolder>'
      sys.exit()
    elif opt in ("-i", "--ifolder"):
      inputfolder = arg
    elif opt in ("-o", "--ofolder"):
      outputfolder = arg

  try: inputfolder
  except NameError: inputfolder = '../data-files/raw-text-files'

  try: outputfolder
  except NameError: outputfolder = '../data-files/collate-x-files'

  text = "{\"witnesses\":["
  for filename in os.listdir(inputfolder):
    if filename.endswith(".txt"):
      title = filename.replace("_", " ").replace(".txt", "")
      text += "{\"id\":\"%(title)s\",\"tokens\":[" % locals()
      f = codecs.open(os.path.join(inputfolder, filename), encoding='utf-8')
      l = 0
      p = 0
      pageName = ''
      for line in f:
        l += 1
        w = 0
        for word in line.split():
          page = re.search(r'\d{1,4}', word)
          if page:
            pageName = page.group()
            l = 0
            p += 1
          else:
            w += 1
            # TODO I don't have a search function for adding columns yet
            text += "{\"t\":\"%(word)s\",\"id\":\"" % locals() + title + "-" + pageName + "-1-" + str(l) + "-" + str(w) + "\",\"line\":\"%(l)s\",\"page\":\"%(pageName)s\"}," % locals()

      text = text[:-1] + "]},"
  text = text[:-1] + "]}"
  file = codecs.open(outputfolder + "/collate-x-witnesses.json","w", "utf-8")
  file.write(text)
  file.close()


if __name__ == "__main__":
   main(sys.argv[1:])

