# This code calls Stability AI's image upscaling API

import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Stability Host URL
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'


# Stability API Key
# If you don't have an API key, you can get one by signing up here https://dreamstudio.ai/
os.environ['STABILITY_KEY'] = 'sk-KwVrEeP4r2XYb1vG44yaGGysriFRgJweiLLWCaWNV47rvzx9'

# Set up the connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    upscale_engine="esrgan-v1-x2plus", # The name of the upscaling model we want to use.
    verbose=True, # Print debug messages.
)

# Import the image to upscale
# Images are limited to 1048576 pixels in total (for example 1024 x 1024)
img = Image.open('test.png')

# Pass the image to the API and call the upscaling process.
answers = stability_api.upscale(
    init_image=img,

    # By default, the image will be upscaled to twice its dimensions
    # An additional "width" or "height" parameter (but not both) can be passed to the upscale function
    width=1024
)

# Set up our warning to print to the console if the adult content classifier is tripped.
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please submit a different image and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            big_img = Image.open(io.BytesIO(artifact.binary))
            # Save the image to a local file
            big_img.save("imageupscaled" + ".png")