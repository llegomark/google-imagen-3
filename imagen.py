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
    """Agent specialized in generating images based on user prompts,
    leveraging Gemini to refine prompts for Imagen 3."""

    def __init__(self, api_key: str = None):
        """Initialize the Image Generator Agent."""
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "API key not found. Please ensure GOOGLE_API_KEY is set in your .env file or environment variables."
            )
        self.client = genai.Client(api_key=self.api_key)

    def generate_unique_filename(self, base_name: str) -> str:
        """Generate a unique filename with timestamp and random numbers."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        random_nums = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return f"{base_name}_{timestamp}_{random_nums}"

    def create_imagen_prompt_prompt(self, user_prompt: str, imagen_prompt_guide: str) -> str:
        """Create a detailed prompt for Gemini to generate an improved Imagen 3 prompt."""
        prompt = f"""You are an expert prompt engineer specializing in creating detailed and effective prompts for Imagen 3, Google's advanced text-to-image model. Your goal is to take a user's initial, possibly simple, prompt and enhance it to produce high-quality images using Imagen 3.

Follow these steps to create the improved prompt:

1. **Understand the User's Request:** Analyze the user's initial prompt to grasp the core subject, desired context, and any implied style or mood.

2. **Consult the Imagen Prompt Guide:** Carefully review the provided 'Imagen prompt guide' documentation to understand the best practices for prompting Imagen 3. Pay close attention to sections on:
    - Prompt writing basics (subject, context, and style)
    - Imagen 3 prompt writing advice (descriptive language, context, artist/style references, prompt engineering tools)
    - Enhancing facial details
    - Generating text in images
    - Prompt parameterization
    - Style examples (photography, illustration, art)
    - Advanced prompt writing techniques (photography modifiers, shapes and materials, historical art references, image quality modifiers)
    - Aspect ratios
    - Photorealistic images (guidance for different subjects like portraits, objects, motion, wide-angle)

3. **Refine the Prompt based on the Guide:**  Using the insights from the 'Imagen prompt guide', enhance the user's prompt by adding specific details and modifiers. Consider improving these aspects:
    - **Subject:** Ensure the subject is clearly defined and detailed.
    - **Context and Background:** Elaborate on the scene's background, environment, and setting.
    - **Style:** Specify a visual style (e.g., photography, painting, digital art, sketch). Be as specific as possible (e.g., watercolor painting, hyperrealistic digital art, black and white photography).
    - **Photography Modifiers (if applicable):** Add relevant photography descriptors like camera proximity, position, lighting (natural, dramatic, warm, cold), camera settings (motion blur, bokeh), lens types (35mm, macro, fisheye), film types (black and white, polaroid).
    - **Shapes and Materials (if applicable):** If the prompt involves objects or specific forms, consider specifying materials and shapes.
    - **Historical Art References (if applicable):** If a particular art style is desired, reference historical art periods or movements (e.g., Impressionism, Renaissance, Pop Art, Art Deco).
    - **Image Quality Modifiers:** Include quality-enhancing keywords like 'high-quality', 'beautiful', 'stylized', '4K', 'HDR', 'Studio Photo', 'detailed', 'by a professional'.
    - **Aspect Ratio:** Suggest an appropriate aspect ratio if it's not already implied in the user prompt (consider 1:1, 4:3, 3:4, 16:9, 9:16 based on the subject).
    - **Photorealistic Guidance (if photorealism is desired):** Use lens type, focal length, and detail suggestions from the guide to enhance photorealism based on the subject (portraits, objects, motion, landscape).

4. **Ensure Prompt is Imagen 3 Compatible:** Verify that the refined prompt adheres to Imagen 3's capabilities and limitations, such as the maximum prompt length (480 tokens - though you don't need to count tokens manually, just keep the prompt reasonably concise and detailed).

5. **Output Only the Imagen 3 Prompt:** Your final output should be ONLY the refined Imagen 3 prompt text, ready to be used directly with the Imagen 3 model.  Do not include any extra conversational text, explanations, or apologies. Just the prompt.

**User's Initial Prompt:**
{user_prompt}

**Imagen Prompt Guide Documentation:**
{imagen_prompt_guide}

**Response format:**
[Start of Imagen 3 Prompt]
<refined and detailed Imagen 3 prompt text>
[End of Imagen 3 Prompt]

**Example of expected output format:**

[Start of Imagen 3 Prompt]
A hyperrealistic, 4K HDR studio photograph of a tabby cat wearing sunglasses, lounging lazily on a sun-drenched windowsill. The scene is brightly lit with natural lighting, highlighting the cat's fur details. Use a 35mm lens for a portrait effect.
[End of Imagen 3 Prompt]

