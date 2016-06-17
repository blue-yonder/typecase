from __future__ import absolute_import
from setuptools import setup, find_packages
import os.path
import inspect


__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def read(filepath):
    with open(os.path.join(__location__, filepath)) as f:
        return f.read()


if __name__ == "__main__":
    setup(name="typecase",
          description="Library providing algebraic datatypes for Python",
          license="new-bsd",
          author="Holger Peters",
          packages=find_packages(exclude=["tests", "test*"]),
          author_email="holger.peters@blue-yonder.com",
          long_description=read('README.rst'),
          classifiers=["Development Status :: 2 - Pre-Alpha"],)
