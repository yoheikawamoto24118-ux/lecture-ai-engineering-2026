"""簡単な ask() の回帰テスト。"""

from app.ask import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    class FakeMetadata:
        prompt_token_count = 123
        response_token_count = 456

    class FakeResponse:
        text = "hello"
        usage_metadata = FakeMetadata()

    class FakeModels:
        def generate_content(self, model, contents):
            assert model == "gemini-3.5-flash-lite"
            assert contents == "question"
            return FakeResponse()

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr("app.ask.genai.Client", FakeClient)
    monkeypatch.setattr("app.ask.get_api_key", lambda: "fake-key")

    result = ask("question")
    captured = capsys.readouterr()

    assert result == "hello"
    assert "[入力トークン数] 123" in captured.out
    assert "[出力トークン数] 456" in captured.out
