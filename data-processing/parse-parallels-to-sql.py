# I think this is no longer needed.

# import codecs
# import re
# import psycopg2
# import json
# import itertools
# from pprint import pprint

# with open('Ahiqar_collate.json') as f:
#     data = json.load(f)

# # print(data["table"][0][0][0]["t"])
# # print(data["table"][0][0][1]["t"])

# try:
#     conn = psycopg2.connect("dbname='ahiqar' user='postgres' host='localhost' port='32768' password='mysecretkey'")
# except:
#     print "I am unable to connect to the database"
# cur = conn.cursor()

# for parallel in data["table"]:
#     lengths = [len(entry) for entry in parallel]
#     if (len(set(lengths)) == 1):
#         print("match")
#         matches = [list(i) for i in zip(*parallel)]
#         for idx, val in enumerate(matches):
#             print (str(idx + 1))
#             pairs = list(itertools.permutations(val, 2))
#             for pair in pairs:
#                 cur.execute("""INSERT INTO word_to_word (word_address, parallel_address) VALUES(%s, %s)""",
#                 (pair[0]["id"], pair[1]["id"]))
#                 print "Pair: %s; %s" % (pair[0]["id"], pair[1]["id"])
#     else:
#         print("different")
#         groups = list(itertools.product(*parallel))
#         for group in groups:
#             sorted = list(itertools.permutations(group, 2))
#             for pair in sorted:
#                 cur.execute("""INSERT INTO word_to_word (word_address, parallel_address) VALUES(%s, %s)""",
#                 (pair[0]["id"], pair[1]["id"]))
#                 print "Pair: %s; %s" % (pair[0]["id"], pair[1]["id"])

# conn.commit()
# cur.close()
# conn.close()
