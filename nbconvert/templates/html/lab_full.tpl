{%- extends 'lab_basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{%- block header -%}
<!DOCTYPE html>
<html>
<head>
{%- block html_head -%}
<meta charset="utf-8" />
{% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
<title>{{nb_title}}</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

{% block ipywidgets %}
{%- if "widgets" in nb.metadata -%}
<script>
(function() {
  function addWidgetsRenderer() {
    var mimeElement = document.querySelector('script[type="application/vnd.jupyter.widget-view+json"]');
    var scriptElement = document.createElement('script');
    var widgetRendererSrc = '{{ resources.ipywidgets_base_url }}@jupyter-widgets/html-manager@*/dist/embed-amd.js';
    var widgetState;

    // Fallback for older version:
    try {
      widgetState = mimeElement && JSON.parse(mimeElement.innerHTML);

      if (widgetState && (widgetState.version_major < 2 || !widgetState.version_major)) {
        widgetRendererSrc = '{{ resources.ipywidgets_base_url }}jupyter-js-widgets@*/dist/embed.js';
      }
    } catch(e) {}

    scriptElement.src = widgetRendererSrc;
    document.body.appendChild(scriptElement);
  }

  document.addEventListener('DOMContentLoaded', addWidgetsRenderer);
}());
</script>
{%- endif -%}
{% endblock ipywidgets %}

{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<style>
a.anchor-link {
  display: none;
}

.highlight  {
  margin: 0.4em;
}
</style>

<!-- Loading mathjax macro -->
{{ mathjax() }}
{%- endblock html_head -%}
</head>
{%- endblock header -%}

{% block body %}
<body class="jp-Notebook">
{{ super() }}
</body>
{%- endblock body %}

{% block footer %}
{{ super() }}
</html>
{% endblock footer %}
