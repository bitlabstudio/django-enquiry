import os
from setuptools import setup, find_packages
import enquiry


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-enquiry",
    version=enquiry.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, poll, survey, enquiry, reusable, app',
    author='Daniel Kaufhold',
    author_email='daniel.kaufhold@bitmazk.com',
    url="https://github.com/bitmazk/django-enquiry",
    packages=find_packages(),
    include_package_data=True,
    tests_require=[
        'fabric',
        'factory_boy',
        'django-nose',
        'coverage',
        'django-coverage',
        'mock',
    ],
    test_suite='enquiry.tests.runtests.runtests',
)
