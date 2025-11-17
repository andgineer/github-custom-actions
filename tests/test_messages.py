def test_debug_message(action, capsys):
    action.debug("foo waz here")
    assert capsys.readouterr().out == "::debug::foo waz here\n"


def test_error_message(action, capsys):
    action.error_message("An error.", title="Error", file="test.txt", line=4)
    assert capsys.readouterr().out == "::error title=Error,file=test.txt,line=4::An error.\n"


def test_notice_message(action, capsys):
    action.notice_message("A notice.")
    assert capsys.readouterr().out == "::notice::A notice.\n"


def test_warning_message(action, capsys):
    action.warning_message("Warning!", file="test.txt")
    assert capsys.readouterr().out == "::warning file=test.txt::Warning!\n"
