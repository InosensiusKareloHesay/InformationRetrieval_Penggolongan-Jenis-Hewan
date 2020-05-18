from bs4 import BeautifulSoup
from collections import Counter
import requests
import re

def crowling(url):
    web = requests.get(url)
    text_Web = web.text
    soup = BeautifulSoup(text_Web, 'lxml')
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))

def case_folding(kalimat):
    lower = kalimat.lower()
    return lower

def tokenizing(regex, kalimat):
    token = re.findall(regex,kalimat)
    return token

def filtering(dict_linkSatuan):
    open_stoplist = open("stoplist_tala.txt", "r")
    stoplists = open_stoplist.read()
    open_stoplist.close()
    stopwords = stoplists.split("\n")
    for word in stopwords:
        if word in dict_linkSatuan.keys():
            del dict_linkSatuan[word]
    return dict_linkSatuan

def PrioritasOperator(Katasatu,Katadua):
    ListKata = [Katasatu,Katadua]
    ListNilai = []
    for kata in ListKata:
        if (kata=="or"):
            ListNilai.append(1)
        elif (kata=="and"):
            ListNilai.append(2)
        elif (kata=="not"):
            ListNilai.append(3)
        elif (kata=="(" or kata ==")"):
            ListNilai.append(0)
    return (ListNilai[0] >= ListNilai[1])

def inputToPostfix(inputBoolean):
    Operator = []
    hasilPostfix = []
    token_Boolean = inputBoolean.split()
    for token in token_Boolean:
        if (case_folding(token) != "(" and case_folding(token) != ")" and case_folding(token) != "and" and case_folding(token) != "or" and case_folding(token) != "not"):
            hasilPostfix.append(token)
        elif (token == '('):
            Operator.append(token)
        elif (token == ')'):
            akhirStack = Operator.pop()
            while (akhirStack != '('):
                hasilPostfix.append(akhirStack)
                akhirStack = Operator.pop()
        else:
            while (len(Operator) != 0) and PrioritasOperator(case_folding(Operator[len(Operator)-1]),case_folding(token)):
                hasilPostfix.append(Operator.pop())
            Operator.append(token)
    while (len(Operator) != 0):
        hasilPostfix.append(Operator.pop())
    return " ".join(hasilPostfix)

def EvaluasiPostfix(listPostfix,DictIncidenceMatriks,file_link):
    outputHasil = []
    if (len(listPostfix) == 1):
        outputHasil.append(cariList(DictIncidenceMatriks, listPostfix[0]))
    else:
        for i in listPostfix:
            if (case_folding(i) == "and"):
                A = outputHasil[len(outputHasil) - 2]
                B = outputHasil[len(outputHasil) - 1]
                output = []
                for number in A:
                    if number in B:
                        output.append(number)
                if len(outputHasil) == 2:
                    outputHasil = []
                else:
                    outputHasil.pop()
                    outputHasil.pop()
                outputHasil.append(output)
            elif (case_folding(i)== "or"):
                A = outputHasil[len(outputHasil) - 2]
                B = outputHasil[len(outputHasil) - 1]
                if len(outputHasil) == 2:
                    outputHasil = []
                else:
                    outputHasil.pop()
                    outputHasil.pop()
                gabunganNumber = [number for number in A + B]
                output = list(set(gabunganNumber))
                outputHasil.append(output)
            elif (case_folding(i) == "not"):
                yangAkanDiNot = outputHasil[len(outputHasil) - 1]
                output = []
                for number in range(len(file_link)):
                    if (number not in yangAkanDiNot):
                        output.append(number)
                if len(outputHasil) > 1:
                    del outputHasil[len(outputHasil) - 1]
                    outputHasil.append(output)
                else:
                    outputHasil = []
                    outputHasil.append(output)
            else:
                output = cariList(DictIncidenceMatriks, i)
                outputHasil.append(output)
    return outputHasil

def cariList(semuaLink,cari):
    counter = 0
    simpanList = []
    for list in semuaLink:
        if (cari in list.keys()):
            simpanList.append(counter)
        counter += 1
    return simpanList

def cariLinkWebsite(outputHasil,file_link):
    link = []
    for i in outputHasil[0]:
        link.append(file_link[i])
    return link

def RUN():
    openFile = open("link2.txt", "r", encoding="utf-8")
    file_link = openFile.read().split()
    DictIncidenceMatriks = []
    for link in file_link:
        link_satuan = crowling('%s' % (link))
        link_caseFolding = case_folding(link_satuan)
        regexSplit = r"[a-z]+"
        kalimat_Inlink = tokenizing(regexSplit, link_caseFolding)
        dict_linkSatuan = Counter(kalimat_Inlink)
        DictIncidenceMatriks.append(filtering(dict_linkSatuan))
    while True:
        inputQuery= input("Yang Dicari = ")
        convert_toPostfix = inputToPostfix(inputQuery)
        listPostfix = convert_toPostfix.split()
        outputHasil = EvaluasiPostfix(listPostfix,DictIncidenceMatriks,file_link)
        ListDitemukan = cariLinkWebsite(outputHasil,file_link)
        for link in ListDitemukan:
            print(link)

if __name__ == '__main__':
    RUN()