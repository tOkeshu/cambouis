from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

classifiers = ["Programming Language :: Python",
               "License :: OSI Approved :: Apache Software License",
               "Development Status :: 4 - Beta"]


setup(name='cambouis',
      version='0.0.1',
      url='https://github.com/tOkeshu/cambouis',
      packages=find_packages(),
      scripts=['bin/lecambouis'],
      long_description=README,
      description="An IRC bot for La Quadrature Du Net",
      author="Romain Gauthier",
      author_email="romain.gauthier@monkeypatch.me",
      include_package_data=True,
      classifiers=classifiers)
