import requests
from bs4 import BeautifulSoup


class PinterestScraper:
    def load_images(self):
        # html = ''

        # with open('pinterest_page.html', 'r', encoding='utf-8') as image:
        #     for line in image.read():
        #         html += line

        url = "https://www.pinterest.com/trillionsssssss/"
        response = requests.get(url)
        html = response.content

        return html

    def parse(self, html):
        content = BeautifulSoup(html, "lxml")
        # print([image['src'] for image in content.findAll('img')])
        return [image["src"] for image in content.findAll("img")]

    def download(self, url):
        response = requests.get(url)
        filename = url.split("/")[-1]

        print("Downloading image %s from URL %s" % (filename, url))

        if response.status_code == 200:
            with open("./images/" + filename, "wb") as image:
                for chunk in response.iter_content(chunk_size=128):
                    image.write(chunk)

    def run(self):
        html = self.load_images()
        urls = self.parse(html)
        print(urls)

        for url in urls:
            self.download(url)


if __name__ == "__main__":
    scraper = PinterestScraper()
    scraper.run()
