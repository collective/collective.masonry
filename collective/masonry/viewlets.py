from zope import component
from zope import schema
from zope import interface
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.base import baseNormalize
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.form import AutoExtensibleForm
from z3c.form import form, button
from plone.z3cform import layout
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry


class RegistryVocabulary(object):
    """vocabulary to use with plone.app.registry"""
    interface.implements(IVocabularyFactory)

    def __init__(self, key):
        self.key = key
    def __call__(self, context):

        registry = component.queryUtility(IRegistry)
        if registry is None:
            return []
        categories = registry[self.key]
        terms = [SimpleTerm(baseNormalize(category),
                            baseNormalize(category),
                            category) for category in categories]
        return SimpleVocabulary(terms)


ModeVocabulary = RegistryVocabulary('collective.masonry.vocabulary.mode')


class IViewletConfiguration(interface.Interface):
    abovemode = schema.Choice(title=u"Above mode",
                         vocabulary="collective.masonry.vocabulary.mode")
    belowmode = schema.Choice(title=u"Below mode",
                         vocabulary="collective.masonry.vocabulary.mode")


class ViewletConfigurationForm(AutoExtensibleForm, form.EditForm):
    """Form to configure default view"""
    schema = IViewletConfiguration


class ViewletConfigurationFormView(layout.FormWrapper):
    form = ViewletConfigurationForm

class ViewletConfigurationAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(IViewletConfiguration)

    def __init__(self, context):
        self.context = context

    def get_abovemode(self):
        return getattr(self.context, 'masonryabovemode',
                       self.default_above_mode)
    def set_abovemode(self, value):
        setattr(self.context, 'masonryabovemode', value)
    abovemode = property(get_abovemode, set_abovemode)

    def get_belowmode(self):
        return getattr(self.context, 'masonrybelowmode',
                       self.default_above_mode)
    def set_belowmode(self, value):
        setattr(self.context, 'masonrybelowmode', value)
    belowmode = property(get_belowmode, set_belowmode)

    @property
    def default_above_mode(self):
        return 'Fixed width'


class PortletsAboveViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/portletsabovecontent.pt')

    def update(self):
        """
        Define everything we want to call in the template
        """
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        self.manageUrl =  '%s/@@manage-masonryportlets' % context_state.view_url()

        ## This is the way it's done in plone.app.portlets.manager, so we'll do the same
        mt = getToolByName(self.context, 'portal_membership')
        self.canManagePortlets = mt.checkPermission('Portlets: Manage portlets', self.context)
        self.config = IViewletConfiguration(self.context)

    def get_mode(self):
        return baseNormalize(self.config.abovemode).lower().replace(' ','-')

class PortletsBelowViewlet(PortletsAboveViewlet):
    render = ViewPageTemplateFile('templates/portletsbelowcontent.pt')

    def get_mode(self):
        return baseNormalize(self.config.belowmode).lower().replace(' ','-')
