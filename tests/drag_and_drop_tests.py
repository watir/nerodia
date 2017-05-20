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
    # TODO: xfail safari
    def test_can_drag_and_drop_an_element_onto_another(self, browser, draggable, droppable):
        assert droppable.text == 'Drop here'
        draggable.drag_and_drop_on(droppable)
        assert droppable.text == 'Dropped!'

    # TODO: xfail FF legacy?
    def test_can_drag_and_drop_an_element_onto_another_when_draggable_is_out_of_viewport(self, browser, draggable, droppable):
        reposition(browser, 'draggable')
        perform_drag_and_drop_on_droppable(draggable, droppable)

    # TODO: xfail FF legacy?
    def test_can_drag_and_drop_an_element_onto_another_when_droppable_is_out_of_viewport(self, browser, draggable, droppable):
        reposition(browser, 'droppable')
        perform_drag_and_drop_on_droppable(draggable, droppable)

    def test_can_drag_an_element_by_the_given_offset(self, browser, draggable, droppable):
        assert droppable.text == 'Drop here'
        draggable.drag_and_drop_by(200, 50)
        assert droppable.text == 'Dropped!'
