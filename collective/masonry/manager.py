from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.masonry.interfaces import IPortletManager

class PortletRenderer(ColumnPortletManagerRenderer):
    """
    A renderer for the content portlets
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, IPortletManager)
    template = ViewPageTemplateFile('templates/renderer.pt')
