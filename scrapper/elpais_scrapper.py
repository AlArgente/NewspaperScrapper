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


class ElPaisScrapper(NewsScrapper):
    """Class that implements a crawler for ElPais newspaper

    This class use the abstract class NewsScrapper as a base class,
    so it's important to look for that class first in case to do an own
    scrapper.
    """
    def __init__(self, parser='html.parser') -> None:
        name = 'elpais'
        url = 'https://elpais.com'
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
        headers2 = soup.find_all(name='h2', class_='c_t')
        all_links = [tag.find('a').get('href') for tag in headers2]
        all_links_clean = [link for link in all_links if link[0] == '/']
        # Thinking about what to do with externals links.
        # all_links_externals = [link for link in all_links if link[0]!='/']
        # If folder doest not exists, create one.
        if not os.path.isdir(newspaper):
            os.mkdir(newspaper)
        for cnt_news_scrapped, link in enumerate(all_links_clean, start=1):
            # If the folder exists, we already has the news, and we only want
            # those news we don't have.
            procesed_link = '_'.join(link.split('/'))
            link_path = newspaper + '/' + procesed_link
            if not os.path.isdir(link_path):
                os.mkdir(link_path)
                file_url = website+link
                text, images_src, title = self.get_info_from_newspaper(file_url)
                metadata = self.create_metadata_for_newspaper_url(title, file_url, len(images_src))
                metadata_file = link_path + '/METADATA.txt'
                with open(metadata_file, 'w') as f:
                    f.write(metadata)
                text_file = link_path + '/text_news.txt'
                self._save_text(text, text_file)
                if len(images_src) > 0:
                    self._save_images(images_src=images_src, img_folder=link_path)
            # To prevent a max connection count by timer and to not saturate the web.
            if cnt_news_scrapped % 30 == 0:
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
        title = soup.find(name='h1', class_='a_t').getText()
        images_src = [img.get('src') for img in soup.find_all('img')]
        article = soup.find_all(name='div', class_='a_c clearfix')
        p_tags_text = [art_p_tags.getText()for art in article for art_p_tags in art.find_all('p')]
        return p_tags_text, images_src, title
