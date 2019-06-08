from jupyter_core.utils import ensure_dir_exists
from ..exporters import TemplateExporter, HTMLExporter, LatexExporter

def ensure_template_dirs_exist():
    for exporter in [TemplateExporter(), HTMLExporter(), LatexExporter()]:
        for path in [*exporter.template_data_paths, exporter.user_config_template_path]:
                ensure_dir_exists(path, mode=0o700)
