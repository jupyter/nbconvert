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

{# 
 ############################################
 # TODO: use "resources" to provide lab CSS #
 ############################################
 #}

{#
{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}
#}

<link rel="stylesheet" href="https://unpkg.com/font-awesome@4.5.0/css/font-awesome.min.css" type="text/css" />
<link rel="stylesheet" href="https://unpkg.com/@jupyterlab/cells@0.19.1/style/index.css" type="text/css" />
<link rel="stylesheet" href="https://unpkg.com/@jupyterlab/outputarea@0.19.1/style/index.css" type="text/css" />
<link rel="stylesheet" href="https://unpkg.com/@jupyterlab/notebook@1.0.0-alpha.7/style/index.css" type="text/css" />
<link rel="stylesheet" href="https://unpkg.com/@jupyterlab/codemirror@1.0.0-alpha.6/style/index.css" type="text/css" />
<link rel="stylesheet" href="https://unpkg.com/@jupyterlab/rendermime@1.0.0-alpha.6/style/index.css" type="text/css" />
<link rel="stylesheet" href="https://unpkg.com/@jupyterlab/theme-light-extension@1.0.0-alpha.7/style/index.css" type="text/css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pygments-css@1.0.0/default.css" type="text/css">

<style>
a.anchor-link {
  display: none;
}

.highlight  {
  margin: 0.4em;
}
</style>

{# 
 ####################################################
 # Generated pygments style using lab CSS variables #
 ####################################################
 #}

<style>
.highlight .hll { background-color: #ffffcc }
.highlight  { background: var(--jp-cell-editor-background); }
.highlight .c { color: var(--jp-mirror-editor-comment-color) } /* Comment */
.highlight .err { color: var(--jp-mirror-editor-error-color) } /* Error */
.highlight .k { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword */
.highlight .o { color: var(--jp-mirror-editor-operator-color) } /* Operator */
.highlight .ch { color: var(--jp-mirror-editor-comment-color) } /* Comment.Hashbang */
.highlight .cm { color: var(--jp-mirror-editor-comment-color) } /* Comment.Multiline */
.highlight .cp { color: var(--jp-mirror-editor-comment-color) } /* Comment.Preproc */
.highlight .cpf { color: var(--jp-mirror-editor-comment-color) } /* Comment.PreprocFile */
.highlight .c1 { color: var(--jp-mirror-editor-comment-color) } /* Comment.Single */
.highlight .cs { color: var(--jp-mirror-editor-comment-color) } /* Comment.Special */
.highlight .kc { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Pseudo */
.highlight .kr { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: var(--jp-mirror-editor-keyword-color); font-weight: bold } /* Keyword.Type */
.highlight .m { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number */
.highlight .s { color: var(--jp-mirror-editor-string-color) } /* Literal.String */
.highlight .ow { color: var(--jp-mirror-editor-operator-color) } /* Operator.Word */
.highlight .mb { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Bin */
.highlight .mf { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Float */
.highlight .mh { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Hex */
.highlight .mi { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Integer */
.highlight .mo { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Oct */
.highlight .sa { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Affix */
.highlight .sb { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Backtick */
.highlight .sc { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Char */
.highlight .dl { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Delimiter */
.highlight .sd { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Doc */
.highlight .s2 { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Double */
.highlight .se { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Escape */
.highlight .sh { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Heredoc */
.highlight .si { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Interpol */
.highlight .sx { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Other */
.highlight .sr { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Regex */
.highlight .s1 { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Single */
.highlight .ss { color: var(--jp-mirror-editor-string-color) } /* Literal.String.Symbol */
.highlight .il { color: var(--jp-mirror-editor-number-color); font-weight: bold } /* Literal.Number.Integer.Long */
</style>

<!-- Loading mathjax macro -->
{{ mathjax() }}
{%- endblock html_head -%}
</head>
{%- endblock header -%}

{% block body %}
<body>
  <div class="jp-Notebook" tabindex="-1">
{{ super() }}
  </div>
</body>
{%- endblock body %}

{% block footer %}
{{ super() }}
</html>
{% endblock footer %}
