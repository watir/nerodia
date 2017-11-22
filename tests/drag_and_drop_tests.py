import pytest


@pytest.fixture()
def draggable(browser):
    yield browser.div(id='draggable')


@pytest.fixture()
def droppable(browser):
    yield browser.div(id='droppable')


def perform_drag_and_drop_on_droppable(draggable, droppable):
    assert droppable.text == 'Drop here'
    draggable.drag_and_drop_on(droppable)
    assert droppable.text == 'Dropped!'


def reposition(browser, what):
    browser.button(id='reposition{}'.format(what.capitalize())).click()


@pytest.mark.page('drag_and_drop.html')
class TestElementDragAndDrop(object):

    @pytest.mark.xfail_safari
    @pytest.mark.quits_browser
    def test_can_drag_and_drop_an_element_onto_another(self, browser, draggable, droppable):
        assert droppable.text == 'Drop here'
        draggable.drag_and_drop_on(droppable)
        assert droppable.text == 'Dropped!'

    @pytest.mark.xfail_firefox
    @pytest.mark.quits_browser
    def test_can_drag_and_drop_an_element_onto_another_when_draggable_is_out_of_viewport(self, browser, draggable, droppable):
        reposition(browser, 'draggable')
        perform_drag_and_drop_on_droppable(draggable, droppable)

    @pytest.mark.quits_browser
    def test_can_drag_an_element_by_the_given_offset(self, browser, draggable, droppable):
        assert droppable.text == 'Drop here'
        y = 150 if browser.wd.w3c else 50
        draggable.drag_and_drop_by(200, y)
        assert droppable.text == 'Dropped!'
