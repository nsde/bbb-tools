import requests
import webbrowser

def getslides(url):
    """Returns valid URLs for all avaiable presentaion slides"""
    urls = []
    url_prefix = url.split("/svg/")[0]
    for slide in range(1, 100):
        url = url_prefix + "/svg/" + str(slide)
        if "200" in str(requests.get(url)):
            urls.append(url)
        else:
            return urls
    
if __name__ == "__main__":
    print(getslides("https://bbb.talpaworld.de/bigbluebutton/presentation/18941bfbd282e5bdf312fe4f33aa8fb5bee76f4f-1615483623193/18941bfbd282e5bdf312fe4f33aa8fb5bee76f4f-1615483623193/54df4f06e75a79796760c3c082d05eb12846bec3-1615483641373/svg/1"))