from unittest.mock import patch

import folium
import pandas as pd
import pytest

from autobahn.autobahn import (
    TrafficWarning,
    calculate_traffic_length,
    get_warnings,
    map_plot,
)


@pytest.fixture
def mock_response():
    return {
        "warning": [
            {
                "isBlocked": False,
                "display_type": "type1",
                "subtitle": "subtitle1",
                "title": "title1",
                "startTimestamp": "2023-01-01T00:00:00Z",
                "delayTimeValue": 10,
                "abnormalTrafficType": "typeA",
                "averageSpeed": 60,
                "description": "description1",
                "routeRecommendation": "route1",
                "lorryParkingFeatureIcons": ["icon1"],
                "geometry": {"coordinates": [[50.0, 8.0], [51.0, 9.0]]},
            }
        ]
    }


@patch("requests.get")
def test_get_warnings(mock_get, mock_response):
    mock_get.return_value.json.return_value = mock_response
    warnings = get_warnings("A1")
    assert warnings == mock_response["warning"]


def test_traffic_warning_initialization(mock_response):
    warning_data = mock_response["warning"][0]
    warning = TrafficWarning(warning_data)
    assert warning.isBlocked == warning_data["isBlocked"]
    assert warning.display_type == warning_data["display_type"]
    assert warning.subtitle == warning_data["subtitle"]
    assert warning.title == warning_data["title"]
    assert warning.startTimestamp == warning_data["startTimestamp"]
    assert warning.delayTimeValue == warning_data["delayTimeValue"]
    assert warning.abnormalTrafficType == warning_data["abnormalTrafficType"]
    assert warning.averageSpeed == warning_data["averageSpeed"]
    assert warning.description == warning_data["description"]
    assert warning.routeRecommendation == warning_data["routeRecommendation"]
    assert warning.lorryParkingFeatureIcons == warning_data["lorryParkingFeatureIcons"]
    pd.testing.assert_frame_equal(
        warning.geo_df, pd.DataFrame({"lat": [50.0, 51.0], "long": [8.0, 9.0]})
    )


def test_create_geo_dataframe(mock_response):
    warning_data = mock_response["warning"][0]
    warning = TrafficWarning(warning_data)
    expected_df = pd.DataFrame({"lat": [50.0, 51.0], "long": [8.0, 9.0]})
    actual_df = TrafficWarning.create_geo_dataframe(
        warning, warning_data["geometry"]["coordinates"]
    )
    pd.testing.assert_frame_equal(expected_df, actual_df)


def test_create_geo_dataframe_with_nan():
    coords = [[50.0, 8.0], [None, 9.0]]
    expected_df = pd.DataFrame({"lat": [50.0], "long": [8.0]})
    actual_df = TrafficWarning.create_geo_dataframe(expected_df, coords)
    pd.testing.assert_frame_equal(expected_df, actual_df)


def test_map_plot(mock_response):
    warning_data = mock_response["warning"][0]
    warning = TrafficWarning(warning_data)
    plotlist = [warning.geo_df]
    m = map_plot(plotlist, on="lat")
    assert isinstance(m, folium.Map)


def test_calculate_traffic_length():
    coordinates = pd.DataFrame({"lat": [10.0, 12.0], "long": [0.0, 0.0]})
    expected_length = 222.0
    actual_length = calculate_traffic_length(coordinates)
    assert abs(expected_length - actual_length) < 1.0  # Allow some tolerance
