import os, re
import pandas as pd
from tqdm import tqdm
import pickle

def listFiles():
    """Returns a list of all training data in the data/ folder"""
    return [f for f in os.listdir("../data") if f.endswith(".txt") and fname.find("-")>0]

def readFile(fname):
    """Given a file name `fname` or a list of filenames, returns its content"""
    if type(fname) == str:
        try:
            with open("../data/"+fname, 'rb') as f:
                data  = f.read().decode("utf8", "ignore")
        except:
            data = None
        return data
    elif type(fname) == list:
        return list(map(readFile, fname))
    else:
        raise TypeError("fname should be a string or a list of strings")

def getIterator():
    """Iterate over all training files amd get their content"""
    for fname in listFiles():
        tag = fname.split("-", 1)[0]
        yield tag, readFile(fname)

def asDataFrame(vectorizer=None):
    """
    Return a pandas DataFrame of all files,
    If a vectorizer function is passed, apply it on the textual data
    """
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
    """
    Return the training data and label, after replacing numbers with the <NUM> token, and removing non alpha numeric characters
    """
    X = []
    y = []
    digits = re.compile(r"\d[\d\.\$]*")
    not_allowed = re.compile(r"[^\s\w<>]")
    clean = lambda text: not_allowed.sub("", digits.sub("<NUM>",text.lower()))
    for fname in listFiles():
        tag, ind = fname.split("-", 1)
        body = clean(readFile(fname))
        y.append(tag)
        X.append(body)
    return (X,y)


def stemmed():
    """Apply Porter stemming on all documents in the training data, and return training data and label"""
    if os.path.exists("../data/stemmed_x.pickle"):
        with open("../data/stemmed_x.pickle", "rb") as f:
            X = pickle.load(f)
        with open("../data/stemmed_y.pickle", "rb") as f:
            y = pickle.load(f)
        return (X,y)
    import nltk
    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    X = []
    y = []
    punc = re.compile(r"[\.,;\(\)\s]+")
    not_allowed = re.compile(r"[^\sa-z]")
    clean = lambda text: not_allowed.sub("", punc.sub(" ",text.lower()))
    for fname in tqdm(listFiles()):
        if fname.find("-")<0:
            continue
        tag, ind = fname.split("-", 1)
        body = clean(readFile(fname))
        body = " ".join([porter.stem(w) for w in body.split()])
        y.append(tag)
        X.append(body)
    with open("../data/stemmed_x.pickle", "wb") as f:
        pickle.dump(X, f)
    with open("../data/stemmed_y.pickle", "wb") as f:
        pickle.dump(y, f)
    return (X,y)
