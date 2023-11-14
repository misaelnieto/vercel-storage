"""
A wrapper around the vercel storage blob api
"""
__version__ = "0.0.1"


class ConfigurationError(ValueError):
    pass


class APIResponseError(ValueError):
    pass
