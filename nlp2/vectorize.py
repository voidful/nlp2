from numpy import dot
from numpy.linalg import norm
import numpy as np
from .text import *


def doc2vec_aver(pretrained_emb, emb_size, context):
    docvec = np.zeros(emb_size)
    sent_count = len(passage_into_sentences(context))
    for sentence in passage_into_sentences(context):
        if len(sentence) > 0:
            for char in spilt_sentence_to_array(sentence, True):
                try:
                    docvec = np.add(docvec, pretrained_emb[char])
                except Exception as e:
                    pass
            docvec = np.divide(docvec, np.full(self._vec_size, len(sentence)))
    docvec = np.divide(docvec, np.full(self._vec_size, sent_count))
    return docvec.tolist()


def doc2vec_max(pretrained_emb, emb_size, context):
    arr_list = []
    for sentence in passage_into_sentences(context):
        if len(sentence) > 0:
            for char in spilt_sentence_to_array(sentence, True):
                try:
                    arr_list.append(pretrained_emb[char])
                except Exception as e:
                    pass
    docvec = np.amax(arr_list, axis=0)
    return docvec.tolist()


def doc2vec_concat(pretrained_emb, emb_size, context):
    docvec = np.zeros(emb_size)
    docvec = np.add(docvec, doc2vec_aver(pretrained_emb, emb_size, context))
    docvec = np.add(docvec, doc2vec_max(pretrained_emb, emb_size, context))
    return docvec.tolist()
