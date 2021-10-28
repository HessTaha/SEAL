from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Union

from seal.experiment import Experiment
from seal.run import Run


class Component(object, metaclass=ABCMeta):
    """
    Base Component class
    
    This object ensures that all subclasses Component implements a special 
    `__call__` method.
    """
    @abstractmethod
    def __call__(self) -> None:
        pass


class ExperimentComponent(Component):
    """
    Base Experiment Component class
    
    This object ensures that all subclasses Experiment component implements a
    `_call_on_experiment` method.
    """
    def __call__(self, object: "Experiment") -> None:
        return self._call_on_experiment(object)
    
    @abstractmethod
    def _call_on_experiment(self, object: "Experiment") -> None:
        pass
    
    
class RunComponent(Component):
    """
    Base Run Component class
    
    This object ensures that all subclasses Run component implements a
    `_call_on_run` method.
    """
    def __call__(self, object: "Run") -> None:
        return self._call_on_run(object)
    
    @abstractmethod
    def _call_on_run(self, object: "Run") -> None:
        pass


class HybridComponent(ExperimentComponent, RunComponent):
    """
    Base Hybrid Component class
    
    This object ensures that all subclasses Experiment / Run component \
    implements either a `_call_on_experiment` and `_call_on_run` method.
    """
    def __call__(self, object: Union["Experiment", "Run"]) -> None:
        if isinstance(object, Experiment):
            return self._call_on_experiment(object)
        elif isinstance(object, Run):
            return self._call_on_run(object)


class Logger(Component, metaclass=ABCMeta):
    """
    Logger is an abstract class that defines a common
    interface for a set of Logger-subclasses.
    
    It provides common methods for all possible subclasses, making it 
    possible for a user to create a custom subclass compatible  with 
    the rest of the components. 
    """
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass
    
    def __call__(self, obj: Union["Experiment", "Run"]) -> None:
        if isinstance(obj, Experiment):
            self.log_experiment(obj)
        
        elif isinstance(obj, Run):
            self.log_run(obj)
    
    @abstractmethod
    def log_experiment(self, experiment: 'Experiment') -> None:
        """
        Saves an instance of :class:`~seal.experiment.Experiment`
        """
        pass

    @abstractmethod
    def log_run(self, run: 'Run') -> None:
        """
        Saves all relevant items and artefacts
        generated by an instance of :class:`~seal.run.Run`. \
        This abstract method should call self._log_metrics, 
        self._log_params, self._log_model. 
        """
        pass
    
    @abstractmethod
    def _log_metrics(self, **kwargs) -> None:
        """
        Saves the metrics of an instance of \ 
        :class:`~seal.run.Run` using its attributes.
        Example :
            :attr:`~seal.run.Run.metrics`
        """
        pass

    @abstractmethod
    def _log_params(self, **kwargs) -> None:
        """
        Saves the hyperOpt parameters of an instance of \ 
        :class:`~seal.run.Run` using its attributes and/or 
        methods. 
        Example :
            :meth:`seal.run.Run.model.get_params()`
        """            
        pass
    
    @abstractmethod
    def _log_model(self, **kwargs) -> None:
        """
        Saves the model of an instance of \ 
        :class:`~seal.run.Run` using its attributes.
        Example :
            :attr:`~seal.run.Run.model`
        """            
        pass