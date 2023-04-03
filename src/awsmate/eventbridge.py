import typing
        
from awsmate.lambdafunction import LambdaEvent, AwsEventSpecificationError


class LambdaBridgeEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by AWS EventBridge.
    """

    def __init__(self, event_object: dict):
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
        >>>     from awsmate.eventbridge import LambdaBridgeEvent
        >>>     event = LambdaBridgeEvent(raw_event)                
        """

        super().__init__(event_object)
    

    def detail_type(self) -> str:
        """
        Returns a readable explanation of the type of this event.

        This explanation is returned as transmitted by AWS EventBridge.

        Returns
        -------
        str
            The detail of the type.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this piece of information.         

        Examples
        --------
        >>> event.detail_type()
        'RDS DB Instance Event'
        """
        
        try:
            ret = self._event['detail-type']
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   


    def source(self) -> str:
        """
        Returns the name of the AWS service that triggered this event.

        This name is returned as transmitted by AWS EventBridge.

        Returns
        -------
        str
            The name of the source AWS service.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this service.         

        Examples
        --------
        >>> event.source()
        'aws.rds'
        """
        
        try:
            ret = self._event['source']
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   


    def detail(self) -> dict:
        """
        Returns the AWS-service-specific details of this event.

        The structure of the returned ``dict`` varies depending on the service that triggers the event. It may be empty but it is expected to be present.

        Returns
        -------
        dict
            The detail of this event.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this detail, or if it is not a ``dict``.      

        Examples
        --------
        >>> event.detail()
        {'EventCategories': ['backup'], 'SourceType': 'DB_INSTANCE', 'SourceArn': 'arn:aws:rds:us-east-1:123456789012:db:rdz0a1b2c3d4e5', 'Date': '2023-04-03T07:20:20.112Z', 'Message': 'Finished DB Instance backup', 'SourceIdentifier': 'rdz0a1b2c3d4e5'}

        """
        
        try:
            ret = self._event['detail']
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        if not isinstance(ret, dict):
            LambdaEvent._raiseEventStructureError(f"Detail should be a dict, not a {type(ret)}.") 
        
        return ret 