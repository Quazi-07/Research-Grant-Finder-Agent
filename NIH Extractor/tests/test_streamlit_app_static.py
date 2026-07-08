from pathlib import Path


def test_streamlit_app_avoids_session_state_items_attribute() -> None:
    app_text = Path("streamlit_app.py").read_text(encoding="utf-8")

    assert "st.session_state.items" not in app_text
    assert 'st.session_state["scored_items"]' in app_text


def test_streamlit_app_guards_against_callable_session_value() -> None:
    app_text = Path("streamlit_app.py").read_text(encoding="utf-8")

    assert "def get_scored_items_from_session" in app_text
    assert "callable(value)" in app_text
    assert 'del st.session_state["items"]' in app_text


def test_streamlit_score_bins_use_string_labels() -> None:
    app_text = Path("streamlit_app.py").read_text(encoding="utf-8")

    assert 'score_labels = ["0-25", "25-45", "45-70", "70-100"]' in app_text
    assert "labels=score_labels" in app_text
