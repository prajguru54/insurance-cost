import requests

def get_image(json_response = False):
    url = "https://api.unsplash.com/search/photos?page=1&query=money&client_id=y-GEU0v7yiAGWicJ_Hs1NtNagXj8RNT7inrSki0abOA"

    payload={}
    headers = {
    'Accept-Version': 'v1',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    # print(response.text)
    # print(response['results'][0]['urls']['regular'])
    image_url = response['results'][0]['urls']['small']
    download_url = response['results'][0]['links']['download']

    if json_response:
        return image_url
    print(download_url)




if __name__ == '__main__':
    get_image()