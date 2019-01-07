import os, codecs, re, sys, getopt, psycopg2

def main(argv):
  try:
    opts, args = getopt.getopt(argv,"hi:d:u:H:P:p:",["ifolder=","database=","username","host","port","password"])
  except getopt.GetoptError:
    print """test.py
    -i <inputfolder>
    -d <database>
    -u <username>
    -H <host>
    -P <port>
    -p <password>"""
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print """test.py
      -i <inputfolder>
      -d <database>
      -u <username>
      -H <host>
      -P <port>
      -p <password>"""
      sys.exit()
    elif opt in ("-i", "--ifolder"):
      inputfolder = arg
    elif opt in ("-d", "--database"):
      database = arg
    elif opt in ("-u", "--username"):
      username = arg
    elif opt in ("-H", "--host"):
      host = arg
    elif opt in ("-P", "--port"):
      port = arg
    elif opt in ("-p", "--password"):
      password = arg

  try: inputfolder
  except NameError: inputfolder = '../data-files/raw-text-files'

  try: database
  except NameError: database = 'ahiqar'

  try: username
  except NameError: username = 'postgres'

  try: host
  except NameError: host = 'localhost'

  try: port
  except NameError: port = '54320'

  try: password
  except NameError: password = 'mysecretkey'

  try:
    conn = psycopg2.connect("dbname='" + database + "' user='" + username + "' host='" + host + "' port='" + port + "' password='" + password + "'")
  except:
    print "I am unable to connect to the database"
  cur = conn.cursor()

  for fileName in os.listdir(inputfolder):
    if fileName.endswith(".txt"):
      f = codecs.open(os.path.join(inputfolder, fileName), encoding='utf-8')
      w = 0
      l = 0
      p = 0
      pageName = ''
      pageID = 0
      columnID = 0
      lineID = 0
      title = fileName.replace("_", " ").replace(".txt", "")
      cur.execute("""INSERT INTO manuscript (manuscript_name) VALUES(%s) RETURNING(manuscript_id)""",
                  (title,))
      conn.commit()
      manuscriptID = cur.fetchone()[0]
      for line in f:
          l += 1
          wl = 0
          for word in line.split():
              wl += 1
              w += 1
              page = re.search(r'\d{1,4}', word)
              if page:
                  pageName = page.group()
                  cur.execute("""INSERT INTO page (page_name, manuscript_id) VALUES(%s, %s) RETURNING(page_id)""",
                  (pageName, manuscriptID))
                  conn.commit()
                  pageID = cur.fetchone()[0]
                  cur.execute("""INSERT INTO col (col_name, page_id) VALUES(%s, %s) RETURNING(col_id)""",
                  ("0", pageID))
                  conn.commit()
                  columnID = cur.fetchone()[0]
                  l = 0
                  p += 1
              else:
                  if (wl == 1):
                      cur.execute("""INSERT INTO line (line_name, col_id) VALUES(%s, %s) RETURNING(line_id)""",
                      (str(l), columnID))
                      conn.commit()
                      lineID = cur.fetchone()[0]
                  cur.execute("""INSERT INTO word (word_address, surface, line_id, position_in_document) VALUES(%s, %s, %s, %s)""",
                  (title + "-" + pageName + "-" + str(l) + "-" + str(wl), word, lineID, w))
  conn.commit()
  cur.close()
  conn.close()

if __name__ == "__main__":
  main(sys.argv[1:])
