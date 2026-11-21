"""Tests for the widget-aware data type filter."""

from nbconvert.filters.widgetsdatatypefilter import (
    WIDGET_STATE_MIMETYPE,
    WIDGET_VIEW_MIMETYPE,
    WidgetsDataTypeFilter,
)


def test_widget_metadata_without_state_falls_back_to_plain_text():
    """Missing widget state should behave like unavailable widget state."""
    filter_ = WidgetsDataTypeFilter(
        notebook_metadata={
            "": {
                "widgets": {
                    WIDGET_STATE_MIMETYPE: {
                        "version_major": 2,
                        "version_minor": 0,
                    }
                }
            }
        }
    )
    filter_.display_data_priority = [WIDGET_VIEW_MIMETYPE, "text/plain"]

    assert filter_(
        {
            WIDGET_VIEW_MIMETYPE: {"model_id": "missing-widget-model"},
            "text/plain": "widget fallback",
        }
    ) == ["text/plain"]


def test_widget_metadata_with_matching_state_prefers_widget_view():
    """Available widget state should still allow the widget view mimetype."""
    filter_ = WidgetsDataTypeFilter(
        notebook_metadata={
            "": {
                "widgets": {
                    WIDGET_STATE_MIMETYPE: {
                        "state": {
                            "available-widget-model": {},
                        },
                    }
                }
            }
        }
    )
    filter_.display_data_priority = [WIDGET_VIEW_MIMETYPE, "text/plain"]

    assert filter_(
        {
            WIDGET_VIEW_MIMETYPE: {"model_id": "available-widget-model"},
            "text/plain": "widget fallback",
        }
    ) == [WIDGET_VIEW_MIMETYPE]
