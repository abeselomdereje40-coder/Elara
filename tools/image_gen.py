from .image_generation.image_generator import ImageGenerator
from .image_generation.providers.openvino_provider import OpenVINOProvider



class ImageGenTool:
        def __init__(self):
                self.provider=OpenVINOProvider()
                self.generator=ImageGenerator(self.provider)

        def __call__(self,**kwargs):
                prompt=kwargs.get("prompt")
                if not prompt:
                        raise ValueError("An image generation prompt is required")

                result=self.generator.run(prompt)

                return result 
