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
"""Abstrac class for news scrapper.
"""
import os
import time
import subprocess
from datetime import datetime
from abc import abstractmethod, ABC
import requests
from bs4 import BeautifulSoup


class NewsScrapper(ABC):
    """Abstrac class for the different newspaper scrapper. In this way
    every newspaper will have their own scrapper, but keeping the same
    structure.
    """
    def __init__(self, name: str, url: str, parser='html.parser', header_name_news='', 
                 header_class_news='', newsarticle_title_name='', newsarticle_title_class='',
                 newsarticle_body_name='', newsarticle_body_class='') -> None:
        self.__newspaper_name = name
        self.__newspaper_url = url
        self.__parser = parser
        self.__bs4 = BeautifulSoup
        self.__header_name_news=header_name_news
        self.__header_class_news=header_class_news
        self.__newsarticle_title_name=newsarticle_title_name
        self.__newsarticle_title_class=newsarticle_title_class
        self.__newsarticle_body_name=newsarticle_body_name
        self.__newsarticle_body_class=newsarticle_body_class

    @property
    def name_(self):
        """Name property.

        Returns:
            str: Newspaper's name
        """
        return self.__newspaper_name

    @property
    def url_(self):
        """Url property

        Returns:
            str: Newspaper's url
        """
        return self.__newspaper_url

    @property
    def parser_(self):
        """Parser property

        Returns:
            str/parser_type: Return the parser used to get the information.
        """
        return self.__parser
    
    @property
    def bs4_(self):
        """BeautifulSoup object to scrape the websites
        
        Returns:
            BeautifulSoup object: BeautifulSoup object to scrappe the website.
        """
        return self.__bs4

    @abstractmethod
    def _clean_news_links(self, all_links):
        """Function to clean the urls obtained at the newspaper home page.

        Args:
            all_links (list): List containing the urls of the news

        Returns:
            list: List with the urls cleaned to do an easy access to them.
        """

    @abstractmethod
    def _create_news_url(self, link):
        """Function to generate the full url of the news that is going to be parsed.

        Args:
            all_links (list): List containing the urls of the news

        Returns:
            list: List with the urls cleaned to do an easy access to them.
        """

    @abstractmethod
    def _get_link_path(self, link):
        """Function that process the news url to create a path for it,
        so the system can create an easy folder if the news isn't saved
        on disk.

        Args:
            link (str): News url

        Returns:
            str: Path of the folder where the data will be saved.
        """

    def create_metadata_for_newspaper_url(self, title, url, n_images):
        """Function to create the metadata for a url from the newspaper

        Args:
            title (str): News title
            url (str): News url
            n_images (int): Number of images
        Returns:
            str: Must return the metadata for the news that is being analyzed.
        """
        now = datetime.now()
        date_extracted = '_'.join(now.strftime('%D').split('/'))
        return str(
            f'DATE EXTRACTED: {date_extracted}\n'
            f'TITLE: {title}\n'
            f'N_IMAGES: {n_images}\n'
            f'URL: {url}\n'
        )

    def _save_metadata(self, metadata, file_path):
        """Function to save the metadata from a news article in a file.

        Args:
            metadata (str): Metadata information to be saved
            file_path (str): Name of the file where metadata is being writen.
        """
        metadata_file = file_path + '/METADATA.txt'
        with open(metadata_file, 'w') as file:
            file.write(metadata)

    def _save_text(self, text, file_path):
        """Function to save the news article text in a file.

        Args:
            text (str): News text to be saved.
            file_path (str): Name of the file where metadata is being writen.
        """
        text_file = file_path + '/text_news.txt'
        with open(text_file, 'w') as file:
            for txt in text:
                file.write(txt)

    def _save_images(self, images_src, img_folder):
        """Function to save the images from a news article. This function
        will create a folder called 'img' where it's going o download
        all the images from a news article.

        Args:
            images_src (list): List with the images urls
            img_folder (str): Path to save the images
        """
        img_folder = img_folder + '/img/'
        os.mkdir(img_folder)
        for img_url in images_src:
            # Download all the images
            cmd = ['wget', img_url, '-P', img_folder]
            try:
                subprocess.Popen(cmd).communicate()
            except TypeError:
                continue

    def pipeline(self):
        """Basic pipeline for extracting information from the newspaper website
        """
        soup = self._init_bs4(self.__newspaper_url)
        self.crawl_website(soup, self.__header_name_news, self.__header_class_news,
                           self.__newsarticle_title_name, self.__newsarticle_title_class,
                           self.__newsarticle_body_name, self.__newsarticle_body_class)

    def _init_bs4(self, url):
        """Function to init a BeautifulSoup object

        Args:
            url (str): Url from newspaper to be scrapped

        Returns:
            BeautifulSoup object: BeautifulSoup object that has parsed the url
        """
        response = requests.get(url)
        website_html = response.text
        return self.__bs4(website_html, self.__parser)

    def crawl_website(self, soup, header_name_news, header_class_news,
                      newsarticle_title_name, newsarticle_title_class,
                      newsarticle_body_name, newsarticle_body_class):
        """Function to fully crawl a newspaper website. This function will crawl the
        newspaper main page and get all the news and save them to our local data.

        Args:
            soup (BeautifulSoup Object): BeautifulSoup object to crawl the website
            header_name_news (str): Headers at the main page that contain the news
            header_class_news (str): header_name_news class in the html file.
            newsarticle_title_name (str): String with the news article title name in the html file
            newsarticle_title_class (str): String with the news article title class in the html file
            newsarticle_body_name (str): String with the news body name in the html file.
            newsarticle_body_class (str): String with the news body class in the html file.
        """
        # Get all links
        newspaper = self.__newspaper_name
        headers = soup.find_all(name=header_name_news, class_=header_class_news)
        all_links = [tag.find('a').get('href') for tag in headers]
        # Clean news articles links
        all_links = self._clean_news_links(all_links)
        # Create folder if doesn't exists
        if not os.path.isdir(newspaper):
            os.mkdir(newspaper)
        # iterate over links_cleaned
        for cnt_news_scrapped, link in enumerate(all_links):
            link_path = self._get_link_path(link)
            # Create a folder for the news article if it doesn't exists in our local data.
            if not os.path.isdir(link_path):
                os.mkdir(link_path)
                # Get news_url.
                news_url = self._create_news_url(link)
                # Get text, images url and article's title
                text, images_src, title = self.get_info_from_newspaper(news_url, newsarticle_title_name, 
                                                                       newsarticle_title_class, newsarticle_body_name,
                                                                       newsarticle_body_class)
                # Create and save metadata metadata
                self._create_and_save_metadata(title, news_url, len(images_src), link_path)
                self._save_text(text, link_path)
                if len(images_src) > 0:
                    self._save_images(images_src=images_src, img_folder=link_path)
            # To prevent a max connection count by timer and to not saturate the web.
            if cnt_news_scrapped % 30 == 0 and cnt_news_scrapped > 1:
                print('Having a minute break.')
                time.sleep(60)
            cnt_news_scrapped += 1

    def get_info_from_newspaper(self, url, newsarticle_title_name, newsarticle_title_class,
                                   newsarticle_body_name, newsarticle_body_class):
        """Function to extract text, title and images_src from a url
        from a newspaper.

        Args:
            url (str): url to extract data from
            newsarticle_title_name (str): String with the news article title name in the html file
            newsarticle_title_class (str): String with the news article title class in the html file
            newsarticle_body_name (str): String with the news body name in the html file.
            newsarticle_body_class (str): String with the news body class in the html file.

        Returns:
            list, list, str: Return a list with the text, a list with
            the images sources and the tittle of the news.
        """
        soup = self._init_bs4(url)
        try:
            title = soup.find(name=newsarticle_title_name, class_=newsarticle_title_class).getText()
        except AttributeError:
            title = 'NoTitleAvailable'
        # Images src must be improved to just select those from the body.
        images_src = self._get_images_src(soup)
        article = soup.find_all(name=newsarticle_body_name, class_=newsarticle_body_class)
        p_tags_text = self._get_paragraph_text(article)
        return p_tags_text, images_src, title

    def _create_and_save_metadata(self, title, link, n_images, file_path):
        """Function that create and save metadata from the news article into our local system.

        Args:
            title (str): Title of the news article
            link (str): Url of the news article
            n_images (int): Number of images from the news article
            file_path (str): Path to save the data in our local system
        """
        metadata = self.create_metadata_for_newspaper_url(title=title, url=link, n_images=n_images)
        self._save_metadata(metadata=metadata, file_path=file_path)

    def _get_paragraph_text(self, article):
        """Function to get the text from the news article.

        Args:
            article (beautiful soup object): bs4 object that contains all the paragraphs from 
            a newspaper article.

        Returns:
            list: List containing all the paragraphs from the text.
        """
        return [art_p_tags.getText() for art in article for art_p_tags in art.find_all('p')]

    def _get_images_src(self, soup):
        """Function to get the images url from a news article to download them later.

        Args:
            soup (bs4 object): bs4 object initialized over a newspaper article.
        """
        return [img.get('src') for img in soup.find_all('img')]
