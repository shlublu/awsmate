import typing
        
from awsmate.lambdafunction import LambdaEvent, AwsEventSpecificationError


class LambdaNotificationEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by AWS S3 Notification.
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
        >>>     from awsmate.s3 import LambdaNotificationEvent
        >>>     event = LambdaNotificationEvent(raw_event)                
        """

        super().__init__(event_object)


    def _records_structure(self) -> dict:
        KEY_RECORDS = "Records"

        try:
            ret = ret = self._event[KEY_RECORDS][0]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))
        
        except IndexError:
            LambdaEvent._raiseEventStructureError(f"'{KEY_RECORDS}' is empty")

        if len(self._event[KEY_RECORDS]) != 1:
            LambdaEvent._raiseEventStructureError(
                f"event contains {str(len(self._event[KEY_RECORDS]))} {KEY_RECORDS} where 1 is expected"
            )
        
        return ret
        
        
    def _s3_structure(self) -> dict:
        try:
            ret = self._records_structure()["s3"]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))
        
        return ret
    

    def _object_structure(self) -> dict:
        try:
            ret = self._s3_structure()["object"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret         
    

    def _bucket_structure(self) -> dict:
        try:
            ret = self._s3_structure()["bucket"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret  
    

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
            ret = self._object_structure()["key"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret 


    def object_size(self) -> typing.Optional[int]:
        """
        Returns the size of the S3 object that is the subject of this notification.

        The size is only defined for object creation events, not for deletions.

        Returns
        -------
        int
            The size of the S3 object in bytes or ``None`` if not defined

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure is invalid.         

        Examples
        --------
        >>> event.objet_size()
        43168
        """
        
        return self._object_structure().get('size', None)


    def object_etag(self) -> typing.Optional[str]:
        """
        Returns the eTag of the S3 object that is the subject of this notification.

        The eTag is only defined for object creation events, not for deletions.

        Returns
        -------
        str
            The eTag of the S3 object or ``None`` if not defined.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure is invalid.         

        Examples
        --------
        >>> event.objet_etag()
        '8b38dac3b5c48c44704ec934eabae5a2'
        """
        
        return self._object_structure().get('eTag', None)


    def bucket_name(self) -> str:
        """
        Returns the name of the S3 bucket that is the subject of this notification.

        Returns
        -------
        str
            The name of the S3 bucket.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this bucket name.         

        Examples
        --------
        >>> event.bucket_name()
        'my-example-s3-bucket'
        """
        
        try:
            ret = self._bucket_structure()["name"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret     


    def bucket_arn(self) -> str:
        """
        Returns the arn of the S3 bucket that is the subject of this notification.

        Returns
        -------
        str
            The arn of the S3 bucket.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this bucket arn.         

        Examples
        --------
        >>> event.bucket_arn()
        'arn:aws:s3:::my-example-s3-bucket'
        """
        
        try:
            ret = self._bucket_structure()["arn"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret  


    def event_name(self) -> str:
        """
        Returns the name of the S3 event that triggered this notification.

        Returns
        -------
        str
            The S3 event name.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this event name.         

        Examples
        --------
        >>> event.event_name()
        'ObjectCreated:Put'
        """
        
        try:
            ret = self._records_structure()["eventName"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret          
