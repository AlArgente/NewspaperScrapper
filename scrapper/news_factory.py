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
"""File containing the factory class for the scrapper so the user
only has to select one it's name.
"""

from scrapper.elpais_scrapper import ElPaisScrapper


class NewsFactory:
    """Factory class to select the correct scrapper with only
    using the name of the newspaper.
    """
    def __init__(self, name: str, parser='html.parser'):
        self.__name = name
        self.__scrapper = None
        self.__load_class(parser=parser)

    @property
    def scrapper_(self):
        """Scrapper property.

        Returns:
            NewsScrapper object: Object that will get the information from a newspaper site.
        """
        return self.__scrapper

    def __load_class(self, parser):
        """Function to load the newspaper scrapper
        """
        if self.__name == 'elpais':
            self.__scrapper = ElPaisScrapper(parser=parser)
        else:
            raise ValueError('No other newspaper available now. Sorry!')

    def pipeline(self):
        """Function to apply the pipeline from the scrapper.
        """
        self.__scrapper.pipeline()
