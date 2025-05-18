from nlu.registry import get_component_class
from nlu.message import Message

class Interperter:
    def __init__(self,pipeline,context=None) -> None:
        self.pipeline = pipeline
        self.context = context if context is not None else {}
        
    @staticmethod
    def default_output():
        return {
            "tokens":[],
            "intent":None,
            "keywords": [],
            "language_dense_features": None,
            "entities": [],
            "candidates":[],
            "sorted_candidates":[]
        }
        
    def parse(self,input,time=None):
        if not input:
            return 
        output = self.default_output()
        message = Message(
            text=input,
            data=output,
            time=time
        )
        message.set("text",input)
        for component_name in self.pipeline:
            component = get_component_class(component_name)()
            component.process(message)
        output.update(message.as_dict())
        return output