import os.path
import shutil
import random
import pytest

from blog.engine import BlogEngine


@pytest.fixture
def engine():
	root_path = os.path.dirname(__file__)
	return BlogEngine(root_path, 'test', '//localhost')


def test_add_posts(engine):
	engine.add_posts()
