from biogeme.expressions import Beta, exp, Power, Divide

class Linear_OASIS:
    def __init__(self, estimate_home, fixed_vars=None):
        self.estimate_home = estimate_home

        self.var_dict = {
            'activity_types' : ['education', 'leisure', 'shopping', 'work'],
            'activity_parameters' : ['desired_duration', 'desired_start_time', 'constant'],
            'flexibility_parameters' : ['early', 'late', 'long', 'short'],
            'travel_parameters' : ['duration', 'cost'],
            'travel_types' : ['travel']}
        
        if estimate_home:
            self.var_dict['activity_types'].append('home')
        
        # Parameters to be estimated
        B_labels = []
        for v in ['activity', 'flexibility']: #travel ignored
            for t in self.var_dict['activity_types']:
                B_labels+=[f'{t}:{p}' for p in self.var_dict[f'{v}_parameters']]
        
        B = {b: Beta(b, 0, None, None, 0) for b in B_labels}

        if fixed_vars is not None:
            assert isinstance(fixed_vars, dict)
            for b in B_labels:
                if b.split(':')[-1] in fixed_vars:
                    B[b].status = 1
                    B[b].initValue = fixed_vars[b.split(':')[-1]]

        self.B = B
    
    def Vi(self, j, database):
        Vi=0
        for at in self.var_dict['activity_types']:
            Vi+= database.variables[f'{at}:participation_{j}'] * (
                    self.B[f'{at}:constant']
                    + database.variables[f'{at}:early_{j}'] * self.B[f'{at}:early'] #early
                    + database.variables[f'{at}:late_{j}'] * self.B[f'{at}:late'] #late
                    + database.variables[f'{at}:long_{j}'] * self.B[f'{at}:long'] #long
                    + database.variables[f'{at}:short_{j}'] * self.B[f'{at}:short'] #short
                    #+ database.variables['travel:duration'] B['travel:duration'] #travel
                )
        return Vi #+ database.variables[f'prob_corr_{j}'] Why not?