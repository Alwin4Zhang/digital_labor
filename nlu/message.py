from typing import Any, Optional, Tuple, Text



def ordered(obj: Any) -> Any:
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    

class Message:
    def __init__(self,text:Text,data=None,time=None) -> None:
        self.text = text
        self.time = time
        self.data = data if data else {}
        
    
    def set(self,prop,info) -> None:
        self.data[prop] = info   
    
    def get(self,prop,default=None) -> Any:
        return self.data.get(prop,default)
    
    def as_dict(self) -> dict:
        d = {key:value for key,value in self.data.items() if value is not None}
        return dict(d,text=self.text)
    
    def __hash__(self) -> int:
        return hash((self.text,str(ordered(self.data))))