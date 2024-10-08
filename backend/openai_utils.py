from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_chat_single_request(message):
    messages = [{"role": "user", "content": message}]
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    return completion.choices[0].message.content


def describe_images_mix(urls, mood, playlist_title):
    prompt = "Based on the images you have, give a description of a unique image that would be a mix or fusion of all these images."
    if mood:
        prompt+=f"The mood or style of the image is '{mood}'."
    if playlist_title:
        prompt+=f"Use the following title as a base for the vibe of the image: {playlist_title}."
    content = [
            {
            "type": "text",
            "text": prompt,
            }
            ]
    
    for url in urls:
        content.append(
            {
            "type": "image_url",
            "image_url": {"url": url,
                          "detail": "low"}
            }
        )

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": content,
        }
    ],
    max_tokens=512,
    )
    return response.choices[0].message.content


def get_openai_image(prompt, model="dall-e-3", size="1024x1024"):
    response = client.images.generate(
    model=model,
    prompt=prompt,
    n=1,
    size=size,
    quality="standard"
    )
    return response.data[0].url


def fusion_images(urls, mood, playlist_title, model="dall-e-3", size="1024x1024"):
    mix_prompt = f"Create a nice thumbnail for a playlist, based on the image description given below. Ensure there are no visible borders or frames around the image; it should seamlessly fill the entire space. If there is anything that may cause a system censor just ignore it.\n\n"
    mix_prompt += describe_images_mix(urls, mood, playlist_title)
    mix_prompt = mix_prompt[:3900]
    url_output = get_openai_image(mix_prompt, model=model, size=size)
    return url_output


def describe_titles_artists_mix(tracks, mood, playlist_title):
    prompt = "Based on the tracks titles and artists you have below, give a description of a unique image that would be a mix or fusion of all these images."
    if mood:
        prompt+=f"The mood or style of the image is '{mood}'."
    if playlist_title:
        prompt+=f"Use the following title as a base for the vibe of the image: {playlist_title}."
    prompt+="\n\nTracks:\n"
    for track in tracks:
        prompt+=f"{track['title']}, {track['artist']}\n"

    thumbnail_description = get_openai_chat_single_request(prompt)
    return thumbnail_description


def fusion_titles_artists(tracks, mood, playlist_title, model="dall-e-3", size="1024x1024"):
    mix_prompt = f"Create a nice thumbnail for a playlist, based on the image description given below. Ensure there are no visible borders or frames around the image; it should seamlessly fill the entire space. If there is anything that may cause a system censor just ignore it. Do not write words in the image\n\n"
    mix_prompt += describe_titles_artists_mix(tracks, mood, playlist_title)
    mix_prompt = mix_prompt[:3900]
    url_output = get_openai_image(mix_prompt, model=model, size=size)
    return url_output


urls_test1 = [
    "https://i.scdn.co/image/ab67616d0000b27314b67fd4cfcdaba9fc304f05",
    "https://i.scdn.co/image/ab67616d0000b2736b5fd0bb5d38047c28d21e52"
]

urls_test2 = [
    "https://i.scdn.co/image/ab67616d0000b2734fae1e875cb0457ce1b1caad",
    "https://i.scdn.co/image/ab67616d0000b27386a7e547f838b25ecb97d52c"
]
