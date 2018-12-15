from numpy import dot
from numpy.linalg import norm
import numpy as np
from .text import *


def doc2vec_aver(pretrained_emb, emb_size, context):
    docvec = np.zeros(emb_size)
    count = len(context)
    for char in context:
        try:
            docvec = np.add(docvec, pretrained_emb[char])
        except Exception as e:
            pass
    docvec = np.divide(docvec, np.full(self._vec_size, count))
    return docvec.tolist()


def doc2vec_max(pretrained_emb, emb_size, context):
    arr_list = []
    for char in context:
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


def doc2vec_hier(pretrained_emb, emb_size, context, windows):
    arr_list = []
    for list in list_in_windows(context, windows):
        try:
            arr_list.append(doc2vec_aver(pretrained_emb, emb_size, list))
        except Exception as e:
            pass
    docvec = np.amax(arr_list, axis=0)
    return docvec.tolist()
