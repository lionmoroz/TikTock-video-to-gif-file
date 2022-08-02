
#validator
    # function that help valid url
#download video from ticktock
    # function that download video from ticktock
#convert in to gif
    # function that conver video in to gif




from TikTokApi import TikTokApi
from moviepy.editor import VideoFileClip
import os
import re
import urllib

input_url = str(input("Enter tiktok url(if you haven't url click enter): "))
default_urls = 'https://www.tiktok.com/@baptistefernandez1/video/7079817362693688581?is_copy_url=1&is_from_webapp=v1&q=programing&t=1659422697792'

DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)" # http basic authentication [optional]
    r"(?:(?:(?=\S{0,253}(?:$|:))" # check full domain length to be less than or equal to 253 (starting after http basic auth, stopping before port)
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+" # check for at least one subdomain (maximum length per subdomain: 63 characters), dashes in between allowed
    r"(?:[a-z0-9]{1,63})))" # check for top level domain, no dashes allowed
    r"|localhost)" # accept also "localhost" only
    r"(:\d{1,5})?", # port [optional]
    re.IGNORECASE
)
SCHEME_FORMAT = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$", # scheme: http(s) or ftp(s)
    re.IGNORECASE
)

def validate_url(url: str):
    url = url.strip()

    if not url:
        print("if you haven't url we use default")
        return default_urls

    if len(url) > 2048:
        raise Exception("URL exceeds its maximum length of 2048 characters (given length={})".format(len(url)))

    result = urllib.parse.urlparse(url)
    scheme = result.scheme
    domain = result.netloc

    if not scheme:
        raise Exception("No URL scheme specified")

    if not re.fullmatch(SCHEME_FORMAT, scheme):
        raise Exception("URL scheme must either be http(s) or ftp(s) (given scheme={})".format(scheme))

    if not domain:
        raise Exception("No URL domain specified")

    if not re.fullmatch(DOMAIN_FORMAT, domain):
        raise Exception("URL domain malformed (domain={})".format(domain))

    return url



def download_tiktok(url):
    """Function download video from Tiktok argument is url video."""
    with TikTokApi() as api:
        video = api.video(url=url)
        video_name = video.author.username
        video_data = video.bytes()        # Bytes of the TikTok video
        with open(f"TikTok-example-{video_name}", "wb") as out_file:
            out_file.write(video_data)
        return out_file.name


def convert_to_gif():
    """Function convert mp4 to gif"""
    file = download_tiktok(validate_url(input_url))
    videoClip = VideoFileClip(f"{file}")
    videoClip.write_gif(f"{file}.gif")

    return print("Path to your gif file "+os.path.abspath(f'{file}.gif'))



convert_to_gif()