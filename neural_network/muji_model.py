import numpy as np
import chainer
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

class MujiNN(Chain):

    def __init__(self, n_mid_units=100, n_out=11):
        super(MujiNN, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, n_mid_units * 2)
            self.l2 = L.Linear(n_mid_units * 2, n_mid_units)
            self.l3 = L.Linear(n_mid_units, n_out)

    def __call__(self, x):
        h = F.relu(self.l1(x))
        h = F.relu(self.l2(h))
        return self.l3(h)