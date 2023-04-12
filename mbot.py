import argparse
from datetime import datetime, timezone
import os.path
import random

from mastodon import Mastodon
from PIL import Image

API_URL = "quinnwitz.house"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--client-key", type = str, required = True,
                        help = "Application's client key.")
    parser.add_argument("-s", "--client-secret", type = str, required = True,
                        help = "Application's client secret.")
    parser.add_argument("-t", "--access_token", type = str, required = True,
                        help = "Application's access token.")
    parser.add_argument("-i", "--imagefile", type = str, default = "images.txt",
                        help = "Path to the file of images.")
    args = parser.parse_args()

    m = Mastodon(client_secret = args.client_secret,
             client_id = "Countdown",
             access_token = args.access_token,
             api_base_url = API_URL)

    ### Step 0: first, make sure we haven't yet tooted today
    # (juuuust in case this gets run multiple times in one day)
    # https://mastodonpy.readthedocs.io/en/stable/07_timelines.html#mastodon.Mastodon.timeline
    toots = m.timeline_home(limit = 5)
    now = datetime.now()
    for toot in toots:
        ts = toot['created_at'].astimezone(tz = datetime.now(timezone.utc).astimezone().tzinfo)
        if ts.year == now.year and ts.month == now.month and ts.day == now.day:
            # We found a toot that happened today, but was it posted by
            # this application?
            if toot['application'] is not None:
                print(f"Already posted today: {toot['url']}\nQuitting!")
                quit()
            print(f"We've posted today, but manually: {toot['url']}")
    # Reaching this point means this specific app's last toot was either
    # yesterday OR not in the last 5 toots (admittedly not perfect).
    
    ### Step 1: need to determine how many days out we are!
    target = datetime(year = 2023, month = 5, day = 12)
    dt = (target - now).days + 1 # the "+1" is to round up, since there are still some hours left
    #print(f"{dt} days until Tears of the Kingdom")

    ### Step 2: pick an image and upload it to Mastodon.
    # https://mastodonpy.readthedocs.io/en/stable/05_statuses.html#mastodon.Mastodon.media_post
    # https://mastodonpy.readthedocs.io/en/stable/02_return_values.html#media-dict

    # This is annoying, as simple-image-download seems to
    # pick out some common icons by Google Images and treats
    # them as part of the dataset. They're small, usually
    # 80x36, but they and other exotic image formats seem to
    # cause issues. So until we completely overhaul the image
    # download part, this seems like the most reliable.
    with open(args.imagefile, "r") as fp:
        images_initial = list(map(lambda x: x.strip(), fp.readlines()))
    images_final = []
    for image in images_initial:
        if image.endswith("jpeg") or image.endswith("png"):
            im = Image.open(image)
            if im.size[0] > 1000:
                images_final.append(image)
    image_id = random.randint(0, len(images_final) - 1)
    image = images_final[image_id]
    print(f"Image found: {image}")

    ### Step 3: make the post
    # https://mastodonpy.readthedocs.io/en/stable/05_statuses.html#writing

    # First, post the media.
    media = m.media_post(image)
    # Second, do some...flavoring.
    if dt > 30:
        text = "days until Tears of the Kingdom."
    elif dt > 20:
        text = "days until Tears of the Kingdom!"
    elif dt > 10:
        text = "DAYS UNTIL TEARS OF THE KINGDOM!!!"
    else:
        # it's the final countdowwwwwn
        ahhs = (10 - dt + 1) * 2 + random.randint(1, (10 - dt + 2))
        text = f"DAYS UNTIL TEARS OF THE KINGDOM {'A' * ahhs}"
    # Then, post the update.
    post = m.status_post(f"{dt} {text}.", 
                         media_ids = media, 
                         sensitive = True if media is not None else False)

    ### All done!
    print(f"NEW TOOT: {toot['url']}\nFIN (for today).")
