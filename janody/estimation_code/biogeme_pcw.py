
import pandas as pd
import numpy as np
import joblib

import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta, exp, Power, Divide, bioMax, log


#Import data
df_long = joblib.load('1801_random_format_long_biogeme.joblib')
df_wide = joblib.load('1801_random_format_wide_biogeme.joblib')


# Read the data
database = db.Database('synthetic', df_wide)


n_alt = df_long['alt_id'].max()
n_obs = df_long['obs_id'].nunique()

#Global variables

#DEFAULT MATSIM TYPICAL DURATIONS
#typical_dur = {'home': 12,
#'work': 8,
#'education': 6,
#'leisure': 2,
#'shopping': 2}

#TYPICAL DURATIONS COMPUTED FROM PCW DATA (average)
avg_dur = {#'business': 3.1395529640427595,
 #'errands': 1.045308924485126,
 #'escort': 0.696585804132974,
 'home': 6.093768640142141,
 'leisure': 2.774682337992376,
 'other': 2.903186274509804,
 'shopping': 0.7106734006734006,
 #'shopping_longterm': 0.9532356532356533,
 'work_edu': 5.813528037383178}

#AVG START TIME FROM PCW DATA (average)
avg_start = {#'business': 12.049999999999999,
  #'errands': 12.75839054157132,
  #'escort': 14.245238095238095,
  'home': 10.104007233961546,
  'leisure': 14.73664760694621,
  'other': 14.245588235294118,
  'shopping': 13.632895622895624,
  #'shopping_longterm': 14.157936507936508,
  'work_edu': 9.807943925233644}


var_dict = {'activity_types' : ['work_edu', 'shopping', 'leisure'], #add home here if estimating home parameters
'activity_parameters' : ['late', 'early', 'short'],
'travel_parameters' : ['travel_time'],
'travel_types' : ['car', 'walk', 'bicyle', 'pt']}

variables = ['start_time', 'duration', 'participation']
variables_modes = ['travel_time']

priority = {
'home': 1,
'work_edu': 1,
'leisure': 3,
'shopping': 3
}


# Parameters to be estimated
B_labels = []
for v in ['activity', 'travel']:
    for t in var_dict[f'{v}_types']:
        B_labels+=[f'{t}:{p}' for p in var_dict[f'{v}_parameters']]
B = {b: Beta(b, 0, None, None, 0) for b in B_labels}

B['act'] = Beta('act', 0, None, None, 0)
B['scale'] = Beta('scale', 200, None, None, 1)
B['walk:travel_time'] = Beta('walk:travel_time', 0, None, None, 1)


#Activity specific
def Vi(j):
    Vi=0
    for at in var_dict['activity_types']:

        late = database.variables[f'{at}:late_{j}']
        early = database.variables[f'{at}:early_{j}']
        short = database.variables[f'{at}:short_{j}']
        duration = database.variables[f'{at}:duration_{j}']
        t_0 = avg_dur[at]*exp(-B['scale']/(priority[at]*avg_dur[at]))

        Vi+= database.variables[f'{at}:participation_{j}'] * (

                B[f'{at}:late']*late +
                B[f'{at}:early']*early +
                B[f'{at}:short']*short +
                bioMax(0, B['act']*avg_dur[at]*log(duration / t_0))

                )

    for m in var_dict['travel_types']:
        Vi+= B[f'{m}:travel_time']*database.variables[f'{m}:travel_time_{j}']


    return Vi


V = {j: Vi(j) for j in range(1,n_alt+1)}
av = {j:1 for j in range(1,n_alt+1)}


logprob = models.loglogit(V, av, database.variables['choice'])
biogeme = bio.BIOGEME(database, logprob)
biogeme.modelName = f'abm_mnl_pcw_random'

results = biogeme.estimate()
