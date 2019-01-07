import codecs, re, psycopg2, json, itertools, sys, getopt
from pprint import pprint

def main(argv):
  try:
    opts, args = getopt.getopt(argv,"hi:d:u:H:P:p:",["ifile=","database=","username","host","port","password"])
  except getopt.GetoptError:
    print """test.py
    -i <inputfile>
    -d <database>
    -u <username>
    -H <host>
    -P <port>
    -p <password>"""
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print  """test.py
      -i <inputfile>
      -d <database>
      -u <username>
      -H <host>
      -P <port>
      -p <password>"""
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
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

  try: inputfile
  except NameError: inputfile = '../data-files/collate-x-files/Ahiqar_collate.json'

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

  with open(inputfile) as f:
    data = json.load(f)

  try:
      conn = psycopg2.connect("dbname='" + database + "' user='" + username + "' host='" + host + "' port='" + port + "' password='" + password + "'")
  except:
      print "I am unable to connect to the database"
  cur = conn.cursor()

  parallelGroup = 0
  for parallel in data["table"]:
    groupIDs = []
    for group in parallel:
      parallelGroup += 1
      cur.execute(
        """INSERT INTO parallel_group (parallel_group_id)
        VALUES(%s)
        ON CONFLICT DO NOTHING""",
      ([parallelGroup]))
      conn.commit()
      print ("parallel group:", parallelGroup)
      groupIDs.append(parallelGroup)
      for entry in group:
        cur.execute(
          """UPDATE word
          SET parallel_group_id = %s
          WHERE word_address = %s RETURNING(parallel_group_id)""",
        (parallelGroup, str(entry["id"])))
        conn.commit()
        print ("Updated word: ", str(entry["id"]), " with group: ", str(parallelGroup))

    groupedPairs = list(itertools.permutations(groupIDs, 2))
    for pair in groupedPairs:
      print (pair)
      cur.execute(
        """INSERT INTO parallel_group_to_parallel_group (parallel_group_id_1, parallel_group_id_2)
        VALUES(%s, %s)
        ON CONFLICT DO NOTHING""",
      (str(pair[0]), str(pair[1])))

  conn.commit()
  cur.close()
  conn.close()

if __name__ == "__main__":
  main(sys.argv[1:])
