{% set base_url      = 'https://cdnjs.cloudflare.com/ajax/libs/' %}

{% set mathjax_url   = base_url ~ 'mathjax/2.7.5/latest.js?config=TeX-AMS_HTML' %}
{% set requirejs_url = base_url ~ 'require.js/2.1.10/require.min.js' %}
{% set jquery_url    = base_url ~ 'jquery/2.0.3/jquery.min.js' %}

{% set urls          = { 'mathjax_url' : mathjax_url, 'requirejs_url' : requirejs_url, 'jquery_url' : jquery_url } %}