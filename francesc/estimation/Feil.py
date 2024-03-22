from biogeme.expressions import Beta, exp, Power, Divide

class Feil:
    def __init__(self, estimate_home, fixed_vars=None):
        self.estimate_home = estimate_home
        self.var_dict = {
            'activity_types' : ['education', 'leisure', 'shopping', 'work'],
            'activity_parameters' : ['Umax', 'Umin', 'alpha', 'beta', 'gamma'],
            'travel_parameters' : ['duration', 'cost'],
            'travel_types' : ['travel']}
        
        if estimate_home:
            self.var_dict['activity_types'].append('home')
        
        # Parameters to be estimated
        B_labels = []
        for v in ['activity']: #travel ignored
            for t in self.var_dict['activity_types']:
                B_labels+=[f'{t}:{p}' for p in self.var_dict[f'{v}_parameters']]
        
        B = {b: Beta(b, 0, None, None, 0) for b in B_labels}
        for b in B_labels:
            if 'Umax' in b: # Umax needs to be positive
                B[b] = Beta(b, 0, 0, None, 0)
            if 'alpha' in b: # alpha needs to be positive
                B[b] = Beta(b, 0, 0, None, 0)
            if 'gamma' in b: # gamma needs to be positive and starts at 1
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
            Vi+= database.variables[f'{at}:participation_{j}'] * (
                self.B[f'{at}:Umin'] + (
                    (self.B[f'{at}:Umax'] - self.B[f'{at}:Umin']) /
                    (1+self.B[f'{at}:gamma'] * 
                     exp(self.B[f'{at}:beta']*(self.B[f'{at}:alpha']-database.variables[f'{at}:duration_{j}']))
                    )**(1/self.B[f'{at}:gamma'])
                )
            )
        return Vi + database.variables[f'prob_corr_{j}']