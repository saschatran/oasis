import pandas as pd
import numpy as np
import pickle
import joblib
from math import ceil

import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, bioMax

#Import data

df_long = joblib.load(open('/PATH/TO/LONG/DATA', 'rb'))
df_wide = joblib.load(open('/PATH/TO/WIDE/DATA', 'rb'))

#train set

n_alt = df_long['alt_id'].max()
n_obs = df_long['obs_id'].nunique()


# Read the data
database = db.Database('synthetic', df_wide)

###
# global variables
###

var_dict = {'activity_types' : ['education', 'leisure', 'shopping', 'work'], #add home here if estimating home parameters
'activity_parameters' : ['desired_duration', 'desired_start_time', 'constant'],
'flexibility_types' : ['F', 'NF'], #flexible, #non flexible
'flexibility_parameters' : ['early', 'late', 'long', 'short'],
'travel_parameters' : ['duration', 'cost'],
'travel_types' : ['travel']}

variables = ['start_time', 'duration', 'participation']

flexibility_lookup = {'education': 'NF',
 'work': 'NF',
 'leisure': 'F',
 'shopping': 'F',
 'home': 'F'}


# Parameters to be estimated
B_labels = []
for v in ['activity', 'flexibility']: #travel ignored
    for t in var_dict[f'activity_types']:
        B_labels+=[f'{t}:{p}' for p in var_dict[f'{v}_parameters']]
B = {b: Beta(b, 0, None, None, 0) for b in B_labels}


#Activity specific
def Vi(j):
    Vi=0
    for at in var_dict['activity_types']:
        fd = flexibility_lookup[at]
        Vi+= database.variables[f'{at}:participation_{j}'] * (
                B[f'{at}:constant']
                + database.variables[f'{at}:early_{j}'] * B[f'{at}:early'] #early
                + database.variables[f'{at}:late_{j}'] * B[f'{at}:late'] #late
                + database.variables[f'{at}:long_{j}'] * B[f'{at}:long'] #long
                + database.variables[f'{at}:short_{j}'] * B[f'{at}:short'] #short
                #+ database.variables['travel:duration'] B['travel:duration'] #travel
            )
    return Vi #+ database.variables[f'prob_corr_{j}']

#Generic parameters (Flexible/Non Flexible)

"""
def Vi(j):
    Vi=0
    for at in var_dict['activity_types']:
        fd = flexibility_lookup[at]
        Vi+= database.variables[f'{at}:participation_{j}'] * (
                B[f'{at}:constant']
                + database.variables[f'{fd}:early_{j}'] * B[f'{fd}:early'] #early
                + database.variables[f'{fd}:late_{j}'] * B[f'{fd}:late'] #late
                + database.variables[f'{fd}:long_{j}'] * B[f'{fd}:long'] #long
                + database.variables[f'{fd}:short_{j}'] * B[f'{fd}:short'] #short
                #+ database.variables['travel:duration'] B['travel:duration'] #travel
            ) + database.variables[f'prob_corr_{j}']
    return Vi
"""


V = {j: Vi(j) for j in range(0,n_alt)}
av = {j:1 for j in range(0,n_alt)}


logprob = models.loglogit(V, av, database.variables['choice'])
biogeme = bio.BIOGEME(database, logprob)
biogeme.modelName = 'abm_params_mnl'

results = biogeme.estimate()
