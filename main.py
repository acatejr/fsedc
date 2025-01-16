import requests
from bs4 import BeautifulSoup


class FSGeodataClearningHouse():
    
    def __init__(self):
        self.edw_base_url = "https://data.fs.usda.gov/geodata/edw/"        
        self.base_url = "https://data.fs.usda.gov/geodata/edw/datasets.php"
        self.metadata_xml_links = []

    def strip_html(self, html_string):
        """
        Strips all HTML tags from a given string.

        Args:
            html_string (str): The string containing HTML content.

        Returns:
            str: The string with all HTML tags removed.
        """
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup.get_text()


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
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links that point to XML metadata files
        xml_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.xml'):
                self.metadata_xml_links.append(href)

    def extract_metadata(self):
        
        if self.metadata_xml_links:
            for link in self.metadata_xml_links:
                url = f"{self.edw_base_url}{link}"
                resp = requests.get(url)
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, features="xml")
                    title = self.strip_html(soup.find("title").get_text())
                    desc_block = soup.find("descript")
                    abstract = self.strip_html(desc_block.find("abstract").get_text())
                    print(abstract, "\n")
                    

# Example usage
if __name__ == "__main__":
    fs_geodata_clearinghouse = FSGeodataClearningHouse()
    fs_geodata_clearinghouse.get_metadata_xml_links()
    fs_geodata_clearinghouse.extract_metadata()

    # xml_links = fs_geodata_clearinghouse.metadata_xml_links

    # print(f"{len(xml_links)} links collected from FS Geodata Clearinghouse.")
    # for l in xml_links[:5]:
    #     print(l)

"""
edw_resources/meta/S_USA.Activity_RngVegImprove.xml
edw_resources/meta/S_USA.Activity_SilvTSI.xml
edw_resources/meta/S_USA.Activity_SilvReforestation.xml
edw_resources/meta/S_USA.Activity_HazFuelTrt_LN.xml
edw_resources/meta/S_USA.Activity_HazFuelTrt_PL.xml
"""