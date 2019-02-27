{% set default_cdn = true %}

{%-if default_cdn %}
  {% set cdn1_url = 'https://cdnjs.cloudflare.com/ajax/libs/' %}

  {% set mathjax_url      = cdn1_url ~ 'mathjax/2.7.5/latest.js?config=TeX-AMS_HTML' %}
  {% set require_js_url   = cdn1_url ~ 'require.js/2.3.6/require.min.js' %}
  {% set jquery_url       = cdn1_url ~ 'jquery/3.3.1/jquery.min.js' %}
  {% set reveal_js        = cdn1_url ~ 'reveal.js/3.7.0/js/reveal.min.js' %}
  {% set font_awesome_url = cdn1_url ~ 'font-awesome/4.7.0/css/font-awesome.css' %}

{% else %}
  {% set libs_dir  = 'libs/' %}

  {% set mathjax_url      = libs_dir ~ 'mathjax/2.7.5/latest.js?config=TeX-AMS_HTML' %}
  {% set require_js_url   = libs_dir ~ 'require.min.js' %}
  {% set jquery_url       = libs_dir ~ 'jquery.min.js' %}
  {% set reveal_js        = libs_dir ~ 'reveal.min.js' %}
  {% set font_awesome_url = libs_dir ~ 'font-awesome.css' %}
  
{% endif %}

{% set urls           = { 
  'mathjax_url' : mathjax_url, 
  'require_js_url' : require_js_url, 
  'jquery_url' : jquery_url,
  'reveal_js' : reveal_js,
  'font_awesome_url' : font_awesome_url
  } %}