from awsmate.lambdafunction import LambdaEvent


class LambdaMessageEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by AWS SNS.
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
        >>>     from awsmate.sns import LambdaMessageEvent
        >>>     event = LambdaMessageEvent(raw_event)                
        """

        super().__init__(event_object)

