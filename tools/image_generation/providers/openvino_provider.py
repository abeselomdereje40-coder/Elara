from pathlib import Path

from huggingface_hub import snapshot_download
from optimum.intel.openvino import OVDiffusionPipeline

from ..image_provider import ImageProvider
from ..image_models import ImageRequest, ImageResult


class OpenVINOProvider(ImageProvider):

    def __init__(self):
        self.model_path = None
        self.pipeline = None

        self.output_dir = Path("generate_image")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_model(self):
        if self.pipeline is not None:
            return

        print("Loading local OpenVINO Stable Diffusion model...")

        # Find the model already downloaded to the Hugging Face cache.
        self.model_path = Path(
            snapshot_download(
                "OpenVINO/stable-diffusion-v1-5-int8-ov",
                local_files_only=True
            )
        )

        # Verify that the four required model components exist.
        components = [
            "text_encoder",
            "unet",
            "vae_decoder",
            "vae_encoder"
        ]

        for component in components:
            xml_file = self.model_path / component / "openvino_model.xml"
            bin_file = self.model_path / component / "openvino_model.bin"

            if not xml_file.is_file() or not bin_file.is_file():
                raise FileNotFoundError(
                    f"Missing OpenVINO model files for {component}"
                )

        print(f"Model directory: {self.model_path}")

        # Load the local model without compiling it immediately.
        self.pipeline = OVDiffusionPipeline.from_pretrained(
            str(self.model_path),
            compile=False
        )

        # Compile the model for inference.
        self.pipeline.compile()

        print("OpenVINO model loaded successfully.")

    def generate(self, request: ImageRequest) -> ImageResult:
        try:
            # Load the model only on the first request.
            self._load_model()

            print(f"Generating image: {request.prompt}")
            print(
                f"Image dimensions: "
                f"{request.width}x{request.height}"
            )

            # Prepare the generation arguments.
            arguments = {
                "prompt": request.prompt,
                "height": request.height,
                "width": request.width,
                "num_inference_steps": 20
            }

            if request.negative_prompt:
                arguments["negative_prompt"] = request.negative_prompt

            if request.seed is not None:
                import torch

                arguments["generator"] = (
                    torch.Generator(device="cpu")
                    .manual_seed(request.seed)
                )

            # Generate the image.
            result = self.pipeline(**arguments)

            image = result.images[0]

            # Save the generated image.
            output_path = self.output_dir / "elara_generated.png"

            image.save(output_path)

            print(f"Image saved to: {output_path.resolve()}")

            return ImageResult(
                success=True,
                image_path=str(output_path.resolve())
            )

        except Exception as e:
            print(f"OpenVINO image generation failed: {e}")

            return ImageResult(
                success=False,
                error=str(e)
            )