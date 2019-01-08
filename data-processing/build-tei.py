# This is still incomplete.

import codecs, re, sys, getopt, os
def main(argv):
    inputfile = "Cod_Sach_339.txt"
    outputfolder = "./"
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofolder="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfolder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfolder> -o <outputfolder>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofolder"):
            outputfolder = arg
    print 'Converting', inputfile, "to tei xml format."
    f = codecs.open(inputfile, encoding='utf-8')
    l = 0
    p = 0
    w = 0
    currentLine = 0
    text = "<body>"
    for line in f:
        currentLine += 1
        for word in line.split():
            w += 1
            page = re.search(r'\d{1,4}', word)
            if page:
                p += 1
                text += "<pb n=\"" + str(p) + "\"/>"
                currentLine = 0
                l = currentLine + 1
                text += "<lb n=\"" + str(1) + "\"/>"
            else:
                if currentLine != l:
                    l = currentLine
                    text += "<lb n=\"" + str(currentLine) + "\"/>"
                text += "<w n=\"" + str(w) + "\">" + word + "</w>"
    text += "</body>"
    outfile = outputfolder + os.path.splitext(os.path.basename(inputfile))[0] + ".tei"
    print "The file has been output to:", outfile
    file = codecs.open(outfile, "w", "utf-8")
    file.write(text)
    file.close()

if __name__ == "__main__":
   main(sys.argv[1:])