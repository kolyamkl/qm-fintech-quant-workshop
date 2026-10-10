import matplotlib

matplotlib.use("Agg")  # draw charts without opening windows

import pandas as pd
import pytest


@pytest.fixture
def make_prices():
    """Build a tiny price DataFrame (business days from 2024-01-01) from a list of closes."""

    def _make(closes):
        index = pd.bdate_range("2024-01-01", periods=len(closes), name="Date")
        return pd.DataFrame({"Close": [float(c) for c in closes]}, index=index)

    return _make
