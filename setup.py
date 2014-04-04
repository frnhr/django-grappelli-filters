import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-grappelli-filters',
    version='0.2.1',
    packages=['grappelli_filters'],
    include_package_data=True,
    install_requires=['django', 'django-grappelli', ],
    license='Unlicense',
    description='Additional filters for Djagno Grappelli admin',
    long_description=README,
    url='https://github.com/frnhr/django-grappelli-filters/',
    author='Fran Hrzenjak',
    author_email='fran@changeset.hr',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
