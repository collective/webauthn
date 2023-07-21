from AccessControl.SecurityInfo import ClassSecurityInfo
from App.config import getConfiguration
from BTrees.OOBTree import OOBTree
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

import os
import json

KEY = "__plone_webauthn"

from .key_data import IKeyData


prefix = os.path.basename(getConfiguration().clienthome)


manage_addWebauthnPluginForm = PageTemplateFile(
    "www/Add", globals(), __name__="manage_addWebauthnPluginForm"
)


def manage_addWebauthnPlugin(self, id, title="", REQUEST=None):
    """Add a WebauthnPlugin to a Pluggable Authentication Service."""
    c = WebauthnPlugin(id, title)
    self._setObject(c.getId(), c)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace"
            "?manage_tabs_message="
            "Webauthn+Plugin+added." % self.absolute_url()
        )


class WebauthnPlugin(BasePlugin, Cacheable):
    """Work with extended Onkopedia login credentials and login data service"""

    meta_type = "Webauthn plugin"
    login_path = "login_form"
    security = ClassSecurityInfo()

    manage_options = BasePlugin.manage_options + Cacheable.manage_options

    _properties = ({"id": "title", "label": "Title", "type": "string", "mode": "w"},)

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title
        annos = self.annotations # ensure that OOBTree is initialized properly

    @property
    def annotations(self):
        annotations = getattr(self, KEY, None)
        if annotations is None:
            setattr(self, KEY, OOBTree())
            annotations = getattr(self, KEY)
        return annotations

    security.declarePrivate("extractCredentials")
    def extractCredentials(self, request):

        return {"login": "ajung", "password": request.BODY}

    security.declarePrivate("authenticateCredentials")
    def authenticateCredentials(self, credentials):
        """Find out if the login and password is correct"""

        # function local import for avoid circular import
        
        data = json.loads(credentials["password"].decode('utf-8'))

        user_id = data["user_id"]
        cname = data["cname"]

        print(user_id, cname)


        return ("pthota", "pthota")


classImplements(
    WebauthnPlugin,
    IAuthenticationPlugin,
    IExtractionPlugin,
)
