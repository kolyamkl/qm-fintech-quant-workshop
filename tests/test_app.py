from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app" / "streamlit_app.py")


def run_app():
    return AppTest.from_file(APP, default_timeout=60).run()


def test_app_runs_with_defaults():
    at = run_app()
    assert not at.exception
    assert len(at.metric) == 4


def test_fast_not_below_slow_shows_warning():
    at = run_app()
    at.sidebar.slider[0].set_value(100)
    at.sidebar.slider[1].set_value(50)
    at.run()
    assert not at.exception
    assert len(at.warning) == 1
    assert len(at.metric) == 0


def test_rsi_strategy_runs():
    at = run_app()
    at.sidebar.radio[0].set_value("RSI mean reversion").run()
    assert not at.exception
    assert len(at.metric) == 4


def test_one_day_range_shows_warning():
    at = run_app()
    last_day = at.sidebar.date_input[0].value[1]
    at.sidebar.date_input[0].set_value((last_day, last_day)).run()
    assert not at.exception
    assert len(at.warning) == 1
