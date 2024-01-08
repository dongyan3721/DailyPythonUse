import os
import re
from docx import Document


def parseKeyWorks(dest):
    file_names = os.listdir(dest)
    files = []
    for f in file_names:
        if re.search("^.+docx?$", f):
            files.append(f)

    extracted_text = []

    for file in files:
        doc = Document(dest + '\\' + file)
        temp = ""
        for paragraph in doc.paragraphs:
            temp += paragraph.text
        extracted_text.append(temp)

    p = r"(被告人.+?犯.+?罪，判处[有无期死徒刑拘役]+.+?。)"
    p1 = r"犯(.+?罪)"
    p2 = r"判处([有无期死徒刑拘役]+)([零一二三四五六七八九十百千万个年月0-9]+)?"
    p3 = r"([处罚金没收财产人民币]+[零一二三四五六七八九十百千万0-9]+*元)"

    for i in range(len(extracted_text)):
        s = re.findall("判决如下：?(.+?)如不服本判决", extracted_text[i])
        if len(s) == 1:
            l1 = re.findall(p, s[0])
            l2 = re.findall(p1, s[0])
            l3 = re.findall(p2, s[0])
            l4 = re.findall(p3, s[0])

            fp = open(files[i] + ".txt", "w+")
            for j in l1:
                fp.write(j)
                fp.write('\n')
            for j in l2:
                fp.write(j)
                fp.write('\n')
            for j in l3:
                if j[-1] == '':
                    fp.write(j[0])
                    fp.write('\n')
                else:
                    for k in j:
                        fp.write(k)
                        fp.write('\n')
                fp.write('\n')
            for j in l4:
                fp.write(j)
                fp.write('\n')
            fp.close()


if __name__ == "__main__":
    parseKeyWorks("C:\\Users\\29145\\Desktop\\刑事案件（全）\\docxed")
