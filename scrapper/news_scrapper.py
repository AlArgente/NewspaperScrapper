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
    def __init__(self, name: str, url: str, parser='html.parser') -> None:
        self.__newspaper_name = name
        self.__newspaper_url = url
        self.__parser = parser
        self.__bs4 = BeautifulSoup

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
        metadata = ''
        metadata += 'DATE EXTRACTED: ' + date_extracted + '\n'
        metadata += 'TITLE: ' + title + '\n'
        metadata += 'N_IMAGES: ' + str(n_images) + '\n'
        metadata += 'URL: ' + url + '\n'
        return metadata

    @abstractmethod
    def crawl_website(self, soup):
        """Function to crawl the website and get all the news from the
        newspaper url

        Args:
            soup (BeautifulSoup object): BeautifulSoup object to get the
            information from the website.
        """

    @abstractmethod
    def get_info_from_newspaper(self, url):
        """Function to extract text, title and images_src from a url
        from a newspaper.

        Args:
            url (str): url to extract data from

        Returns:
            list, list, str: Return a list with the text, a list with
            the images sources and the tittle of the news.
        """

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
            subprocess.Popen(cmd).communicate()

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

    def pipeline(self):
        """Basic pipeline for extracting information from the newspaper website
        """
        response = requests.get(self.__newspaper_url)
        website_html = response.text
        soup = self.__bs4(website_html, self.__parser)
        self.crawl_website(soup=soup)
