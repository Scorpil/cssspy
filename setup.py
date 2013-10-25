import codecs
from setuptools import setup
import cssspy


requirements = codecs.open('requirements.txt').readlines()

def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()

setup(
    name='cssspy',
    version=cssspy.__version__,
    description=cssspy.__doc__.strip(),
    long_description=long_description(),
    author=cssspy.__author__,
    author_email='webdev@scorpil.com',
    license=cssspy.__licence__,
    packages=['cssspy', 'cssspy.cssscrapy', 'cssspy.cssscrapy.spiders'],
    entry_points={
        'console_scripts': [
            'cssspy = cssspy.__main__:run',
        ],
    },
    install_requires=requirements,
    data_files=[
        ('cssspy', ['cssspy/scrapy.cfg']),
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
