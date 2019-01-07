# This is still incomplete.

import codecs
import re

f = codecs.open('Cod_Sach_339.txt', encoding='utf-8')
l = 0
p = 0
text = "<pb>"
for line in f:
    w = 0
    l += 1
    if l == 1:
        text += "<line n=\"" + str(l) + "\">"
    else:
        text += "</line><line n=\"" + str(l) + "\">"
    for word in line.split():
        w += 1
        page = re.search(r'\d{1,4}', word)
        if page:
            if p == 0:
                p += 1
                text = text[:3] + " xml:id=\"" + page.group() + "\" n=\"" + str(p) + "\">"
            else:
                text += "</pb><pb xml:id=\"" + page.group() + "\" n=\"" + str(p) + "\">"
            l = 0
            p += 1
        else:
            text += "<w n=\"" + str(w) + "\">" + word + "</w>"
print(text + "</line></pb>")
