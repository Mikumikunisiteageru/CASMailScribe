# setup.py

import codecs
import setuptools

with codecs.open("README.md", "r", "utf-8") as fin:
	longdescription = fin.read()

setuptools.setup(
	name = "casmailscribe",
	version = "0.1.0",
	author = "Yu-Chang YANG",
	author_email = "yang.yc.allium@gmail.com",
	description = "A tool to dump CAS mailboxes",
	long_description = longdescription,
	long_description_content_type = "text/markdown",
	url = "https://github.com/Mikumikunisiteageru/CASMailScribe",
	packages = setuptools.find_packages(),
	install_requires = ["zmail", "selenium", "chromedriver_py"],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
