class TemplateRequest(object):
    def __init__(self, **kwargs):
        self.width = int(kwargs["width"])
        self.height = int(kwargs["height"])
        self.dpi = int(kwargs["dpi"])
        self.format = kwargs["format"]


def parse_template_request(request):
    return TemplateRequest(**request)
