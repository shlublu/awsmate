import typing
        
from awsmate.errors import AwsEventSpecificationError
from awsmate.lambdafunction import LambdaEvent


class LambdaNotificationEvent(LambdaEvent):
    KEY_S3 = "s3"
    KEY_RECORDS = "Records"


    def __init__(self, eventObject: dict):
        super().__init__(eventObject)


    def objet_key(self) -> str:
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
