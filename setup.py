from setuptools import setup
from blargg import __version__

setup(
    name='django-blargg',
    version=__version__,
    description="A minimal, admin-powered, django blogging app with a fun name.",
    long_description=open('README.md').read(),
    author='Brad Montgomery',
    author_email='brad@bradmontgomery.net',
    url='https://github.com/bradmontgomery/django-blargg',
    license='MIT',
    packages=['blargg'],
    include_package_data=True,
    package_data={
        '': ['README.md', 'LICENSE.txt', 'HISTORY.md'],
        'blargg': ['templates/blargg/*.html']
    },
    zip_safe=False,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
