from Products.CMFCore.utils import getToolByName

def cook_resources(context):
    """Refresh javascript and css"""
    jsregistry = getToolByName(context, 'portal_javascripts')

    jsregistry.cookResources()
