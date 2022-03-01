import pytest
from taipy.gui import Gui, Markdown
import pathlib
import logging


def test_donwload_file(gui: Gui, helpers):
    def do_something(state, id):
        gui.download((pathlib.Path(__file__).parent.parent.parent / "resources" / "taipan.jpg"))

    # Bind a page so that the function will be called
    # gui.add_page(
    #     "test", Markdown("<|Do something!|button|on_action=do_something|id=my_button|>")
    # )
    gui.run(run_server=False)
    # WS client and emit
    ws_client = gui._server._ws.test_client(gui._server.get_flask())
    # Get the jsx once so that the page will be evaluated -> variable will be registered
    sid = helpers.create_scope_and_get_sid(gui)
    ws_client.emit("message", {"client_id": sid, "type": "A", "name": "my_button", "payload": "do_something"})
    # assert for received message (message that would be sent to the frontend client)
    received_messages = ws_client.get_received()
    assert len(received_messages) == 1
    assert isinstance(received_messages[0], dict)
    assert "name" in received_messages[0] and received_messages[0]["name"] == "message"
    assert "args" in received_messages[0]
    args = received_messages[0]["args"]
    assert "type" in args and args["type"] == "DF"
    assert "content" in args and args["content"] == "/taipy-content/taipyStatic0/taipan.jpg"
    logging.getLogger().debug(args["content"])
