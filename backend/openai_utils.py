"""
This module provides utility functions to interact with OpenAI's API for generating
descriptions and images (e.g., playlist thumbnails) using GPT and DALL·E models.

Required:
- `OPENAI_API_KEY` must be set in `config.py`
"""

from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize OpenAI client with API key from config
client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_chat_single_request(message: str) -> str:
    """
    Sends a single message to GPT and returns the response.

    Args:
        message (str): Prompt for GPT.

    Returns:
        str: GPT-generated response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] GPT Chat request failed: {e}")
        return ""


def get_openai_image(prompt: str, model="dall-e-3", size="1024x1024") -> str:
    """
    Generates an image using OpenAI DALL·E from a text prompt.

    Args:
        prompt (str): Description of the image.
        model (str): DALL·E model to use.
        size (str): Output image size.

    Returns:
        str: URL of the generated image.
    """
    try:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size=size,
            quality="standard"
        )
        return response.data[0].url
    except Exception as e:
        print(f"[ERROR] Image generation failed: {e}")
        return ""


def describe_images_mix(urls: list, mood: str, playlist_title: str) -> str:
    """
    Creates a description that fuses multiple images, considering mood and playlist title.

    Args:
        urls (list): List of image URLs.
        mood (str): Optional mood.
        playlist_title (str): Optional playlist title.

    Returns:
        str: GPT-generated description.
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] describe_images_mix failed: {e}")
        return ""


def fusion_images(urls: list, mood: str, playlist_title: str, model="dall-e-3", size="1024x1024") -> str:
    """
    Generates a thumbnail by fusing multiple images and passing the description to DALL·E.

    Args:
        urls (list): Image URLs to fuse.
        mood (str): Mood for the image.
        playlist_title (str): Title for vibe inspiration.
        model (str): Image model.
        size (str): Image size.

    Returns:
        str: URL of the generated image.
    """
    base_prompt = (
        "Create a nice thumbnail for a playlist, based on the image description given below. "
        "Ensure there are no visible borders or frames around the image; it should seamlessly fill the entire space. "
        "If there is anything that may cause a system censor just ignore it.\n\n"
    )
    mix_prompt = base_prompt + describe_images_mix(urls, mood, playlist_title)
    mix_prompt = mix_prompt[:3900]  # Trim for token safety
    return get_openai_image(mix_prompt, model=model, size=size)


def describe_titles_artists_mix(tracks: list, mood: str, playlist_title: str) -> str:
    """
    Generates a visual description by fusing track titles and artists with mood and title.

    Args:
        tracks (list): Track dicts with 'title' and 'artist'.
        mood (str): Mood for inspiration.
        playlist_title (str): Playlist title.

    Returns:
        str: GPT-generated image description.
    """
    prompt = "Based on the tracks titles and artists you have below, give a description of a unique image that would be a mix or fusion of all these images."
    if mood:
        prompt += f" The mood or style of the image is '{mood}'."
    if playlist_title:
        prompt += f" Use the following title as a base for the vibe of the image: {playlist_title}."

    prompt += "\n\nTracks:\n"
    for track in tracks:
        prompt += f"{track['title']}, {track['artist']}\n"

    return get_openai_chat_single_request(prompt)


def fusion_titles_artists(tracks: list, mood: str, playlist_title: str, model="dall-e-3", size="1024x1024") -> str:
    """
    Generates a playlist image based on fused track titles, artists, mood, and title.

    Args:
        tracks (list): Track dicts.
        mood (str): Desired mood.
        playlist_title (str): Playlist title.
        model (str): Image model.
        size (str): Image size.

    Returns:
        str: URL of the generated image.
    """
    base_prompt = (
        "Create a nice thumbnail for a playlist, based on the image description given below. "
        "Ensure there are no visible borders or frames around the image; it should seamlessly fill the entire space. "
        "If there is anything that may cause a system censor just ignore it. Do not write words in the image.\n\n"
    )
    mix_prompt = base_prompt + describe_titles_artists_mix(tracks, mood, playlist_title)
    mix_prompt = mix_prompt[:3900]
    return get_openai_image(mix_prompt, model=model, size=size)
