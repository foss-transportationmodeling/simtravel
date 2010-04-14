class SpecificationError(Exception):
    pass

class ChoicesError(SpecificationError):
    pass

class VariablesError(SpecificationError):
    pass

class CoefficientsError(SpecificationError):
    pass

class SeedError(SpecificationError):
    pass

class ThresholdsError(SpecificationError):
    pass

class DataError(Exception):
    pass

class ProbabilityError(Exception):
    pass

class ErrorSpecificationError(Exception):
    pass

class ModelError(Exception):
    pass
