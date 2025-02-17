import numpy as np

from nltk.chunk import RegexpParser
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

__all__ = [
    "extract_tags",
    "get_cat_tags",
]


def extract_tags(data):
    idxs = np.unique([x[0] for x in data.treepositions() if len(x) > 1])
    raw_data = [list(data[int(i)]) for i in idxs]

    tags = []
    for phrase in raw_data:
        skip = False
        res = ''
        for word in phrase:
            if word[0] == "able" and "JJ" in word[1]:
                skip = True
            else:
                res += word[0] + ' '

        if len(res) > 0 and not skip:
            tags.append(res[:-1])

    return tags

def get_cat_tags(a, verbose=False):
    if verbose:
        print()
        print('-'*100)
        print("\tRunning `get_cat_tags`...")
        print('-'*100)

    clf_tag_parser = RegexpParser(
        "CTAG: {\
            (<NN>|<NNS>|<NNP>|<NNPS>)?\
            ((<VB>|<VBD>|<VBG>|<VBN>|<VBP>|<VBZ>)<RB>?)+\
            <DT>?\
            (<JJ>|<JJR>|<JJS>)+\
            (<CC>(<JJ>|<JJR>|<JJS>))?\
            (<NN>|<NNS>|<NNP>|<NNPS>)?\
        }"
    )

    pos_tags = pos_tag(word_tokenize(a))
    if verbose:
        print("Part of Speech Tags:", pos_tags, '\n')

    data = clf_tag_parser.parse(pos_tags)
    if verbose:
        print("Matched Categorical Tags:", data)

    return extract_tags(data)
