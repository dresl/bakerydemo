from django.templatetags.static import static
from django.utils.html import format_html

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.images.formats import Format, register_image_format

from bakerydemo.breads.models import Country, BreadIngredient, BreadType
from bakerydemo.base.models import People, FooterText

'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''


class BreadIngredientAdmin(ModelAdmin):
    # These stub classes allow us to put various models into the custom "Wagtail Bakery" menu item
    # rather than under the default Snippets section.
    model = BreadIngredient
    search_fields = ('name', )


class BreadTypeAdmin(ModelAdmin):
    model = BreadType
    search_fields = ('title', )


class BreadCountryAdmin(ModelAdmin):
    model = Country
    search_fields = ('title', )


class BreadModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bread Categories'
    menu_icon = 'fa-suitcase'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (BreadIngredientAdmin, BreadTypeAdmin, BreadCountryAdmin)


class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-users'  # change as required
    list_display = ('first_name', 'last_name', 'job_title', 'thumb_image')
    list_filter = ('job_title', )
    search_fields = ('first_name', 'last_name', 'job_title')


class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ('body',)


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bakery Misc'
    menu_icon = 'fa-cutlery'  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PeopleModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(BreadModelAdminGroup)
modeladmin_register(BakeryModelAdminGroup)


@hooks.register('register_rich_text_features')
def make_h1_default(features):
    features.default_features.append('h1')


@hooks.register("register_rich_text_features")
def register_code_styling(features):
    """Add the <code> to the richtext editor and page."""

    # Step 1
    feature_name = "code"
    type_ = "CODE"
    tag = "code"

    # Step 2
    control = {
        "type": type_,
        "label": "</>",
        "description": "Code"
    }

    # Step 3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    # Step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6. This is optional
    # This will register this feature with all richtext editors by default
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
    and is stored as HTML with a `<mark>` tag.
    """
    feature_name = 'mark'
    type_ = 'MARK'
    tag = 'mark'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': '☆',
        'description': 'Mark',
        # This isn’t even required – Draftail has predefined styles for MARK.
        # 'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('mark')


register_image_format(Format('thumbnail', 'Thumbnail', 'richtext-image thumbnail', 'max-120x120'))
