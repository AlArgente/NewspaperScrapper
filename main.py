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


from scrapper.news_factory import NewsFactory

def print_available_newspaper_scrappers():
    """Function to print the available newspaper scrappers.
    """
    newspapers = ['elpais', 'elmundo', 'abc']
    print('The newspaper available are:')
    for i, newspaper in enumerate(newspapers, start=1):
        print(f'{i}.- {newspaper}')
    print('Please, select one from the showed above.')

def main():
    """Main function.
    """
    print_available_newspaper_scrappers()
    newspaper = input('Input the newspaper name you want to save the news: ')
    # Load the newspaper scrapper.
    # newspaper = 'elpais' # As there is only one available, no input needed.
    factory = NewsFactory(newspaper)
    # Download all the news available at the newspaper site.
    factory.pipeline()

if __name__ == '__main__':
    main()
