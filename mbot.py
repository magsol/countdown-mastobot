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
    toots = m.timeline_home(limit = 1)
    ts = toots[0]['created_at'].astimezone(tz = datetime.now(timezone.utc).astimezone().tzinfo)
    now = datetime.now()
    if ts.year == now.year and ts.month == now.month and ts.day == now.day:
        print("Already made a post today! Quitting.")
        quit()
    
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
        images_initial = fp.readlines()
    images_final = []
    for image in images_initial:
        if image.endswith("jpeg") or image.endswith("png"):
            im = Image.open(image)
            if im.size[0] > 1000:
                images_final.append(image)
    image_id = random.randint(0, len(images_final) - 1)
    image = images_final[image_id]
    print(image)

    ### Step 3: make the post
    # https://mastodonpy.readthedocs.io/en/stable/05_statuses.html#writing

    # First, post the media.
    media = m.media_post(image)
    # Then, post the update.
    post = m.status_post(f"{dt} days until Tears of the Kingdom.", 
                         media_ids = media, 
                         sensitive = True if media is not None else False)

    ### All done!
    print("Posted! Quitting.")
