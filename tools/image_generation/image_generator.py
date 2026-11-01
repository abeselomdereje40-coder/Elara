from .image_models import ImageRequest


class ImageGenerator:

    def __init__(self, provider):
        self.provider = provider

    def run(self, prompt: str):
        request = ImageRequest(
            prompt=prompt
        )

        return self.provider.generate(request)