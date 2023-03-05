from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Financial and Insurance Industry',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='ptrFinance',
  version='0.0.17',
  description='Financial Web Scraping Library',
  #long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Rocco Pio Maria Petruccio',
  author_email='whatsappbackuprocco@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords=["Web Scraping", "Finance"],
  packages=find_packages(),
  install_requires=['bs4', "requests_html", "requests", "pandas"]
)
