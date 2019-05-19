from jupyter_core.utils import ensure_dir_exists
from ..exporters import TemplateExporter, HTMLExporter, LatexExporter

def ensure_user_template_dir_exists():
    for exporter in [TemplateExporter, HTMLExporter, LatexExporter]:
        path = exporter().user_config_template_path
        ensure_dir_exists(path, mode=0o700)
