from graph.builder import route_by_risk


def test_route_low_risk():
    state = {"risk_level": 0}
    assert route_by_risk(state) == "normal_response"


def test_route_high_risk():
    state = {"risk_level": 2}
    assert route_by_risk(state) == "safe_response"