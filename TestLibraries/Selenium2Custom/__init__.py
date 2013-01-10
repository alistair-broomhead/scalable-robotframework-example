"""
Wrapper adding missing functionality for Selenium2
"""
#TODO check what of this is obselete
from selenium.common.exceptions import WebDriverException
from robot.api import logger

__author__ = 'Alistair Broomhead'
from Selenium2Library import Selenium2Library

class Selenium2Custom(Selenium2Library):
    """
    Custom wrapper for robotframework Selenium2Library to add extra functionality
    """
    def get_text(self, locator):
        """
        Returns the text of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._get_text(locator)
    def get_html(self, id=None):
        """
        Get the current document as an XML accessor object.
        """
        from lxml import html
        src = self.get_source().encode('ascii', 'xmlcharrefreplace')
        page = html.fromstring(src)
        element = page.get_element_by_id(id) if id is not None else page
        return html.tostring(element)
    def close_all_browsers(self):
        """Closes all open browsers and resets the browser cache.

        After this keyword new indexes returned from `Open Browser` keyword
        are reset to 1.

        This keyword should be used in test or suite teardown to make sure
        all browsers are closed.
        """
        try:
            self._debug('Closing all browsers')
            self._cache.close_all()
        except WebDriverException, e:
            logger.warn("Could not close all browsers: %r"%e)
    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `selenium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.
        """
        path, link = self._get_screenshot_paths(filename)
        if hasattr(self._current_browser(), 'get_screenshot_as_file'):
            self._current_browser().get_screenshot_as_file(path)
        else:
            self._current_browser().save_screenshot(path)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))


