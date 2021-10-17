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
"""Document that implement a crawler for ABC newspaper

This work is done for research purpose. Please, use it with caution.

Author: Alberto Argente del Castillo Garrido
Github: AlArgente
"""

import requests
from scrapper.news_scrapper import NewsScrapper


class ABCScrapper(NewsScrapper):
    """Class that implements a crawler for ElMundo newspaper

    This class use the abstract class NewsScrapper as a base class,
    so it's important to look for that class first in case to do an own
    scrapper.
    """
    def __init__(self, parser='html.parser') -> None:
        name = 'abc'
        url = 'https://www.abc.es/'
        header_name_news = 'h3'
        header_class_news = 'titular lead-title'
        newsarticle_title_name = 'span'
        newsarticle_title_class = 'titular'
        newsarticle_body_name = 'span'
        newsarticle_body_class = 'cuerpo-texto'
        super().__init__(name, url, parser, header_name_news, header_class_news,
                         newsarticle_title_name, newsarticle_title_class, 
                         newsarticle_body_name, newsarticle_body_class)

    def _get_link_path(self, link: str):
        """Function that process the news url to create a path for it,
        so the system can create an easy folder if the news isn't saved
        on disk.

        Args:
            link (str): News url

        Returns:
            str: Path of the folder where the data will be saved.
        """
        procesed_link = '_'.join(link.split('/'))
        return self.name_ + '/' + procesed_link

    def _clean_news_links(self, all_links: list):
        """Function to clean the urls obtained at the newspaper home page.
        This function must be overrided at some classes if necessary.
        In ABC we just need to select those that starts with /, as the
        fully url are external from the newspaper.

        Args:
            all_links (list): List containing the urls of the news

        Returns:
            list: List with the urls cleaned to do an easy access to them.
        """
        return [link for link in all_links if link[0] == '/']

    def _create_news_url(self, link: str):
        """Function to generate the full url of the news that is going to be parsed.
        In ElMund we don't need to do anything, so just return the link

        Args:
            link (str): str containing the url of the news that is going to be parsed.

        Returns:
            str: Full url of the news
        """
        return self.url_ + link

    def _init_bs4(self, url: str):
        """Function to init a BeautifulSoup object
        Overrided to be able to extract the data from the newspaper,
        beacause of the need of headers.

        Args:
            url (str): Url from newspaper to be scrapped

        Returns:
            BeautifulSoup object: BeautifulSoup object that has parsed the url
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        source=requests.get(url, headers=headers).text
        return self.bs4_(source, self.parser_)
