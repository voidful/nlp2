from .text import *


def doc2vec_aver(pretrained_emb, emb_size, context):
    docvec = [0] * emb_size
    count = len(context)
    for char in context:
        try:
            docvec = map(sum, zip(docvec, pretrained_emb[char]))
        except Exception as e:
            pass
    docvec = map(lambda x: x / count, zip(docvec, pretrained_emb[char]))
    return docvec.tolist()


def doc2vec_max(pretrained_emb, emb_size, context):
    arr_list = []
    for char in context:
        try:
            arr_list.append(pretrained_emb[char])
        except Exception as e:
            pass
    docvec = [max(row) for row in arr_list]
    return docvec.tolist()


def doc2vec_concat(pretrained_emb, emb_size, context):
    docvec = [0] * emb_size
    docvec = map(sum, zip(docvec, doc2vec_aver(pretrained_emb, emb_size, context)))
    docvec = map(sum, zip(docvec, doc2vec_max(pretrained_emb, emb_size, context)))
    return docvec.tolist()


def doc2vec_hier(pretrained_emb, emb_size, context, windows):
    arr_list = []
    for list in list_in_windows(context, windows):
        try:
            arr_list.append(doc2vec_aver(pretrained_emb, emb_size, list))
        except Exception as e:
            pass
    docvec = [max(row) for row in arr_list]
    return docvec.tolist()


def dot(A, B):
    return sum(a * b for a, b in zip(A, B))


def cosine_similarity(vector1, vector2):
    return dot(vector1, vector2) / ((dot(vector1, vector1) ** .5) * (dot(vector2, vector2) ** .5))
