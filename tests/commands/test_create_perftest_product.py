"""
Tests for management command to create perftest database.

"""

from django.core.management import call_command
from datazilla.model import PerformanceTestModel



def call_create_perftest_project(*args, **kwargs):
    call_command("create_perftest_project", *args, **kwargs)


def test_no_args(capsys):
    """Shows need for a project name."""
    try:
        call_create_perftest_project()
        raise Exception("Should have gotten a SystemExit")

    except SystemExit:
        exp = (
            "",
            "Error: You must supply a project name to create: --project project\n",
            )

        assert capsys.readouterr() == exp


def test_successful_create(capsys, monkeypatch):
    """Successful create call on pushlog database."""

    calls = []
    @classmethod
    def mock_create(justme, project, hosts, types, cron_batch):
        class MyFoo(object):
            def disconnect(self):
                pass
        calls.append((project, hosts, types, cron_batch))
        return MyFoo()
    monkeypatch.setattr(PerformanceTestModel, "create", mock_create)

    call_create_perftest_project(
        project="spam",
        perftest_host="pth",
        objectstore_host="osh",
        perftest_type="ptt",
        objectstore_type="ost",
        cron_batch="small",
        )

    exp = (
        "Perftest project created: spam\n",
        "",
        )
    assert capsys.readouterr() == exp
    assert calls == [(
        "spam",
        {"perftest": "pth", "objectstore": "osh"},
        {"perftest": "ptt", "objectstore": "ost"},
        "small"
        )]
