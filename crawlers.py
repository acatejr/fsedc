import requests
from bs4 import BeautifulSoup
import arrow
from pathlib import Path


def strip_html(html_string):
    """
    Strips all HTML tags from a given string.

    Args:
        html_string (str): The string containing HTML content.

    Returns:
        str: The string with all HTML tags removed.
    """

    soup = BeautifulSoup(html_string, "html.parser")

    return soup.get_text()


class DataDotGov:
    def __init__(self):
        pass

    def extract_metadata(self):
        metadata_urls = [
            "https://catalog.data.gov/harvest/object/203bed83-5da3-4a64-b156-ea016f277b07",
            "https://catalog.data.gov/harvest/object/04643a90-e5fd-4602-a8fa-e8195dd16c5e",
            "https://catalog.data.gov/harvest/object/abf916ec-6ddd-4030-8f5e-3b317a33ba1e",
            "https://catalog.data.gov/harvest/object/589436ca-1324-4773-9201-acecd5d83448",
            "https://catalog.data.gov/harvest/object/21392fa4-ff86-4ac8-9f38-33d67aef770c",
            "https://catalog.data.gov/harvest/object/9216c0ce-d083-48a6-b017-e0efc0fada37",
            "https://catalog.data.gov/harvest/object/0b20b4e4-34f8-4d1d-ae1c-7a405d0f6d36",
            "https://catalog.data.gov/harvest/object/36b9144a-dc24-43cf-85c3-49a08dbed762",
            "https://catalog.data.gov/harvest/object/9d60be08-5c3b-45a7-8ae6-017a4ca9433c",
            "https://catalog.data.gov/harvest/object/a4a75240-4fac-40f7-a327-6596becff636",
            "https://catalog.data.gov/harvest/object/8df82322-0812-46c7-b2b3-52829a8417e1",
            "https://catalog.data.gov/harvest/object/0419db56-01a4-4a97-a4f0-1fb903e77cdf",
            "https://catalog.data.gov/harvest/object/32d5b113-e83c-48f3-b05a-fd99ed7a3a92",
            "https://catalog.data.gov/harvest/object/f2e66a1c-10b6-4243-920a-0b64352b8c63",
            "https://catalog.data.gov/harvest/object/a0a63e30-b3cb-418b-8616-d89ee2e9e100",
        ]

        for url in metadata_urls:
            resp = requests.get(url)
            if resp.status_code == 200:
                resp_json = resp.json()
                title = strip_html(resp_json["title"])
                print(title)
                # description = strip_html(resp_json["description"])
                # modified = arrow.get(resp_json["modified"])
                # keywords = resp_json["keyword"]
                # print(title, description, keywords)


class FSGeodataClearningHouse:
    def __init__(self):
        self.edw_base_url = "https://data.fs.usda.gov/geodata/edw/"
        self.base_url = "https://data.fs.usda.gov/geodata/edw/datasets.php"
        self.metadata_xml_links = []

    def get_metadata_xml_links(self, base_url=None):
        """
        Retrieves a list of XML metadata file links from the specified base URL.

        Args:
            base_url (str, optional): The base URL to fetch the HTML content from.
                                      If not provided, the instance's base_url attribute is used.

        Returns:
            list: A list of URLs (strings) that point to XML metadata files.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the HTTP request.
        """

        url = base_url
        if base_url == None:
            url = self.base_url

        # Fetch the HTML content from the base URL
        response = requests.get(url)
        response.raise_for_status()  # TODO: Raise an exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all links that point to XML metadata files
        xml_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".xml"):
                self.metadata_xml_links.append(href)

    def extract_metadata_from_urls(self, limit=None):
        assets = []

        if self.metadata_xml_links:

            if limit:
                source_links = self.metadata_xml_links[0:limit]
            else:
                source_links = self.metadata_xml_links

            for link in source_links:
                url = f"{self.edw_base_url}{link}"
                resp = requests.get(url)

                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, features="xml")
                    title = strip_html(soup.find("title").get_text()).strip()
                    descr_block = soup.find("descript")
                    abstract = strip_html(descr_block.find("abstract").get_text()).strip()
                    asset = {"title": title, "description": abstract, "url": url}
                    assets.append(asset)

                    # descr_block = soup.find("descript")
                    # abstract = strip_html(descr_block.find("abstract").get_text())
                    # if abstract and len(abstract) > 0:
                    #     asset = {"title": title, "description": abstract, "url": url}
                    #     assets.append(asset)

        return assets

    def download_metadata_files(self):
        for link in self.metadata_xml_links:
            url = f"{self.edw_base_url}{link}"
            resp = requests.get(url)
            if resp.status_code == 200:
                filename = Path(f"./tmp/fsgeodata/{link.split("/")[-1]}")
                filename.parent.mkdir(exist_ok=True, parents=True)
                with open(filename, "wb") as file:
                    file.write(resp.content)

    def extract_metadata_from_local_xml(self):

        assets = []

        for l in self.metadata_xml_links:
            filename = f"./tmp/fsgeodata/{l.split('/')[-1]}"
            with open(filename, "r") as file:
                content = file.read()
                soup = BeautifulSoup(content, features="xml")
                title = strip_html(soup.find("title").get_text())
                descr_block = soup.find("descript")
                abstract = strip_html(descr_block.find("abstract").get_text())
                url = f"{self.edw_base_url}{l}"
                if abstract and len(abstract) > 0:
                        asset = {"title": title, "description": abstract, "url": url}
                        assets.append(asset)
        return assets


class ClimateRiskViewer:
    def __init__(self):
        pass

    def extract_metadata(self):
        pass
