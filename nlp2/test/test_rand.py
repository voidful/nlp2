import unittest

from nlp2.rand import *


class TestRandom(unittest.TestCase):

    def test_random_string(self):
        self.assertEqual(len(random_string(3)), 3)
        self.addTypeEqualityFunc(str, random_string(3))

    def test_random_string_with_timestamp(self):
        self.assertEqual(len(random_string_with_timestamp(3)), 10 + 3)
        self.addTypeEqualityFunc(str, random_string_with_timestamp(3))

    def test_random_value_in_array_form(self):
        self.assertEqual(random_value_in_array_form([3, 3]), 3)
        self.assertEqual(random_value_in_array_form([3.0, 3.0]), 3)
        self.assertEqual(random_value_in_array_form(['A', 'A']), 'A')

    def test_seed(self):
        print(random.random())
        set_seed(100)
        numA = random.random()
        set_seed(100)
        numB = random.random()
        self.assertEqual(numA, numB)
        try:
            import numpy as np
            print(np.random.random(10))
            set_seed(100)
            seedA = np.random.rand(10)
            print(seedA)
            set_seed(100)
            seedB = np.random.rand(10)
            print(seedB)
            self.assertTrue((seedA == seedB).all())
            import torch
            set_seed(100)
            seqA = torch.rand(2, 3)
            set_seed(100)
            seqB = torch.rand(2, 3)
            self.assertTrue(torch.all(seqA.eq(seqB)).data.item())
            self.assertFalse(torch.all(seqA.gt(seqB)).data.item())
        except:
            pass


if __name__ == '__main__':
    unittest.main()
