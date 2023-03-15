import typing
        
from awsmate.lambdafunction import LambdaEvent, AwsEventSpecificationError


class LambdaNotificationEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by AWS S3 Notification.
    """

    KEY_S3 = "s3"
    KEY_RECORDS = "Records"


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
        >>>     from awsmate.s3 import LambdaNotificationEvent
        >>>     event = LambdaNotificationEvent(raw_event)                
        """

        super().__init__(event_object)


    def object_key(self) -> str:
        """
        Returns the key of the S3 object that is the subject of this notification.

        Returns
        -------
        str
            The key of the S3 object.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this key.         

        Examples
        --------
        >>> event.objet_key()
        'path/to/some/object'
        """
        
        try:
            ret = self._event[LambdaNotificationEvent.KEY_RECORDS][0][LambdaNotificationEvent.KEY_S3]["object"]["key"]
    
        except KeyError as err:
            raise AwsEventSpecificationError(f"Event structure is not as expected: cannot reach {str(err)}.")

        except IndexError:
            raise AwsEventSpecificationError(
                f"Event structure is not as expected: no {LambdaNotificationEvent.KEY_RECORDS} object is present in '{LambdaNotificationEvent.KEY_S3}'."
            )

        if len(self._event[LambdaNotificationEvent.KEY_RECORDS]) != 1:
            raise AwsEventSpecificationError(
                f"Event contains {str(len(self._event[LambdaNotificationEvent.KEY_RECORDS]))} {LambdaNotificationEvent.KEY_RECORDS} where 1 is expected."
            )

        return ret 
