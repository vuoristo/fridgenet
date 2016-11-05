import os
import re
import time
import argparse
import requests
import io
import hashlib
from PIL import Image
from multiprocessing import Pool
from selenium import webdriver

argument_parser = argparse.ArgumentParser(description='Download images using google image search')
argument_parser.add_argument('query', metavar='query', type=str, help='The query to download images from')
argument_parser.add_argument('--count', metavar='count', default=100, type=int, help='How many images to fetch')


def ensure_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def largest_file(dir_path):
    def parse_num(filename):
        match = re.search('\d+', filename)
        if match:
            return int(match.group(0))

    files = os.listdir(dir_path)
    if len(files) != 0:
        return max(filter(lambda x: x, map(parse_num, files)))
    else:
        return 0

def fetch_image_urls(query, images_to_download):
    image_urls = set()

    search_url = "https://duckduckgo.com/?q={q}&t=ht&iax=1&ia=images"
    browser = webdriver.Firefox()
    browser.get(search_url.format(q=query))

    time.sleep(3)


    while len(image_urls) < images_to_download:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        images = browser.find_elements_by_css_selector("img.tile--img__img")
        for img in images:
            image_urls.add(img.get_attribute('src'))

    browser.quit()
    return image_urls



def persist_image(image_url):
    size = (256, 256)
    image_content = requests.get(image_url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    resized = image.resize(size)
    with open(query_directory + hashlib.sha1(image_content).hexdigest(), 'wb')  as f:
        resized.save(f, "JPEG", quality=85)


if __name__ == '__main__':
    args = argument_parser.parse_args()

    ensure_directory('./images/')

    query_directory = './images/' + args.query + "/"
    ensure_directory(query_directory)

    image_urls = fetch_image_urls(args.query, args.count)

    image_urls = [url for url in image_urls]

    print(image_urls)
    print("image count", len(image_urls))

    pool = Pool(12)
    pool.map(persist_image, image_urls)
    persist_image(image_urls[0])



