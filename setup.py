import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = ["loguru"]

setup(name="threado",
      description="threado",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT",
      version="1.4",
      author="Alex Ng",
      author_email="alex_q_wu@qq.com",
      maintainer="Alex Ng",
      maintainer_email="alex_q_wu@qq.com",
      url="https://github.com/AlexNg9527/threado",
      packages=setuptools.find_packages(),
      install_requires=requires,
      classifiers=[
          'Programming Language :: Python :: 3',
      ])
