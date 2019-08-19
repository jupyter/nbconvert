{%- macro celltags(cell) -%}
    {% if cell.metadata.tags | length > 0 %} data-cell-tags="{{ cell.metadata.tags | join(', ') }}"{% endif %}
{%- endmacro %}

