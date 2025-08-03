import sys
import types


def test_predict_logs_and_returns_sum(monkeypatch):
    logs = []

    class DummyLogger:
        def session(self):
            class Session:
                def __enter__(self_inner):
                    return self_inner
                def __exit__(self_inner, exc_type, exc, tb):
                    pass
                def log(self_inner, data):
                    logs.append(data)
            return Session()

    dummy_why = types.SimpleNamespace(logger=lambda **kwargs: DummyLogger())
    monkeypatch.setitem(sys.modules, 'whylogs', dummy_why)

    import importlib
    serve = importlib.import_module('serving.serve')

    result = serve.predict([1, 2, 3])
    assert result == 6
    assert logs[0]['prediction'] == 6
    assert logs[0]['features'] == [1, 2, 3]
