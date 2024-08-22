import os


def setup_django_typings():
    from django_stubs_ext import monkeypatch

    monkeypatch()


def setup_settings():
    """
    Load settings from environment variables.
    """
    _settings = os.getenv("SIMPLE_SETTINGS") or os.getenv("DJANGO_SETTINGS_MODULE")

    if _settings != "core.settings.test":
        from dotenv import load_dotenv

        load_dotenv()

        _settings = (
            os.getenv("SIMPLE_SETTINGS")
            or os.getenv("DJANGO_SETTINGS_MODULE")
            or "core.settings.development"
        )

    os.environ.setdefault("SIMPLE_SETTINGS", _settings)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", _settings)

    setup_django_typings()
