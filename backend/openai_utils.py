"""
This script provides functions to interact with OpenAI's API for generating text descriptions
and AI-generated images. It allows users to describe images or tracks, and generate thumbnails 
based on these descriptions using DALL-E or GPT models.

Key Features:
- Generates text descriptions of images or tracks using GPT models.
- Creates playlist thumbnails based on image URLs or track details using DALL-E.
- Supports customization through mood and playlist title inputs.

Environment Variables Used:
- OPENAI_API_KEY should be set in `config.py` for authentication.
"""

from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize OpenAI client with API key
client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_chat_single_request(message):
    """
    Sends a single message to OpenAI's GPT model and returns the response.

    Args:
        message (str): The input message or prompt for the OpenAI model.

    Returns:
        str: The generated text response from the model.
    """
    messages = [{"role": "user", "content": message}]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return completion.choices[0].message.content


def describe_images_mix(urls, mood, playlist_title):
    """
    Creates a prompt to describe a unique image that fuses multiple images, considering mood and playlist title.

    Args:
        urls (list): A list of image URLs to fuse into a single image.
        mood (str): The desired mood or style of the image (optional).
        playlist_title (str): The playlist title to influence the image's vibe (optional).

    Returns:
        str: The generated description from OpenAI for a fused image based on input images, mood, and title.
    """
    prompt = "Based on the images you have, give a description of a unique image that would be a mix or fusion of all these images."
    if mood:
        prompt += f" The mood or style of the image is '{mood}'."
    if playlist_title:
        prompt += f" Use the following title as a base for the vibe of the image: {playlist_title}."

    content = [{"type": "text", "text": prompt}]
    
    for url in urls:
        content.append({
            "type": "image_url",
            "image_url": {"url": url, "detail": "low"}
        })

    # Send the request to OpenAI's GPT model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": content,
        }],
        max_tokens=512,
    )
    
    return response.choices[0].message.content


def get_openai_image(prompt, model="dall-e-3", size="1024x1024"):
    """
    Generates an image using OpenAI's DALL-E model based on a given text prompt.

    Args:
        prompt (str): The prompt to generate an image.
        model (str, optional): The model to use for image generation. Defaults to "dall-e-3".
        size (str, optional): The size of the generated image. Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image.
    """
    response = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size=size,
        quality="standard"
    )
    
    return response.data[0].url


def fusion_images(urls, mood, playlist_title, model="dall-e-3", size="1024x1024"):
    """
    Combines multiple images into a single playlist thumbnail using OpenAI DALL-E.

    Args:
        urls (list): A list of image URLs to fuse.
        mood (str): The desired mood or style of the image (optional).
        playlist_title (str): The playlist title to influence the image's vibe (optional).
        model (str, optional): The model to use for image generation. Defaults to "dall-e-3".
        size (str, optional): The size of the generated image. Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image thumbnail.
    """
    mix_prompt = (
        "Create a nice thumbnail for a playlist, based on the image description given below. "
        "Ensure there are no visible borders or frames around the image; it should seamlessly "
        "fill the entire space. If there is anything that may cause a system censor just ignore it.\n\n"
    )
    mix_prompt += describe_images_mix(urls, mood, playlist_title)
    
    # Ensure the prompt doesn't exceed token limit
    mix_prompt = mix_prompt[:3900]
    
    url_output = get_openai_image(mix_prompt, model=model, size=size)
    return url_output


def describe_titles_artists_mix(tracks, mood, playlist_title):
    """
    Creates a text prompt to describe a unique image that fuses track titles and artists, considering mood and playlist title.

    Args:
        tracks (list): A list of track dictionaries containing 'title' and 'artist' keys.
        mood (str): The desired mood or style of the image (optional).
        playlist_title (str): The playlist title to influence the image's vibe (optional).

    Returns:
        str: The generated description from OpenAI for a fused image based on track titles, artists, mood, and title.
    """
    prompt = "Based on the tracks titles and artists you have below, give a description of a unique image that would be a mix or fusion of all these images."
    if mood:
        prompt += f" The mood or style of the image is '{mood}'."
    if playlist_title:
        prompt += f" Use the following title as a base for the vibe of the image: {playlist_title}."
    
    prompt += "\n\nTracks:\n"
    for track in tracks:
        prompt += f"{track['title']}, {track['artist']}\n"

    thumbnail_description = get_openai_chat_single_request(prompt)
    return thumbnail_description


def fusion_titles_artists(tracks, mood, playlist_title, model="dall-e-3", size="1024x1024"):
    """
    Combines track titles and artists into a single playlist thumbnail using OpenAI DALL-E.

    Args:
        tracks (list): A list of track dictionaries containing 'title' and 'artist' keys.
        mood (str): The desired mood or style of the image (optional).
        playlist_title (str): The playlist title to influence the image's vibe (optional).
        model (str, optional): The model to use for image generation. Defaults to "dall-e-3".
        size (str, optional): The size of the generated image. Defaults to "1024x1024".

    Returns:
        str: The URL of the generated image thumbnail.
    """
    mix_prompt = (
        "Create a nice thumbnail for a playlist, based on the image description given below. "
        "Ensure there are no visible borders or frames around the image; it should seamlessly "
        "fill the entire space. If there is anything that may cause a system censor just ignore it. "
        "Do not write words in the image.\n\n"
    )
    mix_prompt += describe_titles_artists_mix(tracks, mood, playlist_title)
    
    # Ensure the prompt doesn't exceed token limit
    mix_prompt = mix_prompt[:3900]
    
    url_output = get_openai_image(mix_prompt, model=model, size=size)
    return url_output
