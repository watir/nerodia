class Scrolling(object):

    @property
    def scroll(self):
        return Scroll(self)


class Scroll(object):

    def __init__(self, ob):
        self.ob = ob

    def by(self, left, top):
        """
        Scrolls by offset.

        :param int left: horizontal offset
        :param int top: vertical offset

        :Example: Scroll by an offset.

        browser.element(name='new_user_button').scroll().by(10, 20)
        """
        self.ob.browser.execute_script('window.scrollBy(arguments[0], arguments[1]);', left, top)
        return self

    def to(self, param='top'):
        """
        Scrolls to specified location.

        :param str param: location to scroll to

        :Example: Scroll by an to a location.

        browser.element(name='new_user_button').scroll().to('top')
        """
        from nerodia.elements.element import Element
        if isinstance(self.ob, Element):
            args = self._element_scroll(param)
        else:
            args = self._browser_scroll(param)
        if args is None:
            raise ValueError("Don't know how to scroll {} to: {}!".format(self.ob, param))
        self.ob.browser.execute_script(*args)
        return self

    # private

    def _element_scroll(self, param):
        if param in ('top', 'start'):
            script = 'arguments[0].scrollIntoView();'
        elif param == 'center':
            script = 'var bodyRect = document.body.getBoundingClientRect();' \
                     'var elementRect = arguments[0].getBoundingClientRect();' \
                     'var left = (elementRect.left - bodyRect.left) - (window.innerWidth / 2);' \
                     'var top = (elementRect.top - bodyRect.top) - (window.innerHeight / 2);' \
                     'window.scrollTo(left, top);'

        elif param in ['bottom', 'end']:
            script = 'arguments[0].scrollIntoView(false);'
        else:
            return None
        return [script, self.ob]

    @staticmethod
    def _browser_scroll(param):
        if param in ('top', 'start'):
            return ['window.scrollTo(0, 0);']
        elif param == 'center':
            return ['window.scrollTo(window.outerWidth / 2, window.outerHeight / 2);']
        elif param in ['bottom', 'end']:
            return ['window.scrollTo(0, document.body.scrollHeight);']
        elif isinstance(param, list):
            return ['window.scrollTo(arguments[0], arguments[1]);', param[0], param[1]]
