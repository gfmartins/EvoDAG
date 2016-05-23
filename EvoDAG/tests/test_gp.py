# Copyright 2016 Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from test_root import cl, X
from EvoDAG.model import Model
from EvoDAG.node import Variable, Add, Mul, Sin
from EvoDAG.gp import Individual
from nose.tools import assert_almost_equals
import numpy as np


def test_indindividual_decision_function():
    Add.nargs = 2
    Mul.nargs = 2
    vars = Model.convert_features(X)
    for x in vars:
        x._eval_ts = x._eval_tr.copy()
    vars = [Variable(k, weight=1) for k in range(len(vars))]
    for i in range(len(vars)):
        ind = Individual([vars[i]])
        ind.decision_function(X)
        hy = ind._ind[0].hy.tonparray()
        [assert_almost_equals(a, b) for a, b in zip(X[:, i], hy)]
    ind = Individual([Sin(0, weight=1),
                      Add(range(2), np.ones(2)), vars[0], vars[-1]])
    ind.decision_function(X)
    hy = ind._ind[0].hy.tonparray()
    y = np.sin(X[:, 0] + X[:, -1])
    [assert_almost_equals(a, b) for a, b in zip(y, hy)]
    y = np.sin((X[:, 0] + X[:, 1]) * X[:, 0] + X[:, 2])
    ind = Individual([Sin(0, weight=1), Add(range(2), weight=np.ones(2)),
                      Mul(range(2), weight=1),
                      Add(range(2), weight=np.ones(2)),
                      vars[0], vars[1], vars[0], vars[2]])
    ind.decision_function(X)
    # assert v.hy.SSE(v.hy_test) == 0
    hy = ind._ind[0].hy.tonparray()
    [assert_almost_equals(a, b) for a, b in zip(hy, y)]
    
