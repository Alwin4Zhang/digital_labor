import os
from typing import Any, Dict, Optional, Text

from nlu.extractors.extractor import EntityExtractor
from nlu.message import Message


class EntitySynonymsMapper(EntityExtractor):
    def __init__(self, 
                 component_config: Optional[Dict[Text, Any]] = None,
                 synonyms: Optional[Dict[Text,Any]] = None
                 ):
        super().__init__(component_config)
        
        self.synonyms = synonyms if synonyms else {}
        
    def process(self, message: Message, **kwargs: Any) -> None:
        updated_entities = message.get("entities",[])[:]
        updated_entities = self.replace_synonyms(updated_entities)
        message.set("entities",updated_entities)
        
    def replace_synonyms(self,entities) -> None:
        new_entities = []
        for entity in entities:
            # need to wrap in `str` to handle e.g. entity values of type int
            entity_value = str(entity['value'])
            if entity_value.lower() in self.synonyms:
                entity['value'] = self.synonyms[entity_value.lower()]
            new_entities.append(entity)
        return new_entities
        
    def add_entities_if_synonyms(self,entity_a,entity_b) -> None:
        if entity_b is not None:
            original = str(entity_a)
            replacement = str(entity_b)
            
            if original != replacement:
                original = original.lower()
                if original in self.synonyms and self.synonyms[original] != replacement:
                    raise f"Found conflicting synonym definitions " 
            
                self.synonyms[original] = replacement