This documentation is written in **RST (ReStructuredText)** format and can be built into web pages 
using Sphinx rendered with an HTML theme (sphinx-rtd-theme). The HTML pages are then hosted using
GitHub Pages service.

The pages are hosted @ https://universalpayload.github.io/documentation/

Getting Started

In order to build the web site content from the source code, install **additional** python packages:

**pip install sphinx docutils sphinx-rtd-theme sphinxcontrib-websupport**


To make html:

**make html**

The generated HTML file is located in 'build'.


Submit changes (for contributors)
Follow the github workflow to submit your pull request.

Travis-CI is used to build the html files and the html files are pushed into a
gh-pages branch which is then rendered by GitHub Pages.

