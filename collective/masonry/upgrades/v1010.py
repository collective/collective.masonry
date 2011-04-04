def upgrade_1000_to_1010(context):
    """Add jquery.imagesloaded to jsregistry"""
    context.runImportStepFromProfile('profile-collective.masonry:default', 'jsregistry')
