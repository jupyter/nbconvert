{% set cdn1_url = 'https://cdnjs.cloudflare.com/ajax/libs/' %}
{# set cdn2_url = 'https://cdn.jsdelivr.net/npm/' #}

{% set mathjax_url      = cdn1_url ~ 'mathjax/2.7.5/latest.js?config=TeX-AMS_HTML' %}
{# set mathjax_url      = cdn2_url ~ 'mathjax@2.7.5/unpacked/MathJax.min.js' #}
{% set require_js_url   = cdn1_url ~ 'require.js/2.3.6/require.min.js' %}
{# set require_js_url   = 'https://requirejs.org/docs/release/2.3.6/minified/require.js' #}
{% set jquery_url       = cdn1_url ~ 'jquery/3.3.1/jquery.min.js' %}
{# set jquery_url       = cdn2_url ~ 'jquery@3.3.1/dist/jquery.min.js' #}
{% set reveal_js        = cdn1_url ~ 'reveal.js/3.7.0/js/reveal.min.js' %}
{# set reveal_js        = cdn2_url ~ 'reveal.js@3.7.0/js/reveal.min.js' #}
{% set font_awesome_url = cdn1_url ~ 'font-awesome/4.7.0/css/font-awesome.css' %}
{# set font_awesome_url = 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css' #}

{% set urls           = { 
  'mathjax_url' : mathjax_url, 
  'require_js_url' : require_js_url, 
  'jquery_url' : jquery_url,
  'reveal_js' : reveal_js,
  'font_awesome_url' : font_awesome_url
  } %}