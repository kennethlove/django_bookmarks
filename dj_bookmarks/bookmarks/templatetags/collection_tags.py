from django import template

register = template.Library()


@register.inclusion_tag('bookmarks/_tags/collections_modal.html', takes_context=True)
def collections_modal(context):
    user = context.get('user')
    return {'collections': user.collections.all()}