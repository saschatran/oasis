from biogeme.expressions import Beta, exp, Power, Divide, log

class MATSIM:
    def __init__(self, estimate_home, fixed_vars=None):
        self.estimate_home = estimate_home

        self.var_dict = {
            'activity_types' : ['education', 'leisure', 'shopping', 'work'],
            'activity_parameters' : ['perf', 'typical_duration'],
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

        for b in B_labels:
            if 'typical_duration' in b: # typical_duration needs to be positive and starts at 1
                B[b] = Beta(b, 1, 0, None, 0)

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
            # assumes expression 10.4 from https://www.matsim.org/files/book/partOne-latest.pdf and prio = 1
            Vi+= database.variables[f'{at}:participation_{j}'] * (
                    self.B[f'{at}:perf'] * self.B[f'{at}:typical_duration'] * 
                        (log(database.variables[f'{at}:duration_{j}'] / self.B[f'{at}:typical_duration']) + 1)
                    + database.variables[f'{at}:early_{j}'] * self.B[f'{at}:early'] #early
                    + database.variables[f'{at}:late_{j}'] * self.B[f'{at}:late'] #late
                    + database.variables[f'{at}:short_{j}'] * self.B[f'{at}:short'] #short
                    # missing wait but it has no data
                    #+ database.variables['travel:duration'] B['travel:duration'] #travel
                )
        return Vi #+ database.variables[f'prob_corr_{j}'] Why not?