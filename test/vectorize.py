import unittest
from nlp2.vectorize import *
import gensim

model = gensim.models.KeyedVectors.load_word2vec_format("fileloc")
model_size = 300


class TestVectorize(unittest.TestCase):

    def test_doc2vec_max(self):
        v1 = doc2vec_max(model, model_size, "你好")
        v2 = doc2vec_max(model, model_size, "你好")
        cosine_similarity(v1, v2)
        self.assertEqual(1, int(cosine_similarity(v1, v2)))
        self.assertEqual(v1, v2)

    def test_doc2vec_aver(self):
        v1 = doc2vec_aver(model, model_size, "你好")
        v2 = doc2vec_aver(model, model_size, "你好")
        cosine_similarity(v1, v2)
        self.assertEqual(1, int(cosine_similarity(v1, v2)))
        self.assertEqual(v1, v2)

    def test_doc2vec_concat(self):
        v1 = doc2vec_concat(model, model_size, "你好")
        v2 = doc2vec_concat(model, model_size, "你好")
        cosine_similarity(v1, v2)
        self.assertEqual(1, int(cosine_similarity(v1, v2)))
        self.assertEqual(v1, v2)

    def test_doc2vec_concat(self):
        v1 = doc2vec_hier(model, model_size, "你好", windows=2)
        v2 = doc2vec_hier(model, model_size, "你好", windows=2)
        self.assertEqual(1,int(cosine_similarity(v1, v2)))
        self.assertEqual(v1, v2)


if __name__ == '__main__':
    unittest.main()
