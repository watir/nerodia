"""Basic script showing how Nerodia works."""
from nerodia.browser import Browser


def run():
    br = Browser(browser='chrome')

    br.goto("https://watir.com")

    # Check that "Titus" is somewhere in the page text
    assert "Watir" in br.text

    # Check "open source" is in the intro
    intro_text = br.div(class_name='intro').text
    assert "open source" in intro_text

    # Check that the page is correct via the URL
    br.link(text='Guides').click()
    assert 'watir.com/guides/' in br.url

    br.close()


if __name__ == '__main__':
    run()
