import logging

defaultLevel = logging.INFO

logging.basicConfig(format = '%(message)s', level = defaultLevel)

logger = logging.getLogger()
"""
Object used for logging.

This object is a standard logger from the Python module ``logging``.

Examples
--------
>>> logger.warning('No configuration properties found. Used default values.')
"""

logger.setLevel(defaultLevel)


def log_internal_error(msg: str) -> None:
    """
    Logs an internal error with an explanatory message followed by a stack trace. 
    
    This function is very useful if you redirect your Lambda function outputs to AWS Cloudwatch, which is recommended. Logs issued by 
    this function appear as ``CRITICAL``. 

    Parameters
    ----------
    msg : str
        Explanatory message. 

    Examples
    --------
    >>> try:
    >>>   raise RuntimeError('WOW!')
    >>> except Exception:
    >>>   log_internal_error("Something wrong happened")
    INTERNAL ERROR: Something wrong happened.
    Traceback (most recent call last):
    File "<stdin>", line 2, in <module>
    RuntimeError: WOW!
    """
    
    import traceback
    logger.critical(f"INTERNAL ERROR: {msg}.")
    logger.critical(traceback.format_exc())
