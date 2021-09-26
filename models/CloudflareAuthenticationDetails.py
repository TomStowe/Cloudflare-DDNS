"""
    A class defining the Cloudflare authentication details
"""
class CloudflareAuthenticationDetails:
    token = ""
    key = ""
    email = ""

    """
        The constructor for the CloudflareAuthenticationDetails
    """
    def __init__(self, token="", key="", email=""):
        self.token = token
        self.key = key
        self.email = email