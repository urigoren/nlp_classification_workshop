# NLP classification workshop for beginners
## Prerequisites
 1.  Python 3.6 installed
 1.  Pip (`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py`)
 1.  Jupyter notebook

## Recommended software for Windows users
 1. Anaconda: https://www.anaconda.com/download/#windows
 1. cmder: https://github.com/cmderdev/cmder/releases/download/v1.3.6/cmder.zip

## Installation steps

 1.  Clone this repository
 1.  Download the training data from: http://goren.ml/pdnlp
 1.  Extract it to `data/`
 1.  Make sure all the requirements are installed `pip3 install -r requirements.txt` OR `conda install --yes --file requirements.txt` if you're with Anaconda
 1.  Launch Jupyter by running `cd notebooks; jupyter notebook` in your terminal


## Dataset

 1.  `data.zip` - The raw contracts, classified by their filename
 1.  `stemmed.zip` - The contracts after preprocessing and stemming (here to save you time)
 1.  `w2v.pickle` - Word2Vec model trained on the data (`gensim` model)
 1.  `test_data.zip` - Unlabeled contracts, for those who would like to participate in the competition ( http://goren4u.com/nlp_classification/ )


