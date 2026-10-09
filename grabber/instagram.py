from requests_html import HTMLSession
import json


class InstagramGrabber:
    def __init__(self, username):
        self.username = username

    def getLinks(self):
        try:
            session = HTMLSession()
            r = session.get('https://instagram.com/' + self.username)
            script_tags = r.html.find('script')
            shortcodes = []
            for s in script_tags:
                txt = s.text or ""
                if 'window._sharedData' in txt:
                    try:
                        json_str = txt.split('window._sharedData =', 1)[1].strip().rstrip(';')
                        json_parsed = json.loads(json_str)
                        images = json_parsed.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {}).get('edge_owner_to_timeline_media', {}).get('edges', [])
                        for image in images:
                            sc = image.get('node', {}).get('shortcode')
                            if sc:
                                shortcodes.append(sc)
                        break
                    except Exception:
                        pass

            links = []
            for sc in shortcodes:
                try:
                    r_post = session.get('https://instagram.com/p/' + sc + '/?taken-by=' + self.username)
                    img = r_post.html.find('meta[property="og:image"]')
                    if len(img) > 0:
                        content = img[0].attrs.get('content')
                        if content:
                            links.append(content)
                except Exception:
                    continue
            return links
        except Exception:
            return []