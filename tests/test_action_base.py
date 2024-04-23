

def test_action_base_summary(action):
    action.summary = "test"
    action.summary += "1"
    assert action.env.github_step_summary.read_text() == "test1"
