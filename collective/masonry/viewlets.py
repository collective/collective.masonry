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
from persistent.dict import PersistentDict

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

    columnWidth = schema.Int(title=u"columnWidth", required=False)
    gutterWidth = schema.Int(title=u"gutterWidth", default=10)
    isFitWidth = schema.Bool(title=u"isFitWidth", default=False)
    isResizable = schema.Bool(title=u"isResizable", default=True)


class ViewletConfigurationForm(AutoExtensibleForm, form.EditForm):
    """Form to configure default view"""
    schema = IViewletConfiguration

    def applyChanges(self, data):
        super(ViewletConfigurationForm, self).applyChanges(data)
        url = self.context.absolute_url()
        self.request.response.redirect('%s/@@manage-portlets' % url)

class ViewletConfigurationFormView(layout.FormWrapper):
    form = ViewletConfigurationForm

class ViewletConfigurationAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(IViewletConfiguration)

    def __init__(self, context):
        self.context = context
        self._configuration = None
        self._default_mode = None

    @property
    def configuration(self):
        if self._configuration is None:
            #get on context
            self._configuration = getattr(self.context, 'masonry_configuration',
                                          None)
        if self._configuration is None:
            #load default
            config = {}
            config["gutterWidth"] = 10
            config["isFitWidth"] = False
            config["isResizable"] = True
            self._configuration = config

        return self._configuration

    def get_storage(self):
        storage = getattr(self.context, 'masonry_configuration', None)
        if storage is None:
            self.context.masonry_configuration = PersistentDict()
            #loads default
            config = self.context.masonry_configuration
            config["gutterWidth"] = 10
            config["isFitWidth"] = False
            config["isResizable"] = True
        return self.context.masonry_configuration

    def get_columnWidth(self):
        return self.configuration.get('columnWidth', None)
    def set_columnWidth(self, value):
        if value:
            self.get_storage()['columnWidth'] = value
    columnWidth = property(get_columnWidth, set_columnWidth)

    def get_gutterWidth(self):
        return self.configuration.get('gutterWidth', 10)
    def set_gutterWidth(self, value):
        self.get_storage()['gutterWidth'] = value
    gutterWidth = property(get_gutterWidth, set_gutterWidth)

    def get_isFitWidth(self):
        return self.configuration.get('isFitWidth', False)
    def set_isFitWidth(self, value):
        self.get_storage()['isFitWidth'] = value
    isFitWidth = property(get_isFitWidth, set_isFitWidth)

    def get_isResizable(self):
        return self.configuration.get('isResizable', True)
    def set_isResizable(self, value):
        self.get_storage()['isResizable'] = value
    isResizable = property(get_isResizable, set_isResizable)

    def get_abovemode(self):
        return getattr(self.context, 'masonryabovemode',
                       self.default_mode)
    def set_abovemode(self, value):
        setattr(self.context, 'masonryabovemode', value)
    abovemode = property(get_abovemode, set_abovemode)

    def get_belowmode(self):
        return getattr(self.context, 'masonrybelowmode',
                       self.default_mode)
    def set_belowmode(self, value):
        setattr(self.context, 'masonrybelowmode', value)
    belowmode = property(get_belowmode, set_belowmode)

    @property
    def default_mode(self):
        if not self._default_mode:
            registry = component.getUtility(IRegistry)
            self._default_mode = registry.get('collective.masonry.defaultmode',
                                             'fixed-width-220')
        return self._default_mode

    def masonry_configuration(self):
        config = "{"
        for key in self.configuration:
            config+="%s: %s," % (key, self.configuration[key])
        config+="itemSelector:'.portlet'}"
        config = config.replace('True', 'true').replace('False', 'false')
        return """<script type="text/javascript">var masonry_configuration = %s</script>""" % config


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
