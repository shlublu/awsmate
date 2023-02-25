class LambdaEvent():
    def __init__(self, eventObject: dict):
        if not isinstance(eventObject, dict):
            raise TypeError(f"eventObject should be a dict. Here: {str(type(eventObject))}.")

        self._event = eventObject

