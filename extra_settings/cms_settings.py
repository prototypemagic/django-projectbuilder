CMS_INSTALLED_APPS = (
    'cms',
    'menus',
    'sekizai',
    'tagging',
    'cms.plugins.file',
    'cms.plugins.flash',
    'cms.plugins.googlemap',
    'cms.plugins.link',
    'cms.plugins.picture',
    'cms.plugins.teaser',
    'cms.plugins.text',
    'cms.plugins.video', 
    'cms.plugins.twitter',
)

CMS_MIDDLE_CLASSES = (
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

CMS_TEMPLATES = (
    ('template.html', 'Main'),
)

CMS_MODERATOR = False
CMS_PERMISSION = True
