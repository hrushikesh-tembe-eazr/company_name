from flask import Flask
import http.client
import zlib
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Vercel!"


@app.route('/company_number/<companyname>', methods=['GET'])
def call_zaubacorp(companyname):
    try:
        # print('SSSSSSSSSSSSS',companyname)
        host = "www.zaubacorp.com"

        companyname = companyname.replace(" ", "-")

        endpoint = f"/companysearchresults/{companyname}"

        # Create an HTTP connection
        conn = http.client.HTTPSConnection(host)

        # Define headers (mimic Postman)
        headers = {
            "Host": host,
            # "User-Agent": "PostmanRuntime/7.43.0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",  # Accept compressed responses
            "Connection": "keep-alive",
        }

        # Make the GET request
        conn.request("GET", endpoint, headers=headers)

        # Get the response
        response = conn.getresponse()

        # Check response status
        if response.status == 200:
            print("Request successful!")

            # Read the raw response data
            raw_data = response.read()

            # Handle Content-Encoding (gzip, deflate, br)
            encoding = response.getheader("Content-Encoding")
            if encoding == "gzip":
                raw_data = zlib.decompress(raw_data, zlib.MAX_WBITS | 16)
            elif encoding == "deflate":
                raw_data = zlib.decompress(raw_data)
            elif encoding == "br":
                import brotli
                raw_data = brotli.decompress(raw_data)

            # Detect character encoding from Content-Type
            content_type = response.getheader("Content-Type")
            if content_type and "charset=" in content_type:
                char_encoding = content_type.split("charset=")[-1]
            else:
                char_encoding = "ISO-8859-1"  # Fallback encoding

            # Decode the response data
            try:
                decoded_data = raw_data.decode(char_encoding)
                # Sample HTML string (replace with the actual HTML content)
                html_content = decoded_data
                
                # Parse the HTML
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Locate the table by its id
                table = soup.find("table", {"id": "results"})
                
                # Check if the table exists
                if table:
                    # Extract table rows
                    rows = table.find_all("tr")
                
                    # Extract table header (optional)
                    headers = [header.get_text(strip=True) for header in rows[0].find_all("th")]
                    # print("Table Headers:", headers)
                
                    # Extract table data
                    table_data = []
                    for row in rows[1:]:  # Skip the header row
                        cells = row.find_all("td")
                        data = [cell.get_text(strip=True) for cell in cells]
                        table_data.append(data)
                
                    json_data = [dict(zip(headers, row)) for row in table_data]
                
                    for entry in json_data:
                        if "Address" in entry:
                            del entry["Address"]
                
                    # print(json_data)
                else:
                    print("Table with id 'results' not found.")
                
                return json_data
            except UnicodeDecodeError:
                print("Failed to decode the response data. Using replacement strategy.")
                decoded_data = raw_data.decode(char_encoding, errors="replace")
                html_content = decoded_data
                
                # Parse the HTML
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Locate the table by its id
                table = soup.find("table", {"id": "results"})
                
                # Check if the table exists
                if table:
                    # Extract table rows
                    rows = table.find_all("tr")
                
                    # Extract table header (optional)
                    headers = [header.get_text(strip=True) for header in rows[0].find_all("th")]
                    # print("Table Headers:", headers)
                
                    # Extract table data
                    table_data = []
                    for row in rows[1:]:  # Skip the header row
                        cells = row.find_all("td")
                        data = [cell.get_text(strip=True) for cell in cells]
                        table_data.append(data)
                
                    json_data = [dict(zip(headers, row)) for row in table_data]
                
                    for entry in json_data:
                        if "Address" in entry:
                            del entry["Address"]
                
                    # print(json_data)
                else:
                    print("Table with id 'results' not found.")
                
                return json_data
                
                # print(decoded_data)
                # return decoded_data
        else:
            print(f"Request failed with status {response.status}")
            return {"status":response.status}
    except:
        return None

if __name__ == '__main__':
    app.run()