Now, generate a detailed and improved Imagen 3 prompt based on the user's initial prompt and the provided Imagen Prompt Guide. Remember to ONLY output the prompt text, enclosed within '[Start of Imagen 3 Prompt]' and '[End of Imagen 3 Prompt]' markers.
"""
        return prompt

    def generate_refined_prompt_from_gemini(self, user_prompt: str, imagen_prompt_guide: str) -> str:
        """Generates a refined Imagen 3 prompt using Gemini based on user input and prompt guide."""
        try:
            prompt_instruction = self.create_imagen_prompt_prompt(
                user_prompt, imagen_prompt_guide)

            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt_instruction,
                config=types.GenerateContentConfig(
                    temperature=1,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=480,
                )
            )

            refined_prompt_text = response.text

            # Extract just the prompt content between markers if markers are present
            start_marker = "[Start of Imagen 3 Prompt]"
            end_marker = "[End of Imagen 3 Prompt]"

            start_index = refined_prompt_text.find(start_marker)
            end_index = refined_prompt_text.find(end_marker)

            if start_index != -1 and end_index != -1:
                refined_prompt_text = refined_prompt_text[start_index + len(
                    start_marker):end_index].strip()
            else:
                print(
                    "Warning: Prompt markers not found in Gemini response. Using the full response as prompt.")

            print("\n=== Refined Imagen 3 Prompt generated by Gemini ===")
            print(refined_prompt_text)
            return refined_prompt_text

        except Exception as e:
            error_msg = f"Error generating refined prompt from Gemini: {str(e)}"
            print(error_msg)
            raise

    def generate_image_from_prompt(self, prompt: str, output_file: str, aspect_ratio: str, number_of_images: int):
        """Generates an image using Imagen 3 based on the provided prompt and saves it."""
        try:
            print(f"\nImagen 3: Generating image with refined prompt...")
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

            if response is None or not response.generated_images or response.generated_images[0].image.image_bytes is None:
                raise Exception(
                    "Image generation failed or no image data received from Imagen 3.")

            for i, generated_image in enumerate(response.generated_images):
                image_bytes = generated_image.image.image_bytes
                image = Image.open(BytesIO(image_bytes))

                # Ensure output directory exists
                output_dir = os.path.dirname(os.path.abspath(output_file))
                os.makedirs(output_dir, exist_ok=True)

                base_filename = os.path.splitext(os.path.basename(output_file))[
                    0]  # Get filename without extension
                # Get extension, default to .png if none
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
                return image_filename  # Return saved filename for potential further use

        except Exception as e:
            error_msg = f"Error generating or saving image: {str(e)}"
            print(error_msg)
            raise


def get_user_prompt_input() -> tuple[str, str, int]:
    """Get the initial image prompt, aspect ratio and number of images from the user."""
    print("\n=== Imagen 3 Prompt Refinement and Image Generator ===")
    print("This tool will refine your prompt using Gemini and generate an image using Imagen 3.")
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


def load_imagen_prompt_guide(filepath="imagen_prompt_guide.md") -> str:
    """Load the Imagen prompt guide from a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(
            f"Warning: {filepath} not found. Using empty prompt guide content.")
        return ""
    except Exception as e:
        print(f"Error loading prompt guide: {e}")
        return ""


def main():
    """Main function to run the image generation process."""
    try:
        # Initialize Image Generator Agent
        image_agent = ImageGeneratorAgent()

        # Get user input
        user_prompt, aspect_ratio, number_of_images = get_user_prompt_input()

        # Load Imagen prompt guide documentation from file
        imagen_prompt_guide_content = load_imagen_prompt_guide(
            "imagen_prompt_guide.md")

        # Generate refined prompt using Gemini
        refined_prompt = image_agent.generate_refined_prompt_from_gemini(
            user_prompt, imagen_prompt_guide_content)

        # Define output filename (using user prompt as base)
        # Sanitize and shorten user prompt for filename
        safe_user_prompt = user_prompt.replace(" ", "_")[:50]
        # Default png output in script directory
        output_file = f"{safe_user_prompt}_generated_image.png"

        # Generate and save image using Imagen 3 and the refined prompt
        image_agent.generate_image_from_prompt(
            refined_prompt, output_file, aspect_ratio, number_of_images)

        print("\n=== Image generation process completed ===")

    except Exception as e:
        print(f"\n=== Image generation process failed ===")
        print(f"Error in main: {str(e)}")


if __name__ == "__main__":
    main()
