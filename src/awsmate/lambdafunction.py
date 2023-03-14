class AwsEventSpecificationError(RuntimeError):
    """
    Error raised by subclasses of :class:`~LambdaEvent` in case of malformed fields in the AWS event.
    """
    
    def __init__(self, msg: str) -> None:
        """
        Parameters
        ----------
        msg : str
            Explanatory message.
        """
        
        super().__init__(msg)


class LambdaEvent():
    """
    Superclass of input events received by AWS Lambda functions triggered by the various AWS services. 

    Without being abstract, this class has no other method than :func:`LambdaEvent.__init__`.
    """
    
    def __init__(self, event_object: dict) -> None:
        """
        Parameters
        ----------
        event_object : dict
            The parameter ``event`` received by the AWS Lambda function handler.

        Raises
        ------
        TypeError
            If ``event_object`` is not a ``dict``.      

        Examples
        --------
        >>> def lambda_handler(raw_event, context):
        >>>     from awsmate.lambdafunction import LambdaEvent
        >>>     event = LambdaEvent(raw_event)                
        """
        
        if not isinstance(event_object, dict):
            raise TypeError(f"eventObject should be a dict. Here: {str(type(event_object))}.")

        self._event = event_object

