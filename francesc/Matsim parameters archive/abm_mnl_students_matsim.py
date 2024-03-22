import pandas as pd
import numpy as np
import pickle
import joblib

import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, exp, Power, Divide

#Import data

data = joblib.load('data/students_dataset_fixed_biogeme_2609.joblib')

# Read the data
database = db.Database('synthetic', data)


n_alt = 9
n_obs = data['obs_id'].max()

###
# global variables
###

var_dict = {'activity_types' : ['education', 'leisure', 'shopping', 'work'],#, 'home'], #add home here if estimating home parameters
'activity_parameters' : ['Umax', 'Umin', 'alpha', 'beta', 'gamma', 'late', 'early', 'k_weibulls', 'lambda_weibulls', 'gamma_weibull','scale_weibulls'],
'travel_parameters' : ['duration', 'cost'],
'travel_types' : ['travel']}

variables = ['start_time', 'duration', 'participation']


# Parameters to be estimated
B_labels = []
for v in ['activity']: #travel ignored
    for t in var_dict['activity_types']:
        B_labels+=[f'{t}:{p}' for p in var_dict[f'{v}_parameters']]
B = {b: Beta(b, 0, None, None, 0) for b in B_labels}
for b in B_labels:
    if 'Umax' in b:
        B[b] = Beta(b, 0, 0, None, 0)
    if 'alpha' in b:
        B[b] = Beta(b, 0, 0, None, 0)
    if 'weibulls' in b:
        B[b] = Beta(b, 1, 0, None, 0)

B['home:late'] = Beta('home:late', 0, 0, None, 1)
B['home:early'] = Beta('home:early', 0, 0, None, 1)
# Vars = {}
# for at in var_dict['activity_types']:
#     for j in range(0,n_alt):
#         database.DefineVariable(f'{at}:duration_{j}', database.variables[f'{at}:long_{j}']- database.variables[f'{at}:short_{j}'])
#         database.DefineVariable(f'{at}:start_time_{j}', database.variables[f'{at}:late_{j}']- database.variables[f'{at}:early_{j}'])

#Activity specific
def Vi(j):
    Vi=0
    for at in var_dict['activity_types']:
        if at != 'home':
            late = database.variables[f'{at}:late_{j}']
            early = database.variables[f'{at}:early_{j}']
        else:
            late = 0
            early = 0
        #Vi+= database.variables[f'{at}:participation_{j}'] * (
                #B[f'{at}:Umin']
        #        0 + (B[f'{at}:Umax'])
        #        / (1+exp(B[f'{at}:beta']*(B[f'{at}:alpha']-database.variables[f'{at}:duration_{j}'])))
                #+ B[f'{at}:late']*late
                #+ B[f'{at}:early']*early
        #        ) + database.variables[f'prob_corr_{j}']
             #if at!='home':

        Vi+= database.variables[f'{at}:participation_{j}'] * (

                (B[f'{at}:Umax'])/(1+exp(B[f'{at}:beta']*(B[f'{at}:alpha']-database.variables[f'{at}:duration_{j}']))))


                #B[f'{at}:Umin']
                #+ (B[f'{at}:Umax'] - B[f'{at}:Umin'])/(1+exp(B[f'{at}:beta']*(B[f'{at}:alpha']-database.variables[f'{at}:duration_{j}']))))


                # B[f'{at}:Umin']
                # + (
                #     (B[f'{at}:Umax'] - B[f'{at}:Umin'])/
                #     (1+B[f'{at}:gamma']*exp(B[f'{at}:beta']*(B[f'{at}:alpha']-database.variables[f'{at}:duration_{j}'])))**(1/B[f'{at}:gamma'])
                # )
                #+
                #B[f'{at}:scale'] *
                #(B[f'{at}:k_weibulls']/B[f'{at}:lambda_weibulls']) * (
                #    ((database.variables[f'{at}:start_time_{j}']-B[f'{at}:gamma_weibull'])/B[f'{at}:lambda_weibulls'])**(B[f'{at}:k_weibulls']-1)
                #) * (
                #    (exp(-((database.variables[f'{at}:start_time_{j}']+B[f'{at}:gamma_weibull'])/B[f'{at}:lambda_weibulls'])**B[f'{at}:k_weibulls']))
                #)
                #)
    return Vi + database.variables[f'prob_corr_{j}']

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
biogeme.modelName = f'abm_params_mnl_students_feil_umax_pos_0503'

results = biogeme.estimate(algoParameters={'maxiter':20000})
