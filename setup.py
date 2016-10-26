from setuptools import setup

setup(
    name='Reference Lookup Service',
    version='1.0beta1',
    long_description=__doc__,
    packages=['reflookup'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-wtf',
        'requests',
        'flask-restful',
        'gunicorn',
        'stop-words',
        'unidecode',
        'bs4',
        'rq',
        'redis',
        'invoke'
    ]
)
