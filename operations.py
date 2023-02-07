from abc import ABC, abstractclassmethod
import pandas
import typing
from utility import *

class Operation(ABC):
    '''Abstract class defining the basic characteristics of any operation: name and status. Both are turned into
    properties, the name should be set by default by the developer, and the status is set to False to be readily
    turned to True by the decorator switch. The abstract operation is the actual operation to be executed on
    datasets, which means any operation defined as subclass of Operation will have its own operation method.'''
    @switch
    def __init__(self, status: bool = False, name: str = None):
        self.__status: bool = status
        self.__name: str = name
    
    @property
    def status(self) -> bool:
        '''getter for the status of an operation object'''
        return self.__status
    
    @property
    def name(self) -> str:
        '''getter for the name of an operation object'''
        return self.__name
    
    @abstractclassmethod
    def operation(self, d):
        pass

class OperationRegistry:
    '''Registry class, takes as starred arguments any operation the user sees fit for their work. Contains two 
    attributes, both made properties: registry {operation name:operation object} and status_registry{operation name:status}.
    Always queried by a Dataset before allowing any operation to be executed.'''
    def __init__(self, *ops: Operation):
        self.__registry: dict = {i.name:i for i in ops}
        self.__status_registry: dict = {i.name:i.status for i in ops}
    
    @property
    def registry(self) -> dict:
        '''getter for the operation registry'''
        return self.__registry
    
    @property
    def status_registry(self) -> dict:
        '''getter for the operation status registry'''
        return self.__status_registry



