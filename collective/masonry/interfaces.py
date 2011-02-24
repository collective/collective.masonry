from zope import interface
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

class IMasonryLayer(interface.Interface):
    """
    A layer specific to this product. Is registered using browserlayer.xml
    """

class IPortletManager(IPortletManager, IColumn):
    """
    Superclass used by our adapter
    The IColumn bit means that we can add all the portlets available to 
     the right-hand and left-hand column portlet managers
    """
    
class IPortletsAboveContent(IPortletManager):
     """
     For the portlet manager above the content area.
     """

class IPortletsBelowContent(IPortletManager):
     """
     For the portlet manager below the content area.
     """
