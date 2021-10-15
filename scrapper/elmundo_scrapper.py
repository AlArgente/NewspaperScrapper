# MIT License
# Copyright (c) 2021 Alberto Argente del Castillo Garrido
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Document that implement a crawler for ElPais newspaper

This work is done for research purpose. Please, use it with caution.

Author: Alberto Argente del Castillo Garrido
Github: AlArgente
"""

import os
import time
import requests
from scrapper.news_scrapper import NewsScrapper


class ElMundoScrapper(NewsScrapper):
    """Class that implements a crawler for ElMundo newspaper

    This class use the abstract class NewsScrapper as a base class,
    so it's important to look for that class first in case to do an own
    scrapper.
    """
    def __init__(self, parser='html.parser') -> None:
        name = 'elmundo'
        url = 'https://www.elmundo.es/'
        super().__init__(name, url, parser)

    def crawl_website(self, soup):
        """Function to crawl the website and get all the news from the
        newspaper url

        See base class for more information.
        Args:
            soup (BeautifulSoup object): BeautifulSoup object to get the
            information from the website.
        """
        newspaper = self.name_
        website = self.url_
        # Get all the headers that contains the news
        headers = soup.find_all(name='header', class_='ue-c-cover-content__headline-group')
        # No need further processing as we have the full link of the news
        all_links = [tag.find('a').get('href') for tag in headers]
        if not os.path.isdir(newspaper): # Crate a folder: newspaper/
            os.mkdir(newspaper)
        for cnt_news_scrapped, link in enumerate(all_links):
            link_name = link.rpartition(website)[2]
            link_name = '_'.join(link_name.split('/'))
            link_path = newspaper + '/' + link_name
            if not os.path.isdir(link_path):
                # Create a folder: newspaper/link
                os.mkdir(link_path)
                text, images_src, title = self.get_info_from_newspaper(link)
                metadata = self.create_metadata_for_newspaper_url(title, link, len(images_src))
                metadata_file = link_path + '/METADATA.txt'
                self._save_metadata(metadata, metadata_file)
                text_file = link_path + '/text_news.txt'
                self._save_text(text, text_file)
                if len(images_src) > 0:
                    self._save_images(images_src=images_src, img_folder=link_path)
            # To prevent a max connection count by timer and to not saturate the web.
            if cnt_news_scrapped % 30 == 0:
                print('Having a minute break!')
                time.sleep(60)
            cnt_news_scrapped += 1

    def get_info_from_newspaper(self, url):
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
        soup = self.bs4_(website_html, self.parser_)
        # title = soup.find(name='h1', class_='ue-c-article__headline js-headline').getText() or 'NoTitleAvailable'
        try:
            title = soup.find(name='h1', class_='ue-c-article__headline js-headline').getText()
        except AttributeError:
            title = 'NoTitleAvailable'
        images_src = [img.get('src') for img in soup.find_all('img')]
        article = soup.find_all(name='div', class_='ue-l-article__body ue-c-article__body')
        p_tags_text = [art_p_tags.getText() for art in article for art_p_tags in art.find_all('p')]
        return p_tags_text, images_src, title
