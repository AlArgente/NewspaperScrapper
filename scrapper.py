"""File to get data from multiple spanish newspapers.
Actually works on elpais newspaper, but will add more
when possible.

The extracted data is the title, text and images from the
article. (Still testing if the images are only from the article
or if I'm extracting others from the url that aren't important.)

Images are extracted to possible future work, but the main
interest is to get the text from the article.

This work is done for research purpose. Please, use it with caution.

Author: Alberto Argente del Castillo Garrido
Github: AlArgente
"""
import os
import time
import subprocess
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_info_from_article_elpais(url):
    """Function to extract text, title and images_src from a url
    from the spanish newspaper 'elpais'

    Args:
        url (str): url to extract data from

    Returns:
        list, list, str: Return a list with the text, a list with
        the images sources and the tittle of the news.
    """
    response = requests.get(url)
    website_html = response.text
    soup = BeautifulSoup(website_html, 'html.parser')
    title = soup.find(name='h1', class_='a_t').getText()
    images_src = [img.get('src') for img in soup.find_all('img')]
    article = soup.find_all(name='div', class_='a_c clearfix')
    p_tags_text = [art_p_tags.getText()for art in article for art_p_tags in art.find_all('p')]
    return p_tags_text, images_src, title

def create_metadata_for_url(title, n_images, url):
    """Function to create metada for the url.

    Args:
        title (str): Title of the news
        n_images (int): Number of images from the news
        url (str): url to the news

    Returns:
        str: metadata description.
    """
    now = datetime.now()
    date_extracted = '_'.join(now.strftime('%D').split('/'))
    metadata = ''
    metadata += 'DATE EXTRACTED: ' + date_extracted + '\n'
    metadata += 'TITLE: ' + title + '\n'
    metadata += 'N_IMAGES: ' + str(n_images) + '\n'
    metadata += 'URL: ' + url + '\n'
    return metadata

NEWSPAPERS = {
    'elpais': 'https://elpais.com'
}

NEWSPAPERS_SCRAPPER_FUNC = {
    'elpais': get_info_from_article_elpais
}

def main():
    """Access through multiple websites and get the news in them.
    """
    cnt_news_scrapped = 0
    for newspaper, website in NEWSPAPERS.items():
        response = requests.get(website)
        website_html = response.text
        soup = BeautifulSoup(website_html, 'html.parser')
        headers2 = soup.find_all(name='h2', class_='c_t')
        all_links = [tag.find('a').get('href') for tag in headers2]
        all_links_clean = [link for link in all_links if link[0] == '/']
        # Thinking about what to do with externals links.
        # all_links_externals = [link for link in all_links if link[0]!='/']
        # If folder doest not exists, create one.
        if not os.path.isdir(newspaper):
            os.mkdir(newspaper)
        for link in all_links_clean:
            # If the folder exists, we already has the news, and we only want
            # those news we don't have.
            procesed_link = '_'.join(link.split('/'))
            link_path = newspaper + '/' + procesed_link
            if not os.path.isdir(link_path):
                os.mkdir(link_path)
                file_url = website+link
                scrapper_fun = NEWSPAPERS_SCRAPPER_FUNC[newspaper]
                text, images_src, title = scrapper_fun(file_url)
                metadata = create_metadata_for_url(title, len(images_src), file_url)
                metadata_file = link_path + '/METADATA.txt'
                with open(metadata_file, 'w') as fp:
                    fp.write(metadata)
                text_file = link_path + '/text_news.txt'
                with open(text_file, 'w') as fp:
                    for txt in text:
                        fp.write(txt)
                if len(images_src) > 0:
                    img_folder = link_path + '/img/'
                    os.mkdir(img_folder)
                    # Download all the images
                    for img_url in images_src:
                        cmd = ['wget', img_url, '-P', img_folder]
                        subprocess.Popen(cmd).communicate()
            cnt_news_scrapped += 1
            # To prevent a max connection count by timer and to not saturate the web.
            if cnt_news_scrapped % 10 == 0:
                time.sleep(60)

if __name__ == '__main__':
    main()
