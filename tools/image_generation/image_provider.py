from abc import ABC,abstractmethod
from .image_models import ImageRequest,ImageResult

class ImageProvider(ABC):
    @abstractmethod
    def generate(self,request:ImageRequest)->ImageResult:
        pass
    