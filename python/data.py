import os, re
import pandas as pd
from tqdm import tqdm

def listFiles():
    return [f for f in os.listdir("../data") if f.endswith(".txt")]

def readFile(fname):
    if type(fname) == str:
        try:
            with open("../data/"+fname, 'r') as f:
                data  = f.read()
        except:
            data = None
        return data
    elif type(fname) == list:
        return list(map(readFile, fname))
    else:
        raise TypeError("fname should be a string or a list of strings")

def getIterator():
    for fname in listFiles():
        tag = fname.split("-", 1)[0]
        yield tag, readFile(fname)

def asDataFrame(vectorizer=None):
    ret = []
    if vectorizer is None:
        cols = ["num", "file", "tag"]
    else:
        cols = ["num", "vector", "tag"]
    for fname in listFiles():
        if fname.find("-")<0:
            continue
        tag, ind = fname.split("-", 1)
        if vectorizer is None:
            ret.append((int(ind.split(".", 1)[0]), fname, tag))
        else:
            ret.append((int(ind.split(".", 1)[0]), vectorizer(readFile(fname)), tag))
    return pd.DataFrame(ret, columns=cols).set_index("num")

def preprocessed():
    X = []
    y = []
    digits = re.compile(r"\d[\d\.\$]*")
    not_allowed = re.compile(r"[^\s\w<>]")
    clean = lambda text: not_allowed.sub("", digits.sub("<NUM>",text.lower()))
    for fname in listFiles():
        if fname.find("-")<0:
            continue
        tag, ind = fname.split("-", 1)
        body = clean(readFile(fname))
        y.append(tag)
        X.append(body)
    return (X,y)


def stemmed():
    import nltk
    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    X = []
    y = []
    punc = re.compile(r"[\.,;\(\)\s]+")
    not_allowed = re.compile(r"[^\s\w]")
    clean = lambda text: not_allowed.sub("", punc.sub(" ",text.lower()))
    for fname in tqdm(listFiles()):
        if fname.find("-")<0:
            continue
        tag, ind = fname.split("-", 1)
        body = clean(readFile(fname))
        body = " ".join([porter.stem(w) for w in body.split()])
        y.append(tag)
        X.append(body)
    return (X,y)
