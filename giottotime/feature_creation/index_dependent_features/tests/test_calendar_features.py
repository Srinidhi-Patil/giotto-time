import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings

from giottotime.feature_creation import CalendarFeature
from giottotime.utils.hypothesis.time_indexes import giotto_time_series


def test_unevenly_spaced_time_series():
    unevenly_spaced_ts = pd.DataFrame(
        index=[
            pd.Period("2012-01-01"),
            pd.Period("2012-01-03"),
            pd.Period("2012-01-10"),
        ]
    )
    cal_feature = CalendarFeature(
        start_date="ignored",
        end_date="ignored",
        region="america",
        country="Brazil",
        kernel=np.array([0, 1]),
        output_name="cal",
        return_name_event=True,
    )

    with pytest.raises(ValueError):
        cal_feature.transform(unevenly_spaced_ts)


@settings(deadline=pd.Timedelta(milliseconds=300), max_examples=10)
@given(giotto_time_series(min_length=2))
def test_correct_index_random_ts(ts):
    cal_feature = CalendarFeature(
        start_date="ignored",
        end_date="ignored",
        region="america",
        country="Brazil",
        kernel=np.array([]),
        output_name="cal",
        return_name_event=False,
    )
    Xt = cal_feature.transform(ts)
    np.testing.assert_array_equal(Xt.index, ts.index)


def test_calendar_transform_with_x_no_names():
    ts = pd.DataFrame(
        index=[
            pd.Period("2012-01-01"),
            pd.Period("2012-01-02"),
            pd.Period("2012-01-03"),
        ]
    )

    cal_feature = CalendarFeature(
        start_date="ignored",
        end_date="ignored",
        region="america",
        country="Brazil",
        kernel=np.array([]),
        output_name="cal",
        return_name_event=False,
    )
    Xt = cal_feature.transform(ts)
    print(Xt)
