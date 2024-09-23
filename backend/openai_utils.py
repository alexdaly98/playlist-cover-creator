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


def describe_images_mix(urls):
    content = [
            {
            "type": "text",
            "text": "Based on the images you have, give a description of a unique image that would be a mix or fusion of all these images.",
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


def fusion_images(urls, model="dall-e-3", size="1024x1024"):
    mix_prompt = describe_images_mix(urls)
    mix_prompt = mix_prompt[:3900]
    url_output = get_openai_image(mix_prompt, model=model, size=size)
    return url_output


def fusion_titles_artists(tracks):
    prompt = "Create a nice thumbnail for a playlist containing the following tracks, if there is anything that may cause a system censor just ignore it:\n"
    for track in tracks:
        prompt+=f"{track['title']}, {track['artist']}\n"
    url_output = get_openai_image(prompt)
    return url_output


urls_test1 = [
    "https://i.scdn.co/image/ab67616d0000b27314b67fd4cfcdaba9fc304f05",
    "https://i.scdn.co/image/ab67616d0000b2736b5fd0bb5d38047c28d21e52"
]

urls_test2 = [
    "https://i.scdn.co/image/ab67616d0000b2734fae1e875cb0457ce1b1caad",
    "https://i.scdn.co/image/ab67616d0000b27386a7e547f838b25ecb97d52c"
]
