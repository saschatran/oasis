import argparse
import pandas as pd
import numpy as np
import pickle
import joblib
from datetime import datetime

import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, exp, Power, Divide

from Feil import Feil
from Linear_OASIS import Linear_OASIS
from MATSIM import MATSIM

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('utility_function', type=str)
    parser.add_argument('data_path', type=str)
    parser.add_argument('--model_name', type=str)
    parser.add_argument('--estimate_home', action='store_true')
    parser.add_argument('--fixed_vars', nargs='+', type=str)
    args = parser.parse_args()

    # convert fixed_vars to dict
    if args.fixed_vars is not None:
        assert len(args.fixed_vars)%2 == 0
        fixed_vars = {args.fixed_vars[i]: float(args.fixed_vars[i+1]) for i in range(0, len(args.fixed_vars), 2)}
    else:
        fixed_vars = None

    data = joblib.load(args.data_path)
    database = db.Database('synthetic', data)

    n_alt = 9
    n_obs = data['obs_id'].max()
    
    ###
    model_name = args.model_name
    if args.utility_function == "Feil":
        uf = Feil(args.estimate_home, fixed_vars)
        model_name = 'Feil' if model_name is None else model_name
    elif args.utility_function == "Linear_OASIS":
        uf = Linear_OASIS(args.estimate_home, fixed_vars)
        model_name = 'Linear_OASIS' if model_name is None else model_name
    elif args.utility_function == "MATSIM":
        uf = MATSIM(args.estimate_home, fixed_vars)
        model_name = 'MATSIM' if model_name is None else model_name
    else:
        raise ValueError(f"Unknown utility function {args.utility_function}")
    
    V = {j: uf.Vi(j, database) for j in range(0,n_alt)}
    av = {j: 1 for j in range(0,n_alt)}

    logprob = models.loglogit(V, av, database.variables['choice'])
    biogeme = bio.BIOGEME(database, logprob)
    # add timestamp to model name
    biogeme.modelName = f"{model_name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    results = biogeme.estimate(algoParameters={'maxiter':20000})


if __name__ == '__main__':
    main()