from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError("Method parse should be implemented!")
