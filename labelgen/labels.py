from django.template.loader import get_template


def render_label(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    return html