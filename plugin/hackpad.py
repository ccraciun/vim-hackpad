from requests_oauthlib import OAuth1Session


API_PATH = 'api/1.0'

CONTENT_TYPE_HEADER = 'Content-Type'
CONTENT_TYPE_MAP = {
        'txt': 'text/plain',
        'html': 'text/html',
        'md': 'text/x-web-markdown',
        }


def parse_url(url):
    if '//' not in url:
        url = '//' + url
    try:
        import urlparse
    except ImportError:
        import urllib.parse as urlparse
    return urlparse.urlparse(url)


def padid_from_path(path):
    return path.strip('/').split('-')[-1]


class HackpadSession(object):
    url = None
    parsed_url = None
    padid = None
    oauth_session = None
    api_endpoint = None
    debug = False

    def __init__(self, key, secret, url='https://hackpad.com', debug=False):
        self.debug = debug
        self.url = url
        self.parsed_url = parse_url(url)
        if self.parsed_url.path not in ('', '/'):
            self.padid = padid_from_path(self.parsed_url.path)
        self.oauth_session = OAuth1Session(key, secret)
        self.api_endpoint = "https://%s/%s" % (self.parsed_url.netloc, API_PATH)

    def get(self, url, *args, **kwargs):
        if self.debug or kwargs.get('debug'):
            print('GET', url, args, kwargs)
        return self.oauth_session.get(url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        if self.debug or kwargs.get('debug'):
            print('POST', url, args, kwargs)
        return self.oauth_session.post(url, *args, **kwargs)

    def pad_list(self):
        req_url = "%s/pads/all" % self.api_endpoint
        return self.get(req_url)

    def pad_search(self, query, start=None, limit=None):
        req_url = "%s/search" % self.api_endpoint
        req_params = {'q': query}
        if start:
            req_params['start'] = start
        if limit:
            req_params['limit'] = limit
        return self.get(req_url, params=req_params)

    def pad_edited_since(self, timestamp):
        req_url = "%s/edited-since/%d" % (self.api_endpoint, timestamp)
        return self.get(req_url)

    def pad_create(self, data, data_format='md'):
        req_url = "%s/pad/create" % self.api_endpoint
        req_headers = {CONTENT_TYPE_HEADER: CONTENT_TYPE_MAP[data_format]}
        return self.post(req_url, data, headers=req_headers)

    def pad_get(self, pad_id, data_format='md', revision='latest'):
        req_url = "%s/pad/%s/content/%s.%s" % (self.api_endpoint,
                                               pad_id, revision,
                                               data_format)
        return self.get(req_url)

    def pad_put(self, pad_id, data, data_format='md'):
        req_url = "%s/pad/%s/content" % (self.api_endpoint, pad_id)
        req_headers = {CONTENT_TYPE_HEADER: CONTENT_TYPE_MAP[data_format]}
        return self.post(req_url, data, headers=req_headers)

    def pad_revert(self, pad_id, revision):
        req_url = "%s/pad/%s/revert-to/%s" % (self.api_endpoint, pad_id, revision)
        return self.post(req_url)

    def pad_revisions(self, pad_id):
        req_url = "%s/pad/%s/revisions" % (self.api_endpoint, pad_id)
        return self.get(req_url)

    def pad_get_options(self, pad_id):
        req_url = "%s/pad/%s/options" % (self.api_endpoint, pad_id)
        return self.get(req_url)

    def pad_set_option(self, pad_id, setting, value):
        req_url = "%s/pad/%s/options" % (self.api_endpoint, pad_id)
        req_params = {setting: value}
        return self.post(req_url, params=req_params)

    def pad_revoke_access(self, pad_id, user):
        req_url = "%s/pad/%s/revoke-access/%s" % (self.api_endpoint, pad_id, user)
        return self.post(req_ulr)
