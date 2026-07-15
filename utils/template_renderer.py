from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(
    directory="templates"
)


def render_template(
    template_name: str,
    request: Request,
    **context
):
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context={**context}
    )