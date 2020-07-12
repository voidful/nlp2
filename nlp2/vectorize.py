from .text import *


def doc2vec_aver(pretrained_emb, emb_size, context):
    docvec = [0] * emb_size
    count = len(context)
    for c in context:
        try:
            docvec = map(sum, zip(docvec, pretrained_emb[c]))
            docvec = map(lambda x: x / count, pretrained_emb[c])
        except Exception as e:
            pass
    return list(docvec)


def doc2vec_max(pretrained_emb, emb_size, context):
    arr_list = []
    for c in context:
        try:
            arr_list.append(pretrained_emb[c])
        except Exception as e:
            pass
    docvec = [max(row) for row in arr_list]
    return list(docvec)


def doc2vec_concat(pretrained_emb, emb_size, context):
    docvec = [0] * emb_size
    docvec = map(sum, zip(docvec, doc2vec_aver(pretrained_emb, emb_size, context)))
    docvec = map(sum, zip(docvec, doc2vec_max(pretrained_emb, emb_size, context)))
    return list(docvec)


def doc2vec_hier(pretrained_emb, emb_size, context, windows):
    arr_list = []
    for i in list_in_windows(context, windows):
        try:
            arr_list.append(doc2vec_aver(pretrained_emb, emb_size, i))
        except Exception as e:
            pass
    docvec = [max(row) for row in arr_list]
    return list(docvec)


def dot(A, B):
    return sum(a * b for a, b in zip(A, B))


def cosine_similarity(vector1, vector2):
    if vector1 == 0 or vector2 == 0:
        return 0
    return dot(vector1, vector2) / ((dot(vector1, vector1) ** .5) * (dot(vector2, vector2) ** .5))
