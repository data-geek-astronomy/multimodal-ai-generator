from src.utils.helpers import make_run_dir, slugify


def test_slugify():
    assert slugify("A Beautiful Sunset!") == "a-beautiful-sunset"


def test_make_run_dir_creates_directory(tmp_path):
    run_dir = make_run_dir(str(tmp_path), "A test prompt")
    assert run_dir.exists()
    assert run_dir.is_dir()
