import random
import datetime
from google.genai import types
from google import genai
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import os

# Load environment variables from .env file
load_dotenv()


class ImageGeneratorAgent:
    """Agent specialized in generating images based on user prompts with Imagen 3."""

    def __init__(self, api_key: str = None):
        """Initialize the Image Generator Agent."""
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key not found. Please ensure GOOGLE_API_KEY is set in your .env file or environment variables."
            )
        self.client = genai.Client(api_key=self.api_key)

    def generate_unique_filename(self, base_name: str) -> str:
        """Generate a unique filename with timestamp, counter and random numbers."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # Timestamp included in base name
        return f"{base_name}_{timestamp}_{random_nums}"

    def generate_image_from_prompt(self, prompt: str, output_file: str, aspect_ratio: str, number_of_images: int) -> list[str] | None:
        """Generates an image using Imagen 3 based on the provided prompt and saves it."""
        try:
            print(f"\nImagen 3: Generating image...")
            response = self.client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio,
                    safety_filter_level="BLOCK_LOW_AND_ABOVE",
                    person_generation="ALLOW_ADULT"
                )
            )

            if response is None or not response.generated_images or not response.generated_images:
                raise Exception(
                    "Image generation failed or no image data received from Imagen 3.")

            saved_filenames = []  # List to store the filenames of the saved images

            # Sanitize and shorten user prompt for filename base BEFORE the loop
            base_filename_prefix = output_file.replace(
                " ", "_")[:50]  # Use output_file as prefix

            for i, generated_image in enumerate(response.generated_images):
                image_bytes = generated_image.image.image_bytes
                image = Image.open(BytesIO(image_bytes))

                # Ensure output directory exists
                output_dir = os.path.dirname(os.path.abspath(output_file))
                os.makedirs(output_dir, exist_ok=True)

                # Generate unique filename for each image in loop, using timestamp in base
                base_filename = self.generate_unique_filename(
                    base_filename_prefix)  # Unique base filename with timestamp
                file_extension = os.path.splitext(output_file)[1] or ".png"
                script_dir = output_dir  # Save to the output directory

                counter = 0
                image_filename = os.path.join(
                    script_dir, base_filename + file_extension)

                while os.path.exists(image_filename):
                    counter += 1
                    image_filename = os.path.join(
                        script_dir, f"{base_filename}_{counter}{file_extension}")

                image.save(image_filename)
                print(f"Image saved to: {image_filename}")
                # Add filename to the list
                saved_filenames.append(image_filename)

            # Function returns None if no images have been saved
            return saved_filenames if saved_filenames else None  # Return the list of filenames

        except Exception as e:
            error_msg = f"Error generating or saving image: {str(e)}"
            print(error_msg)
            raise


def get_user_prompt_input() -> tuple[str, str, int]:
    """Get the initial image prompt, aspect ratio and number of images from the user."""
    print("\n=== Imagen 3 Image Generator ===")
    print("This tool will generate an image using Imagen 3.")
    print("The image will be saved in the same directory as this script.")

    user_prompt = input("Enter your image prompt: ").strip()
    while not user_prompt:
        user_prompt = input(
            "Prompt cannot be empty. Please enter an image prompt: ").strip()

    print("\nAvailable aspect ratios: 1:1, 3:4, 4:3, 9:16, 16:9")
    aspect_ratio = input(
        "Enter desired aspect ratio (default: 16:9): ").strip() or "16:9"
    while aspect_ratio not in ["1:1", "3:4", "4:3", "9:16", "16:9"]:
        aspect_ratio = input(
            "Invalid aspect ratio. Choose from 1:1, 3:4, 4:3, 9:16, 16:9: ").strip() or "16:9"

    number_of_images_str = input(
        "Enter number of images to generate (1-4, default: 1): ").strip() or "1"
    while not number_of_images_str.isdigit() or not 1 <= int(number_of_images_str) <= 4:
        number_of_images_str = input(
            "Invalid number of images. Enter a number between 1 and 4: ").strip() or "1"
    number_of_images = int(number_of_images_str)

    return user_prompt, aspect_ratio, number_of_images


def main():
    """Main function to run the image generation process."""
    try:
        # Initialize Image Generator Agent
        image_agent = ImageGeneratorAgent()

        # Get user input
        user_prompt, aspect_ratio, number_of_images = get_user_prompt_input()

        # Define output filename (using user prompt as base)
        # Sanitize and shorten user prompt for filename
        safe_user_prompt = user_prompt.replace(" ", "_")[:50]
        # Default png output in script directory
        # Just used for extension and prefix
        output_file = f"{safe_user_prompt}_generated_image.png"

        # Generate and save image using Imagen 3 and the refined prompt
        saved_image_filenames = image_agent.generate_image_from_prompt(
            user_prompt, output_file, aspect_ratio, number_of_images)

        if saved_image_filenames:
            print(
                f"\n=== Image generation process completed. {len(saved_image_filenames)} image(s) saved ===")
        else:
            print(
                "\n=== Image generation process completed, but no images were saved. ===")

    except Exception as e:
        print(f"\n=== Image generation process failed ===")
        print(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main()
