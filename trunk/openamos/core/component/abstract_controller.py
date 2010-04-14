from openamos.core.data_array import DataArray


class BasicController(object):
    def __init__(self, model_list, data):
        for i in model_list:
            if not isinstance(i, SubModel):
                raise ModelError, """all object(s) in the model_list """\
                    """must be valid SubModel objects"""

        self.model_list = model_list
    #TODO: check for validity of dat aand choiceset TYPES
        self.data = data


    #TODO: check for varnames in model specs and in the data

    def create_choiceset(self, shape, criterion, names):
        #TODO: Should setup a system to generate the choicesets dynamically
        #based on certain criterion

        #this choiceset creation criterion must be an attribute of the SubModel class
        from numpy import ones
        choiceset = ones(shape)
        return DataArray(choiceset, names)


    def filter_data(self, data_filter):
        return data_filter.compare(self.data)
            

    def run_component(self):
        for i in model_list:
            # Retrieving a subset of all agents (e.g., children, adults etc)
            # on which the particular model will be applied
            data_subset = filter_data(i.data_filter)

            # this subsection of the method is run when a particular
            # model has to be run until a condition is violated
            if run_until_condition is not None:

                agents_to_simulate_ind = True

                while (agents_to_simulate_ind):
                    # Retrieving the records of those agents where a certain
                    # stopping criterion is not satisfied
                    agents_to_simulate = run_until_condition.compare(data_subset)
                
                    # Generate a choiceset for the corresponding agents
                    choiceset_shape = (agents_to_simulate.shape[0], 
                                       i.model.specification.number_choices)
                    choicenames = i.model.specification.choices
                    choiceset = self.create_choiceset(choiceset_shape, i.choiceset_criterion, 
                                                      choicenames)
            
                    # simulate the choice
                    result = i.simulate_choice(agents_to_simulate, choiceset)

                    # update the indicator for agents to simulate
                    data_subset.setcolumn(dep_varname, result)
                    result_run_var = data_subset.calculate_equation(data_filter.coefficients)
                    data_subset.setcolumn(i.run_until_condition.varname, result_run_var)

                    agents_to_simulate = run_until_condition.compare(data_subset)
                    if agents_to_simulate.shape[0] <> 0:
                        agents_to_simulate = True
                    else:
                        agents_to_simulate = False

        else:
            agents_to_simulate = data_subset
            result = i.simulate_choice(agents_to_simulate, choiceset)
        
        # SOMEWHERE THE DATA HAS TO BE STORED FOR THE VALUES THAT
        # ARE BEING SIMULATED IN BOTH CASES WHERE MODELS RUN IN A LOOP
        # AND IN THE ALTERNATIVE CASE WHERE THEY RUN ONLY ONCE
        # I.E. EITHER UPDATE SELF.DATA OBJECT; WRITE TO AGENT OBJECTS;
        # WRITE TO DATABASE



    
    
