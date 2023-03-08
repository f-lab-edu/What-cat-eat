import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, model, id):
        raise NotImplementedError
