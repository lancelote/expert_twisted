from setuptools import setup, find_packages

setup(
    name='feed_aggregation',
    install_requires=['feedparser', 'Klein', 'Twisted', 'treq', 'lxml', 'attrs', 'hyperlink'],
    package_dir={'': 'src'},
    packages=find_packages('src') + ['twisted.plugins'],
)
