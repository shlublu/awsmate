import json
import typing
        
from awsmate.lambdafunction import LambdaEvent


class LambdaBridgePutEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by AWS EventBridge.

    Warnings
    --------
    AWS EventBridge can be configured in `Universal Target mode <https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html>`_,
    which allows passing the target arbitrary event objects instead of standard ones. :class:`~LambdaBridgePutEvent` is *not* designed to handle such events as they
    do not comply to the AWS EventBridge events specifications. The `PutEvents format <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEventsRequestEntry.html>`_
    is the only handled.
    """

    def __init__(self, event_object: dict):
        """
        Parameters
        ----------
        event_object : ``dict``
            The parameter ``event`` received by the AWS Lambda function handler.

        Raises
        ------
        ``TypeError``
            If ``event_object`` is not a ``dict``.  
                    
        Examples
        --------
        >>> def lambda_handler(raw_event, context):
        >>>     from awsmate.eventbridge import LambdaBridgePutEvent
        >>>     event = LambdaBridgePutEvent(raw_event)                 
        """

        super().__init__(event_object)
    

    def detail_type(self) -> str:
        """
        Returns a readable explanation of the type of this event.

        This explanation is returned as transmitted by AWS EventBridge.

        Returns
        -------
        ``str``
            The detail of the type.

        Raises
        ------
        :exc:`awsmate.lambdafunction.AwsEventSpecificationError`
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
        ``str``
            The name of the source AWS service.

        Raises
        ------
        :exc:`awsmate.lambdafunction.AwsEventSpecificationError`
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


    def detail(self) -> typing.Any:
        """
        Returns the AWS-service-specific details of this event.

        The structure of the returned data varies depending on the service that triggers the event.

        Returns
        -------
        ``any``
            The detail of this event as submitted by the service that triggered it.

        Raises
        ------
        :exc:`awsmate.lambdafunction.AwsEventSpecificationError`
            If the event structure does not allow retrieving this detail, or if cannot be JSON deserialized.      

        Examples
        --------
        >>> event.detail()
        {'EventCategories': ['backup'], 'SourceType': 'DB_INSTANCE', 'SourceArn': 'arn:aws:rds:us-east-1:123456789012:db:rdz0a1b2c3d4e5', 'Date': '2023-04-03T07:20:20.112Z', 'Message': 'Finished DB Instance backup', 'SourceIdentifier': 'rdz0a1b2c3d4e5'}

        """
        
        try:
            ret = json.loads(self._event['detail'])
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        except (TypeError, json.JSONDecodeError) as err:
            LambdaEvent._raiseEventStructureError(f"Detail JSON cannot be decoded: {str(err)}.")            
        
        return ret 