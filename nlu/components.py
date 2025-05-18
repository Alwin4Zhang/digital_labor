# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2023/11/16 21:28:55
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''
import logging
import typing
from typing import Any, Dict, Hashable, List, Optional, Set, Text, Tuple, Type, Iterable
from nlu.message import Message


class ComponentMetaclass(type):
    """Metaclass with `name` class property."""

    @property
    def name(cls):
        """The name property is a function of the class - its __name__."""

        return cls.__name__
    
class Component(metaclass=ComponentMetaclass):
    """A component is a message processing unit in a pipeline.

    Components are collected sequentially in a pipeline. Each component
    is called one after another. This holds for
    initialization, training, persisting and loading the components.
    If a component comes first in a pipeline, its
    methods will be called first.

    E.g. to process an incoming message, the ``process`` method of
    each component will be called. During the processing
    (as well as the training, persisting and initialization)
    components can pass information to other components.
    The information is passed to other components by providing
    attributes to the so called pipeline context. The
    pipeline context contains all the information of the previous
    components a component can use to do its own
    processing. For example, a featurizer component can provide
    features that are used by another component down
    the pipeline to do intent classification.
    """
    
    @property
    def name(self):
        """Access the class's property name from an instance."""
        return type(self).name
    
    @classmethod
    def required_components(cls) -> List[Type["Component"]]:
        """Specify which components need to be present in the pipeline.

        Returns:
            The list of class names of required components.
        """

        return []

    defaults = {}
    
    
    def __init__(self,component_config:Optional[Dict[Text, Any]] = None) -> None:
        if not component_config:
            component_config = {}
            
        component_config['name'] = self.name
        self.component_config = component_config
    
    @classmethod
    def required_packages(cls) -> List[Text]:
        """Specify which python packages need to be installed.

        E.g. ``["spacy"]``. More specifically, these should be
        importable python package names e.g. `sklearn` and not package
        names in the dependencies sense e.g. `scikit-learn`

        This list of requirements allows us to fail early during training
        if a required package is not installed.

        Returns:
            The list of required package names.
        """
        return []
    
    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ):
        """Load this component from file.

        After a component has been trained, it will be persisted by
        calling `persist`. When the pipeline gets loaded again,
        this component needs to be able to restore itself.
        Components can rely on any context attributes that are
        created by :meth:`components.Component.create`
        calls to components previous to this one.

        Args:
            meta: Any configuration parameter related to the model.
            model_dir: The directory to load the component from.
            # model_metadata: The model's :class:`rasa.nlu.model.Metadata`.
            cached_component: The cached component.

        Returns:
            the loaded component
        """
        if cached_component:
            return cached_component
        return cls(meta)
    
    def process(self,message:Message,**kwargs:Any) -> None:
        """Process an incoming message.

        This is the components chance to process an incoming
        message. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`rasa.nlu.components.Component.create`
        of ANY component and
        on any context attributes created by a call to
        :meth:`rasa.nlu.components.Component.process`
        of components previous to this one.

        Args:
            message: The :class:`rasa.nlu.training_data.message.Message` to process.

        """

        pass