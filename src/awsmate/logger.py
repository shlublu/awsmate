import logging
import traceback
import typing

defaultLevel = logging.INFO

logging.basicConfig(format = '%(message)s', level = defaultLevel)

logger = logging.getLogger()
"""
logging.Logger : Standard logger from the Python module ``logging``.

Examples
--------
>>> logger.warning('No configuration properties found. Used default values.')
"""

logger.setLevel(defaultLevel)


def log_internal_error(msg: typing.Optional[str] = None) -> None:
    """
    Logs an error explanatory message followed by a stack trace. 
    
    This function is very useful if you redirect your Lambda function outputs to AWS Cloudwatch, which is recommended. Logs issued by 
    this function appear as ``CRITICAL``. 

    Parameters
    ----------
    msg : str
        Optional explanatory message. 

    Examples
    --------
    >>> try:
    >>>   raise RuntimeError('WOW!')
    >>> except Exception:
    >>>   log_internal_error("This one is expected")
    INTERNAL ERROR: This one is expected.
    Traceback (most recent call last):
    File "<stdin>", line 2, in <module>
    RuntimeError: WOW!
    """
    
    logger.critical(f"INTERNAL ERROR: {msg}.")
    logger.critical(traceback.format_exc())
