# google-imagen-3: AI Image Generator with Imagen 3 and Gemini Prompt Refinement

[![Google Imagen 3](/images/a_person_setting_on_the_beach_watching_meteors_pix_generated_image.png)](https://github.com/llegomark/google-imagen-3)
[![Google Imagen 3](/images/mayon_volcano_pixel_art_generated_image.png_20250213_034953_310585.png)](https://github.com/llegomark/google-imagen-3)

This repository provides a Python script, `imagen_with_refinement.py`, for generating high-quality images using Google's cutting-edge **Imagen 3** model.  Leveraging the latest **Google Gen AI Python SDK (`google-genai`)** and **Gemini**, this tool enhances your image prompts before sending them to Imagen 3, resulting in more detailed and visually compelling creations.

**Imagen 3 - Google's Premier Text-to-Image Model:**

*   **Unmatched Detail**: Generate images with exceptional detail, nuanced lighting, and minimal artifacts.
*   **Superior Natural Language Understanding**:  Accurately interprets and responds to complex, natural language prompts.
*   **Versatile Styles**: Create images across a vast spectrum of formats and artistic styles, from photorealistic to stylized art.
*   **Advanced Text Rendering**:  Effectively incorporates text within images (while this script primarily focuses on visual generation).

The `imagen_with_refinement.py` script takes your text prompt and utilizes **Gemini** to refine it based on the [Imagen Prompt Guide](https://ai.google.dev/gemini-api/docs/imagen-prompt-guide). This enhanced prompt is then used by **Imagen 3 (`imagen-3.0-generate-002`)** to generate the final image, which is saved locally.

**For a simplified version without prompt refinement, please see `imagen_no_refinement.py`.**

## Features

*   **Imagen 3 Powered**: Employs Google's state-of-the-art Imagen 3 model (`imagen-3.0-generate-002`) for superior image generation.
*   **Google Gen AI SDK**: Built using the latest `google-genai` Python SDK for optimal performance and access to the newest features.
*   **Gemini Prompt Refinement**: Integrates Gemini (`gemini-2.0-flash-thinking-exp-01-21`) to intelligently enhance user prompts based on the official "Imagen Prompt Guide", leading to improved image quality and prompt adherence.
*   **Customizable Aspect Ratio**: Allows users to select from various aspect ratios (1:1, 3:4, 4:3, 9:16, 16:9) for generated images, with a default widescreen 16:9 setting.
*   **Adjustable Image Count**: Enables users to generate multiple images (1-4) per prompt.
*   **Robust Safety Filters**: Implements `BLOCK_LOW_AND_ABOVE` safety filtering to ensure responsible and safe image generation.
*   **Local Storage with Unique Filenames**: Saves generated images as PNG files in the script's directory, using unique, timestamped filenames to prevent accidental overwriting.
*   **Command-Line Interface**: Provides a straightforward command-line interface for easy prompt input and image generation.

## Getting Started

### Prerequisites

*   **Python 3.12+** (Recommended)
*   **pip** (Python Package Installer)
*   **Google Generative AI API Key**: Obtain an API key from [Google AI for Developers](https://aistudio.google.com/app/u/0/apikey) to access Google's Generative AI services.
*   **Python Libraries**: Install the required libraries listed in `requirements.txt`.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/llegomark/google-imagen-3.git
    cd google-imagen-3
    ```

2.  **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, install them individually:

    ```bash
    pip install python-dotenv google-genai Pillow
    ```

3.  **Configure API Key:**

    *   Create a `.env` file in the same directory as `imagen_with_refinement.py` (or `imagen_no_refinement.py` if you are using the simplified version).
    *   Add your Google Generative AI API key to `.env`:

        ```env
        GOOGLE_API_KEY=YOUR_API_KEY_HERE
        ```

        **Replace `YOUR_API_KEY_HERE` with your actual API key.**

4.  **(Optional) Imagen Prompt Guide:**
    *   For prompt refinement to function (using `imagen_with_refinement.py`), ensure you have the `imagen_prompt_guide.md` file in the same directory. This file should contain the content from the [Imagen Prompt Guide documentation](https://ai.google.dev/gemini-api/docs/imagen-prompt-guide).

### Usage

#### Generate Images with Prompt Refinement (`imagen_with_refinement.py`)

1.  Run the script from your terminal:

    ```bash
    python imagen_with_refinement.py
    ```

2.  You will be prompted to enter your image prompt, desired aspect ratio, and number of images to generate.

    ```
    === Imagen 3 Prompt Refinement and Image Generator ===
    This tool will refine your prompt using Gemini and generate an image using Imagen 3.
    The image will be saved in the same directory as this script.

    Enter your image prompt: Your Image Prompt Here (e.g., "a futuristic cityscape at sunset")

    Available aspect ratios: 1:1, 3:4, 4:3, 9:16, 16:9
    Enter desired aspect ratio (default: 16:9): [Press Enter for default or type aspect ratio]

    Enter number of images to generate (1-4, default: 1): [Press Enter for default or type number]
    ```

3.  The script will refine your prompt using Gemini, generate the image(s) using Imagen 3, and save them as PNG files (e.g., `your_prompt_generated_image_timestamp_random.png`) in the same directory.

#### Generate Images Without Prompt Refinement (`imagen_no_refinement.py`)

1.  Run the simplified script:

    ```bash
    python imagen_no_refinement.py
    ```

2.  Follow the same prompts as above to enter your image prompt, aspect ratio, and number of images. This script will directly use your prompt with Imagen 3, bypassing the Gemini refinement step.

## Prompt Writing Tips for Imagen 3

To maximize the quality of your generated images, consider these prompt writing guidelines (refer to the comprehensive [Imagen Prompt Guide](https://ai.google.dev/gemini-api/docs/imagen-prompt-guide) for more in-depth information):

*   **Descriptive Prompts are Key**: Employ rich adjectives and adverbs to paint a vivid and detailed picture of your desired image for the AI.
*   **Contextualize the Scene**: Provide ample background information and context to aid the AI's understanding of the scene you envision.
*   **Specify Visual Style**: Clearly indicate the desired visual style (e.g., "photograph," "painting," "digital art," "sketch"). Be as precise as possible (e.g., "watercolor painting," "hyperrealistic digital art," "vintage black and white photograph").
*   **Leverage Modifiers**: Experiment with photography-related modifiers (lighting conditions, lens types, camera angles), artistic styles, and image quality enhancers to fine-tune your generated images.
*   **Iterate and Refine**: Prompt engineering is an iterative process. Don't hesitate to experiment with different prompts and modifiers to progressively refine your output and achieve your artistic vision.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.