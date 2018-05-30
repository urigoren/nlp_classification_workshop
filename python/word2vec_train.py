import sys, os, json
from gensim.models import Word2Vec
from argparse import ArgumentParser


class DirSentences(object):
    def __init__(self, *args):
        self.dirs = args
        self.len = None

    def __len__(self):
        if self.len is not None:
            return self.len
        ret = 0
        for dirname in self.dirs:
            for fname in os.listdir(dirname):
                with open(f"{dirname}/{fname}", "rb") as f:
                    content = f.read().decode("utf-8", "ignore")
                    ret += len(content.split("\n"))
        self.len = ret
        return ret

    def __iter__(self):
        total_len = 0
        for dirname in self.dirs:
            for fname in os.listdir(dirname):
                with open(f"{dirname}/{fname}", "rb") as f:
                    content = f.read().decode("utf-8", "ignore")
                    for line in content.split("\n"):
                        yield line.split()
                        total_len += 1
        self.len = total_len


def main(params):
    if os.path.exists(params.model):
        print ("Loading previous model " + params.model)
        model = Word2Vec.load(params.model)
    else:
        print("Creating new model and building vocab")
        model = Word2Vec(iter=1, min_count=params.minTF, workers=params.workers, size=params.size, window=params.window)
        with open(params.vocab, 'r') as f:
            vocab_freq = json.load(f)
        model.build_vocab_from_freq(vocab_freq)
        print("Vocab generation done {c} words".format(c=len(model.wv.vocab)))
    print("Training model")
    train_sentences = DirSentences(*params.input.split(','))
    model.train(train_sentences, total_examples=len(train_sentences), epochs=1)
    print("Saving model to " + params.model)
    model.save(params.model)
    return 0


if __name__ == "__main__":
    argparse = ArgumentParser()
    argparse.add_argument('--window', default=5, type=int, help='window size')
    argparse.add_argument('--size', default=50, type=int, help='vector size')
    argparse.add_argument('--workers', default=4, type=int, help='number of processes')
    argparse.add_argument('--minTF', default=4, type=int, help='minimum term frequency')
    argparse.add_argument('--model', default='w2v.pickle', type=str, help='model file')
    argparse.add_argument('--input', default='TrainDir', type=str, help='dirs to learn from, comma separated')
    argparse.add_argument('--vocab', default='vocab.json', type=str, help='vocab frequency file, in json format')
    params = argparse.parse_args()
    sys.exit(main(params))
