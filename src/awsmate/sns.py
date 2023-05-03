import base64
import typing

from binascii import Error as Base64Error
from copy import deepcopy

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


    def _sns_structure(self) -> dict:
        try:
            ret = self._records_structure()["Sns"]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))
        
        return ret
    

    def event_subscription_arn(self) -> str:
        """
        Returns the arn of the subscription that led this message to be sent.

        Returns
        -------
        str
            The arn of the SNS subscription.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this subscription arn.         

        Examples
        --------
        >>> event.event_subscription_arn()
        'arn:aws:sns:eu-west-1:123456789012:sns-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6'
        """
        
        try:
            ret = self._records_structure()["EventSubscriptionArn"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret  


    def unsubscribe_url(self) -> str:
        """
        Returns the unsubscription URL of the subscription that led this message to be sent.

        Returns
        -------
        str
            The unsubscription URL.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this URL.         

        Examples
        --------
        >>> event.unsubscribe_url()
        'https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:eu-west-1:123456789012:your-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6'
        """
        
        try:
            ret = self._sns_structure()["UnsubscribeUrl"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   
    

    def topic_arn(self) -> str:
        """
        Returns the arn of the topic this message belongs to.

        Returns
        -------
        str
            The arn of the SNS topic.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this topic arn.         

        Examples
        --------
        >>> event.topic_arn()
        'arn:aws:sns:eu-west-1:123456789012:sns-lambda'
        """
        
        try:
            ret = self._sns_structure()["TopicArn"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret  
        
        
    def signature(self) -> str:
        """
        Returns the signature of the message.

        Returns
        -------
        str
            The signature of the message.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this signature.         

        Examples
        --------
        >>> event.signature()
        'On1AdgZdIdWOHBltcSQCLuy+mE/Nozp9QHYGXSHVjhwZbXEkAi7svphPzaM='
        """
        
        try:
            ret = self._sns_structure()["Signature"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret     
    

    def signing_cert_url(self) -> str:
        """
        Returns the URL of the certificate that allows checking the signature of this message.

        Returns
        -------
        str
            The signature of the message.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this URL.         

        Examples
        --------
        >>> event.signing_cert_url()
        'https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-aa11bb22cc33dd44ee55ff66ee55dd44.pem'

        See Also
        --------
        :meth:`signature`
        """
        
        try:
            ret = self._sns_structure()["SigningCertUrl"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   
    

    def message_id(self) -> str:
        """
        Returns the unique identifier of the message.

        Returns
        -------
        str
            The id of the message.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this identifier.         

        Examples
        --------
        >>> event.message_id()
        'a1b2c3d4-e5f6-aa11-bb22-f6e5d4c3b2a4'
        """
        
        try:
            ret = self._sns_structure()["MessageId"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   
    

    def subject(self) -> typing.Optional[str]:
        """
        Returns the subject of the message if any.

        Returns
        -------
        str
            The subject of the message or ``None`` if omitted.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this subject.         

        Examples
        --------
        >>> event.message_subject()
        'Some subject'
        """
        
        try:
            ret = self._sns_structure()["Subject"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   
        
        
    def message(self) -> str:
        """
        Returns the content of the message.

        Returns
        -------
        str
            The content of the message.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this content.         

        Examples
        --------
        >>> event.message()
        'some text'
        """
        
        try:
            ret = self._sns_structure()["Message"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret   


    def message_type(self) -> str:
        """
        Returns the type of the message.

        This type is returned as transmitted by AWS SNS. No verification is performed.

        Returns
        -------
        str
            The type of the message.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving this type.         

        Examples
        --------
        >>> event.message_type()
        'Notification'
        """
        
        try:
            ret = self._sns_structure()["Type"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return ret       
    

    def message_attributes(self) -> dict:
        """
        Returns the attributes of the message, if any.

        Attributes must comply to `the AWS SNS attributes specifications <https://docs.aws.amazon.com/sns/latest/dg/sns-message-attributes.html>`_. Binary values
        are decoded from base-64 to binary strings.

        Returns
        -------
        dict
            The attributes of the message, which is empty if no attribute is specified.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If the event structure does not allow retrieving such attributes or if their do not comply to AWS SNS attributes specifications.         

        Examples
        --------
        >>> event.message_attributes()
        {'AttributeName': {'Type': 'String', 'Value': 'Some text'}, 'OtherAttributeName': {'Type': 'Binary', 'Value': b'Some decoded binary'}}
        """
        
        try:
            ret = self._sns_structure()["MessageAttributes"]
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        if ret is None:
            ret = {}

        if not isinstance(ret, dict):
            LambdaEvent._raiseEventStructureError(f'MessageAttributes is not expected to be a {str(type(ret))}')

        for k in ret.keys():
            if not isinstance(k, str):
                LambdaEvent._raiseEventStructureError(f'MessageAttributes has a key of type {str(type(k))}: {str(k)}')

            if not isinstance(ret[k], dict):
                LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] is not expected to be a {str(type(ret[k]))}')

            if 'Type' not in ret[k].keys():
                LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] does not have a Type key')

            if 'Value' not in ret[k].keys():
                LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] does not have a Value key')

            for sk in ret[k].keys():
                if sk not in ['Type', 'Value']:
                    LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] has a key that is neither Type nor Value')

            if ret[k]['Type'] not in ['String', 'Binary']:
                LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] has a Type that is neither String nor Binary')

            if not isinstance(ret[k]['Value'], str):
                LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] has a raw value of unexpected type {str(type(ret[k]["Value"]))}')

            if ret[k]['Type'] == 'Binary': 
                try:
                    ret = deepcopy(ret)
                    ret[k]["Value"] = base64.b64decode(ret[k]["Value"])

                except Base64Error as err:
                    LambdaEvent._raiseEventStructureError(f'MessageAttributes[{k}] has a raw value that is not encoded in base-64')

        return ret    

