# Create your views here.
from django.views.generic import TemplateView
from django.conf import settings
import os


class FrontendView(TemplateView):
    template_name = "index.html"

    def get_template_names(self):
        template_path = os.path.join(settings.FRONTEND_DIR, "index.html")
        if not os.path.exists(template_path):
            raise FileNotFoundError(
                f"The Vue frontend build files were not found at {settings.FRONTEND_DIR}. "
                "You may need to run 'yarn build' in the frontend directory."
            )
        return [template_path]
