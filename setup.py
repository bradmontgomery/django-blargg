from setuptools import setup
from blargg import __version__

setup(
    name='django-blargg',
    version=__version__,
    description="yet another blog app; this one aims to be fairly minimal",
    long_description=open('README.rst').read(),
    author='Brad Montgomery',
    author_email='brad@bradmontgomery.net',
    url='https://github.com/bradmontgomery/django-blargg',
    license='MIT',
    packages=['blargg'],
    include_package_data=True,
    package_data={
        '': ['README.rst'],
        'blargg': ['templates/blargg/*.html']
    },
    zip_safe=False,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
