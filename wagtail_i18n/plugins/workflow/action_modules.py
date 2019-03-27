import functools

from django.template.loader import render_to_string

from wagtail.core import hooks


class BaseActionModule:
    template_name = None

    def __init__(self, request, translation_request):
        self.request = request
        self.translation_request = translation_request

    def render(self):
        context = {
            'translation_request': self.translation_request,
        }

        return render_to_string(self.template_name, context, request=self.request)


@functools.lru_cache()
def get_action_modules():
    action_modules = []

    for fn in hooks.get_hooks('wagtail_i18n_workflow_register_action_modules'):
        new_action_modules = fn()
        if new_action_modules:
            action_modules.extend(new_action_modules)

    print("HEY", action_modules)

    return action_modules
