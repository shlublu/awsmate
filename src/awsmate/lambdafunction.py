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

    Without being abstract, this class has no other public method than :meth:`LambdaEvent.__init__`.
    """
    
    @staticmethod
    def _raiseEventStructureError(msg: str) -> None:
        raise AwsEventSpecificationError(f"Event structure is not as expected: {msg}.")
    

    @staticmethod
    def _raiseCannotReachError(msg: str) -> None:
        LambdaEvent._raiseEventStructureError(f'cannot reach "{msg}"')
    

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
            raise TypeError(f"event_object should be a dict. Here: {str(type(event_object))}.")

        self._event = event_object


    def _records_structure(self) -> dict:
        KEY_RECORDS = "Records"

        try:
            ret = self._event[KEY_RECORDS][0]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))
        
        except IndexError:
            LambdaEvent._raiseEventStructureError(f"'{KEY_RECORDS}' is empty")

        if len(self._event[KEY_RECORDS]) != 1:
            LambdaEvent._raiseEventStructureError(
                f"event contains {str(len(self._event[KEY_RECORDS]))} {KEY_RECORDS} where 1 is expected"
            )
        
        return ret
