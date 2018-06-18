from requests_html import HTMLSession
import json


class InstagramGrabber:
    def __init__(self, username):
        self.username = username

    def getLinks(self):
        session = HTMLSession()
        r = session.get('https://instagram.com/' + self.username)
        l = r.html.find('body > script:nth-child(2)')[0].text
        json_str = l[21:]
        json_str = json_str[:-1]
        json_parsed = json.loads(json_str)
        shortcodes = []
        try:
            images = json_parsed['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
            for image in images:
                node = image['node']
                shortcode = node['shortcode']
                shortcodes.append(shortcode)
            links = []
            for sc in shortcodes:
                r = session.get('https://instagram.com/p/' + sc + '/?taken-by=' + self.username)
                img = r.html.find('head > meta[property="og:image"]')
                if len(img) > 0:
                    img = img[0]
                    links.append(img.attrs['content'])
            return links
        except:
            return []