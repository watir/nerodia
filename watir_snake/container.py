class Container(object):
    def element(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, self._extract_selector(*args, **kwargs))

    # private

    def _extract_selector(self, *args, **kwargs):
        if args and len(args) == 2:
            return {args[0]: args[1]}
        elif not args:
            return kwargs

        raise ValueError('expected kwargs dict or (how, what), got {}'.format(kwargs))

    # Plural of 'a' cannot be a method name, use link/links instead
    def link(self, *args, **kwargs):
        from .elements.link import Anchor
        return Anchor(self, dict(tag_name='a', **self._extract_selector(*args, **kwargs)))

    def links(self, *args, **kwargs):
        from .elements.html_elements import AnchorCollection
        return AnchorCollection(self, dict(tag_name='a', **self._extract_selector(*args, **kwargs)))

    def abbr(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='abbr', **self._extract_selector(*args, **kwargs)))

    def abbrs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='abbr',
                                                **self._extract_selector(*args, **kwargs)))

    def address(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self,
                           dict(tag_name='address', **self._extract_selector(*args, **kwargs)))

    def addresses(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='address',
                                                **self._extract_selector(*args, **kwargs)))

    def area(self, *args, **kwargs):
        from .elements.area import Area
        return Area(self, dict(tag_name='area', **self._extract_selector(*args, **kwargs)))

    def areas(self, *args, **kwargs):
        from .elements.html_elements import AreaCollection
        return AreaCollection(self, dict(tag_name='area',
                                         **self._extract_selector(*args, **kwargs)))

    def article(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='article',
                                      **self._extract_selector(*args, **kwargs)))

    def articles(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='article',
                                                **self._extract_selector(*args, **kwargs)))

    def aside(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='aside', **self._extract_selector(*args, **kwargs)))

    def asides(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='aside',
                                                **self._extract_selector(*args, **kwargs)))

    def audio(self, *args, **kwargs):
        from .elements.html_elements import Audio
        return Audio(self, dict(tag_name='audio', **self._extract_selector(*args, **kwargs)))

    def audios(self, *args, **kwargs):
        from .elements.html_elements import AudioCollection
        return AudioCollection(self, dict(tag_name='audio',
                                          **self._extract_selector(*args, **kwargs)))

    def b(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='b', **self._extract_selector(*args, **kwargs)))

    def bs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='b',
                                                **self._extract_selector(*args, **kwargs)))

    def base(self, *args, **kwargs):
        from .elements.html_elements import Base
        return Base(self, dict(tag_name='base', **self._extract_selector(*args, **kwargs)))

    def bases(self, *args, **kwargs):
        from .elements.html_elements import BaseCollection
        return BaseCollection(self, dict(tag_name='base',
                                         **self._extract_selector(*args, **kwargs)))

    def bdi(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='bdi', **self._extract_selector(*args, **kwargs)))

    def bdis(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='bdi',
                                                **self._extract_selector(*args, **kwargs)))

    def bdo(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='bdo', **self._extract_selector(*args, **kwargs)))

    def bdos(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='bdo',
                                                **self._extract_selector(*args, **kwargs)))

    def blockquote(self, *args, **kwargs):
        from .elements.html_elements import Quote
        return Quote(self, dict(tag_name='blockquote', **self._extract_selector(*args, **kwargs)))

    def blockquotes(self, *args, **kwargs):
        from .elements.html_elements import QuoteCollection
        return QuoteCollection(self, dict(tag_name='blockquote',
                                          **self._extract_selector(*args, **kwargs)))

    def body(self, *args, **kwargs):
        from .elements.html_elements import Body
        return Body(self, dict(tag_name='body', **self._extract_selector(*args, **kwargs)))

    def bodys(self, *args, **kwargs):
        from .elements.html_elements import BodyCollection
        return BodyCollection(self, dict(tag_name='body',
                                         **self._extract_selector(*args, **kwargs)))

    def br(self, *args, **kwargs):
        from .elements.html_elements import BR
        return BR(self, dict(tag_name='br', **self._extract_selector(*args, **kwargs)))

    def brs(self, *args, **kwargs):
        from .elements.html_elements import BRCollection
        return BRCollection(self, dict(tag_name='br', **self._extract_selector(*args, **kwargs)))

    def button(self, *args, **kwargs):
        from .elements.button import Button
        return Button(self, dict(tag_name='button', **self._extract_selector(*args, **kwargs)))

    def buttons(self, *args, **kwargs):
        from .elements.html_elements import ButtonCollection
        return ButtonCollection(self, dict(tag_name='button',
                                           **self._extract_selector(*args, **kwargs)))

    def canvas(self, *args, **kwargs):
        from .elements.html_elements import Canvas
        return Canvas(self, dict(tag_name='canvas', **self._extract_selector(*args, **kwargs)))

    def canvases(self, *args, **kwargs):
        from .elements.html_elements import CanvasCollection
        return CanvasCollection(self, dict(tag_name='canvas',
                                           **self._extract_selector(*args, **kwargs)))

    def caption(self, *args, **kwargs):
        from .elements.html_elements import TableCaption
        return TableCaption(self, dict(tag_name='caption',
                                       **self._extract_selector(*args, **kwargs)))

    def captions(self, *args, **kwargs):
        from .elements.html_elements import TableCaptionCollection
        return TableCaptionCollection(self, dict(tag_name='caption',
                                                 **self._extract_selector(*args, **kwargs)))

    def checkbox(self, *args, **kwargs):
        from .elements.check_box import CheckBox
        return CheckBox(self, dict(tag_name='input', type='checkbox',
                                   **self._extract_selector(*args, **kwargs)))

    def checkboxes(self, *args, **kwargs):
        from .elements.check_box import CheckBoxCollection
        return CheckBoxCollection(self, dict(tag_name='input', type='checkbox',
                                             **self._extract_selector(*args, **kwargs)))

    def cite(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='cite', **self._extract_selector(*args, **kwargs)))

    def cites(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='cite',
                                                **self._extract_selector(*args, **kwargs)))

    def code(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='code', **self._extract_selector(*args, **kwargs)))

    def codes(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='code',
                                                **self._extract_selector(*args, **kwargs)))

    def col(self, *args, **kwargs):
        from .elements.html_elements import TableCol
        return TableCol(self, dict(tag_name='col', **self._extract_selector(*args, **kwargs)))

    def cols(self, *args, **kwargs):
        from .elements.html_elements import TableColCollection
        return TableColCollection(self, dict(tag_name='col',
                                             **self._extract_selector(*args, **kwargs)))

    def colgroup(self, *args, **kwargs):
        from .elements.html_elements import TableCol
        return TableCol(self, dict(tag_name='colgroup', **self._extract_selector(*args, **kwargs)))

    def colgroups(self, *args, **kwargs):
        from .elements.html_elements import TableColCollection
        return TableColCollection(self, dict(tag_name='colgroup',
                                             **self._extract_selector(*args, **kwargs)))

    def data(self, *args, **kwargs):
        from .elements.html_elements import Data
        return Data(self, dict(tag_name='data', **self._extract_selector(*args, **kwargs)))

    def datas(self, *args, **kwargs):
        from .elements.html_elements import DataCollection
        return DataCollection(self, dict(tag_name='data',
                                         **self._extract_selector(*args, **kwargs)))

    def datalist(self, *args, **kwargs):
        from .elements.html_elements import DataList
        return DataList(self, dict(tag_name='datalist',
                                   **self._extract_selector(*args, **kwargs)))

    def datalists(self, *args, **kwargs):
        from .elements.html_elements import DataListCollection
        return DataListCollection(self, dict(tag_name='datalist',
                                             **self._extract_selector(*args, **kwargs)))

    def dd(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='dd',
                                      **self._extract_selector(*args, **kwargs)))

    def dds(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='dd',
                                                **self._extract_selector(*args, **kwargs)))

    # 'del' is an invalid method name, use delete/deletes instead
    def delete(self, *args, **kwargs):
        from .elements.html_elements import Mod
        return Mod(self, dict(tag_name='del', **self._extract_selector(*args, **kwargs)))

    def deletes(self, *args, **kwargs):
        from .elements.html_elements import ModCollection
        return ModCollection(self, dict(tag_name='del', **self._extract_selector(*args, **kwargs)))

    def details(self, *args, **kwargs):
        from .elements.html_elements import Details
        return Details(self, dict(tag_name='details', **self._extract_selector(*args, **kwargs)))

    def detailses(self, *args, **kwargs):
        from .elements.html_elements import DetailsCollection
        return DetailsCollection(self, dict(tag_name='details',
                                            **self._extract_selector(*args, **kwargs)))

    def dfn(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='dfn', **self._extract_selector(*args, **kwargs)))

    def dfns(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='dfn',
                                                **self._extract_selector(*args, **kwargs)))

    def dialog(self, *args, **kwargs):
        from .elements.html_elements import Dialog
        return Dialog(self, dict(tag_name='dialog', **self._extract_selector(*args, **kwargs)))

    def dialogs(self, *args, **kwargs):
        from .elements.html_elements import DialogCollection
        return DialogCollection(self, dict(tag_name='dialog',
                                           **self._extract_selector(*args, **kwargs)))

    def div(self, *args, **kwargs):
        from .elements.html_elements import Div
        return Div(self, dict(tag_name='div', **self._extract_selector(*args, **kwargs)))

    def divs(self, *args, **kwargs):
        from .elements.html_elements import DivCollection
        return DivCollection(self, dict(tag_name='div', **self._extract_selector(*args, **kwargs)))

    def dl(self, *args, **kwargs):
        from .elements.dlist import DList
        return DList(self, dict(tag_name='dl', **self._extract_selector(*args, **kwargs)))

    def dls(self, *args, **kwargs):
        from .elements.html_elements import DListCollection
        return DListCollection(self, dict(tag_name='dl', **self._extract_selector(*args, **kwargs)))

    def dt(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='dt', **self._extract_selector(*args, **kwargs)))

    def dts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='dt',
                                                **self._extract_selector(*args, **kwargs)))

    def em(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='em', **self._extract_selector(*args, **kwargs)))

    def ems(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='em',
                                                **self._extract_selector(*args, **kwargs)))

    def embed(self, *args, **kwargs):
        from .elements.html_elements import Embed
        return Embed(self, dict(tag_name='embed', **self._extract_selector(*args, **kwargs)))

    def embeds(self, *args, **kwargs):
        from .elements.html_elements import EmbedCollection
        return EmbedCollection(self, dict(tag_name='embed',
                                          **self._extract_selector(*args, **kwargs)))

    def fieldset(self, *args, **kwargs):
        from .elements.html_elements import FieldSet
        return FieldSet(self, dict(tag_name='fieldset', **self._extract_selector(*args, **kwargs)))

    def fieldsets(self, *args, **kwargs):
        from .elements.html_elements import FieldSetCollection
        return FieldSetCollection(self, dict(tag_name='fieldset',
                                             **self._extract_selector(*args, **kwargs)))

    def figcaption(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='figcaption',
                                      **self._extract_selector(*args, **kwargs)))

    def figcaptions(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='figcaption',
                                                **self._extract_selector(*args, **kwargs)))

    def figure(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='figure', **self._extract_selector(*args, **kwargs)))

    def figures(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='figure',
                                                **self._extract_selector(*args, **kwargs)))

    def file_field(self, *args, **kwargs):
        from .elements.file_field import FileField
        return FileField(self, dict(tag_name='input', type='file',
                                    **self._extract_selector(*args, **kwargs)))

    def file_fields(self, *args, **kwargs):
        from .elements.file_field import FileFieldCollection
        return FileFieldCollection(self, dict(tag_name='input', type='file',
                                              **self._extract_selector(*args, **kwargs)))

    def font(self, *args, **kwargs):
        from .elements.html_elements import Font
        return Font(self, dict(tag_name='font', **self._extract_selector(*args, **kwargs)))

    def fonts(self, *args, **kwargs):
        from .elements.html_elements import FontCollection
        return FontCollection(self, dict(tag_name='font',
                                         **self._extract_selector(*args, **kwargs)))

    def footer(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='footer',
                                      **self._extract_selector(*args, **kwargs)))

    def footers(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='footer',
                                                **self._extract_selector(*args, **kwargs)))

    def form(self, *args, **kwargs):
        from .elements.form import Form
        return Form(self, dict(tag_name='form', **self._extract_selector(*args, **kwargs)))

    def forms(self, *args, **kwargs):
        from .elements.html_elements import FormCollection
        return FormCollection(self, dict(tag_name='form',
                                         **self._extract_selector(*args, **kwargs)))

    def frame(self, *args, **kwargs):
        from .elements.i_frame import Frame
        return Frame(self, dict(tag_name='frame', **self._extract_selector(*args, **kwargs)))

    def frames(self, *args, **kwargs):
        from .elements.i_frame import FrameCollection
        return FrameCollection(self, dict(tag_name='frame',
                                          **self._extract_selector(*args, **kwargs)))

    def frameset(self, *args, **kwargs):
        from .elements.html_elements import FrameSet
        return FrameSet(self, dict(tag_name='frameset', **self._extract_selector(*args, **kwargs)))

    def framesets(self, *args, **kwargs):
        from .elements.html_elements import FrameSetCollection
        return FrameSetCollection(self, dict(tag_name='frameset',
                                             **self._extract_selector(*args, **kwargs)))

    def h1(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(tag_name='h1', **self._extract_selector(*args, **kwargs)))

    def h1s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(tag_name='h1',
                                            **self._extract_selector(*args, **kwargs)))

    def h2(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(tag_name='h2', **self._extract_selector(*args, **kwargs)))

    def h2s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(tag_name='h2',
                                            **self._extract_selector(*args, **kwargs)))

    def h3(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(tag_name='h3', **self._extract_selector(*args, **kwargs)))

    def h3s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(tag_name='h3',
                                            **self._extract_selector(*args, **kwargs)))

    def h4(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(tag_name='h4', **self._extract_selector(*args, **kwargs)))

    def h4s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(tag_name='h4',
                                            **self._extract_selector(*args, **kwargs)))

    def h5(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(tag_name='h5', **self._extract_selector(*args, **kwargs)))

    def h5s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(tag_name='h5',
                                            **self._extract_selector(*args, **kwargs)))

    def h6(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(tag_name='h6', **self._extract_selector(*args, **kwargs)))

    def h6s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(tag_name='h6',
                                            **self._extract_selector(*args, **kwargs)))

    def head(self, *args, **kwargs):
        from .elements.html_elements import Head
        return Head(self, dict(tag_name='head', **self._extract_selector(*args, **kwargs)))

    def heads(self, *args, **kwargs):
        from .elements.html_elements import HeadCollection
        return HeadCollection(self, dict(tag_name='head',
                                         **self._extract_selector(*args, **kwargs)))

    def header(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='header',
                                      **self._extract_selector(*args, **kwargs)))

    def headers(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='header',
                                                **self._extract_selector(*args, **kwargs)))

    def hgroup(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='hgroup', **self._extract_selector(*args, **kwargs)))

    def hgroups(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='hgroup',
                                                **self._extract_selector(*args, **kwargs)))

    def hidden(self, *args, **kwargs):
        from .elements.hidden import Hidden
        return Hidden(self, dict(tag_name='input', type='hidden',
                                 **self._extract_selector(*args, **kwargs)))

    def hiddens(self, *args, **kwargs):
        from .elements.hidden import HiddenCollection
        return HiddenCollection(self, dict(tag_name='input', type='hidden',
                                           **self._extract_selector(*args, **kwargs)))

    def hr(self, *args, **kwargs):
        from .elements.html_elements import HR
        return HR(self, dict(tag_name='hr', **self._extract_selector(*args, **kwargs)))

    def hrs(self, *args, **kwargs):
        from .elements.html_elements import HRCollection
        return HRCollection(self, dict(tag_name='hr', **self._extract_selector(*args, **kwargs)))

    def html(self, *args, **kwargs):
        from .elements.html_elements import Html
        return Html(self, dict(tag_name='html', **self._extract_selector(*args, **kwargs)))

    def htmls(self, *args, **kwargs):
        from .elements.html_elements import HtmlCollection
        return HtmlCollection(self, dict(tag_name='html',
                                         **self._extract_selector(*args, **kwargs)))

    # Plural of 'i' cannot be a method name, use ital/itals instead
    def ital(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='i', **self._extract_selector(*args, **kwargs)))

    def itals(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='i',
                                                **self._extract_selector(*args, **kwargs)))

    def iframe(self, *args, **kwargs):
        from .elements.i_frame import IFrame
        return IFrame(self, dict(tag_name='iframe', **self._extract_selector(*args, **kwargs)))

    def iframes(self, *args, **kwargs):
        from .elements.html_elements import IFrameCollection
        return IFrameCollection(self, dict(tag_name='iframe',
                                           **self._extract_selector(*args, **kwargs)))

    def img(self, *args, **kwargs):
        from .elements.image import Image
        return Image(self, dict(tag_name='img', **self._extract_selector(*args, **kwargs)))

    def imgs(self, *args, **kwargs):
        from .elements.html_elements import ImageCollection
        return ImageCollection(self, dict(tag_name='img',
                                          **self._extract_selector(*args, **kwargs)))

    def input(self, *args, **kwargs):
        from .elements.input import Input
        return Input(self, dict(tag_name='input', **self._extract_selector(*args, **kwargs)))

    def inputs(self, *args, **kwargs):
        from .elements.html_elements import InputCollection
        return InputCollection(self, dict(tag_name='input',
                                          **self._extract_selector(*args, **kwargs)))

    def ins(self, *args, **kwargs):
        from .elements.html_elements import Mod
        return Mod(self, dict(tag_name='ins', **self._extract_selector(*args, **kwargs)))

    def inses(self, *args, **kwargs):
        from .elements.html_elements import ModCollection
        return ModCollection(self, dict(tag_name='ins', **self._extract_selector(*args, **kwargs)))

    def kbd(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='kbd', **self._extract_selector(*args, **kwargs)))

    def kbds(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='kbd',
                                                **self._extract_selector(*args, **kwargs)))

    def keygen(self, *args, **kwargs):
        from .elements.html_elements import Keygen
        return Keygen(self, dict(tag_name='keygen', **self._extract_selector(*args, **kwargs)))

    def keygens(self, *args, **kwargs):
        from .elements.html_elements import KeygenCollection
        return KeygenCollection(self, dict(tag_name='keygen',
                                           **self._extract_selector(*args, **kwargs)))

    def label(self, *args, **kwargs):
        from .elements.html_elements import Label
        return Label(self, dict(tag_name='label', **self._extract_selector(*args, **kwargs)))

    def labels(self, *args, **kwargs):
        from .elements.html_elements import LabelCollection
        return LabelCollection(self, dict(tag_name='label',
                                          **self._extract_selector(*args, **kwargs)))

    def legend(self, *args, **kwargs):
        from .elements.html_elements import Legend
        return Legend(self, dict(tag_name='legend', **self._extract_selector(*args, **kwargs)))

    def legends(self, *args, **kwargs):
        from .elements.html_elements import LegendCollection
        return LegendCollection(self, dict(tag_name='legend',
                                           **self._extract_selector(*args, **kwargs)))

    def li(self, *args, **kwargs):
        from .elements.html_elements import LI
        return LI(self, dict(tag_name='li', **self._extract_selector(*args, **kwargs)))

    def lis(self, *args, **kwargs):
        from .elements.html_elements import LICollection
        return LICollection(self, dict(tag_name='li', **self._extract_selector(*args, **kwargs)))

    def main(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='main', **self._extract_selector(*args, **kwargs)))

    def mains(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='main',
                                                **self._extract_selector(*args, **kwargs)))

    def map(self, *args, **kwargs):
        from .elements.html_elements import Map
        return Map(self, dict(tag_name='map', **self._extract_selector(*args, **kwargs)))

    def maps(self, *args, **kwargs):
        from .elements.html_elements import MapCollection
        return MapCollection(self, dict(tag_name='map', **self._extract_selector(*args, **kwargs)))

    def mark(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='mark', **self._extract_selector(*args, **kwargs)))

    def marks(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='mark',
                                                **self._extract_selector(*args, **kwargs)))

    def menu(self, *args, **kwargs):
        from .elements.html_elements import Menu
        return Menu(self, dict(tag_name='menu', **self._extract_selector(*args, **kwargs)))

    def menus(self, *args, **kwargs):
        from .elements.html_elements import MenuCollection
        return MenuCollection(self, dict(tag_name='menu',
                                         **self._extract_selector(*args, **kwargs)))

    def menuitem(self, *args, **kwargs):
        from .elements.html_elements import MenuItem
        return MenuItem(self, dict(tag_name='menuitem', **self._extract_selector(*args, **kwargs)))

    def menuitems(self, *args, **kwargs):
        from .elements.html_elements import MenuItemCollection
        return MenuItemCollection(self, dict(tag_name='menuitem',
                                             **self._extract_selector(*args, **kwargs)))

    def meta(self, *args, **kwargs):
        from .elements.html_elements import Meta
        return Meta(self, dict(tag_name='meta', **self._extract_selector(*args, **kwargs)))

    def metas(self, *args, **kwargs):
        from .elements.html_elements import MetaCollection
        return MetaCollection(self, dict(tag_name='meta',
                                         **self._extract_selector(*args, **kwargs)))

    def meter(self, *args, **kwargs):
        from .elements.html_elements import Meter
        return Meter(self, dict(tag_name='meter', **self._extract_selector(*args, **kwargs)))

    def meters(self, *args, **kwargs):
        from .elements.html_elements import MeterCollection
        return MeterCollection(self, dict(tag_name='meter',
                                          **self._extract_selector(*args, **kwargs)))

    def nav(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='nav', **self._extract_selector(*args, **kwargs)))

    def navs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='nav',
                                                **self._extract_selector(*args, **kwargs)))

    def noscript(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='noscript',
                                      **self._extract_selector(*args, **kwargs)))

    def noscripts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='noscript',
                                                **self._extract_selector(*args, **kwargs)))

    def object(self, *args, **kwargs):
        from .elements.html_elements import Object
        return Object(self, dict(tag_name='object', **self._extract_selector(*args, **kwargs)))

    def objects(self, *args, **kwargs):
        from .elements.html_elements import ObjectCollection
        return ObjectCollection(self, dict(tag_name='object',
                                           **self._extract_selector(*args, **kwargs)))

    def ol(self, *args, **kwargs):
        from .elements.html_elements import OList
        return OList(self, dict(tag_name='ol', **self._extract_selector(*args, **kwargs)))

    def ols(self, *args, **kwargs):
        from .elements.html_elements import OListCollection
        return OListCollection(self, dict(tag_name='ol', **self._extract_selector(*args, **kwargs)))

    def optgroup(self, *args, **kwargs):
        from .elements.html_elements import OptGroup
        return OptGroup(self, dict(tag_name='optgroup', **self._extract_selector(*args, **kwargs)))

    def optgroups(self, *args, **kwargs):
        from .elements.html_elements import OptGroupCollection
        return OptGroupCollection(self, dict(tag_name='optgroup',
                                             **self._extract_selector(*args, **kwargs)))

    def option(self, *args, **kwargs):
        from .elements.option import Option
        return Option(self, dict(tag_name='option', **self._extract_selector(*args, **kwargs)))

    def options(self, *args, **kwargs):
        from .elements.html_elements import OptionCollection
        return OptionCollection(self, dict(tag_name='option',
                                           **self._extract_selector(*args, **kwargs)))

    def output(self, *args, **kwargs):
        from .elements.html_elements import Output
        return Output(self, dict(tag_name='output', **self._extract_selector(*args, **kwargs)))

    def outputs(self, *args, **kwargs):
        from .elements.html_elements import OutputCollection
        return OutputCollection(self, dict(tag_name='output',
                                           **self._extract_selector(*args, **kwargs)))

    def p(self, *args, **kwargs):
        from .elements.html_elements import Paragraph
        return Paragraph(self, dict(tag_name='p', **self._extract_selector(*args, **kwargs)))

    def ps(self, *args, **kwargs):
        from .elements.html_elements import ParagraphCollection
        return ParagraphCollection(self, dict(tag_name='p',
                                              **self._extract_selector(*args, **kwargs)))

    def param(self, *args, **kwargs):
        from .elements.html_elements import Param
        return Param(self, dict(tag_name='param', **self._extract_selector(*args, **kwargs)))

    def params(self, *args, **kwargs):
        from .elements.html_elements import ParamCollection
        return ParamCollection(self, dict(tag_name='param',
                                          **self._extract_selector(*args, **kwargs)))

    def pre(self, *args, **kwargs):
        from .elements.html_elements import Pre
        return Pre(self, dict(tag_name='pre', **self._extract_selector(*args, **kwargs)))

    def pres(self, *args, **kwargs):
        from .elements.html_elements import PreCollection
        return PreCollection(self, dict(tag_name='pre', **self._extract_selector(*args, **kwargs)))

    def progress(self, *args, **kwargs):
        from .elements.html_elements import Progress
        return Progress(self, dict(tag_name='progress', **self._extract_selector(*args, **kwargs)))

    def progresses(self, *args, **kwargs):
        from .elements.html_elements import ProgressCollection
        return ProgressCollection(self, dict(tag_name='progress',
                                             **self._extract_selector(*args, **kwargs)))

    def q(self, *args, **kwargs):
        from .elements.html_elements import Quote
        return Quote(self, dict(tag_name='q', **self._extract_selector(*args, **kwargs)))

    def qs(self, *args, **kwargs):
        from .elements.html_elements import QuoteCollection
        return QuoteCollection(self, dict(tag_name='q', **self._extract_selector(*args, **kwargs)))

    def radio(self, *args, **kwargs):
        from .elements.radio import Radio
        return Radio(self, dict(tag_name='input', type='radio',
                                **self._extract_selector(*args, **kwargs)))

    def radios(self, *args, **kwargs):
        from .elements.radio import RadioCollection
        return RadioCollection(self, dict(tag_name='input', type='radio',
                                          **self._extract_selector(*args, **kwargs)))

    def rp(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='rp', **self._extract_selector(*args, **kwargs)))

    def rps(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='rp',
                                                **self._extract_selector(*args, **kwargs)))

    def rt(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='rt', **self._extract_selector(*args, **kwargs)))

    def rts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='rt',
                                                **self._extract_selector(*args, **kwargs)))

    def ruby(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='ruby', **self._extract_selector(*args, **kwargs)))

    def rubies(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='ruby',
                                                **self._extract_selector(*args, **kwargs)))

    def s(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='s', **self._extract_selector(*args, **kwargs)))

    def ss(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='s',
                                                **self._extract_selector(*args, **kwargs)))

    def samp(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='samp', **self._extract_selector(*args, **kwargs)))

    def samps(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='samp',
                                                **self._extract_selector(*args, **kwargs)))

    def script(self, *args, **kwargs):
        from .elements.html_elements import Script
        return Script(self, dict(tag_name='script', **self._extract_selector(*args, **kwargs)))

    def scripts(self, *args, **kwargs):
        from .elements.html_elements import ScriptCollection
        return ScriptCollection(self, dict(tag_name='script',
                                           **self._extract_selector(*args, **kwargs)))

    def section(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='section',
                                      **self._extract_selector(*args, **kwargs)))

    def sections(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='section',
                                                **self._extract_selector(*args, **kwargs)))

    def select(self, *args, **kwargs):
        from .elements.select import Select
        return Select(self, dict(tag_name='select', **self._extract_selector(*args, **kwargs)))

    select_list = select

    def selects(self, *args, **kwargs):
        from .elements.html_elements import SelectCollection
        return SelectCollection(self, dict(tag_name='select',
                                           **self._extract_selector(*args, **kwargs)))

    select_lists = selects

    def small(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='small', **self._extract_selector(*args, **kwargs)))

    def smalls(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='small',
                                                **self._extract_selector(*args, **kwargs)))

    def source(self, *args, **kwargs):
        from .elements.html_elements import Source
        return Source(self, dict(tag_name='source', **self._extract_selector(*args, **kwargs)))

    def sources(self, *args, **kwargs):
        from .elements.html_elements import SourceCollection
        return SourceCollection(self, dict(tag_name='source',
                                           **self._extract_selector(*args, **kwargs)))

    def span(self, *args, **kwargs):
        from .elements.html_elements import Span
        return Span(self, dict(tag_name='span', **self._extract_selector(*args, **kwargs)))

    def spans(self, *args, **kwargs):
        from .elements.html_elements import SpanCollection
        return SpanCollection(self, dict(tag_name='span',
                                         **self._extract_selector(*args, **kwargs)))

    def strong(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='strong', **self._extract_selector(*args, **kwargs)))

    def strongs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='strong',
                                                **self._extract_selector(*args, **kwargs)))

    def style(self, *args, **kwargs):
        from .elements.html_elements import Style
        return Style(self, dict(tag_name='style', **self._extract_selector(*args, **kwargs)))

    def styles(self, *args, **kwargs):
        from .elements.html_elements import StyleCollection
        return StyleCollection(self, dict(tag_name='style',
                                          **self._extract_selector(*args, **kwargs)))

    def sub(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='sub', **self._extract_selector(*args, **kwargs)))

    def subs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='sub',
                                                **self._extract_selector(*args, **kwargs)))

    def summary(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='summary',
                                      **self._extract_selector(*args, **kwargs)))

    def summaries(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='summary',
                                                **self._extract_selector(*args, **kwargs)))

    def sup(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='sup', **self._extract_selector(*args, **kwargs)))

    def sups(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='sup',
                                                **self._extract_selector(*args, **kwargs)))

    def table(self, *args, **kwargs):
        from .elements.table import Table
        return Table(self, dict(tag_name='table', **self._extract_selector(*args, **kwargs)))

    def tables(self, *args, **kwargs):
        from .elements.table import TableCollection
        return TableCollection(self, dict(tag_name='table',
                                          **self._extract_selector(*args, **kwargs)))

    def tbody(self, *args, **kwargs):
        from .elements.table_section import TableSection
        return TableSection(self, dict(tag_name='tbody', **self._extract_selector(*args, **kwargs)))

    def tbodys(self, *args, **kwargs):
        from .elements.table_section import TableSectionCollection
        return TableSectionCollection(self, dict(tag_name='tbody',
                                                 **self._extract_selector(*args, **kwargs)))

    def td(self, *args, **kwargs):
        from .elements.html_elements import TableDataCell
        return TableDataCell(self, dict(tag_name='td', **self._extract_selector(*args, **kwargs)))

    def tds(self, *args, **kwargs):
        from .elements.html_elements import TableDataCellCollection
        return TableDataCellCollection(self, dict(tag_name='td',
                                                  **self._extract_selector(*args, **kwargs)))

    def template(self, *args, **kwargs):
        from .elements.html_elements import Template
        return Template(self, dict(tag_name='template', **self._extract_selector(*args, **kwargs)))

    def templates(self, *args, **kwargs):
        from .elements.html_elements import TemplateCollection
        return TemplateCollection(self, dict(tag_name='template',
                                             **self._extract_selector(*args, **kwargs)))

    def textarea(self, *args, **kwargs):
        from .elements.text_area import TextArea
        return TextArea(self, dict(tag_name='textarea', **self._extract_selector(*args, **kwargs)))

    def textareas(self, *args, **kwargs):
        from .elements.html_elements import TextAreaCollection
        return TextAreaCollection(self, dict(tag_name='textarea',
                                             **self._extract_selector(*args, **kwargs)))

    def text_field(self, *args, **kwargs):
        from .elements.text_field import TextField
        return TextField(self, dict(tag_name='input', **self._extract_selector(*args, **kwargs)))

    def text_fields(self, *args, **kwargs):
        from .elements.text_field import TextFieldCollection
        return TextFieldCollection(self, dict(tag_name='input',
                                              **self._extract_selector(*args, **kwargs)))

    def tfoot(self, *args, **kwargs):
        from .elements.table_section import TableSection
        return TableSection(self, dict(tag_name='tfoot', **self._extract_selector(*args, **kwargs)))

    def tfoots(self, *args, **kwargs):
        from .elements.table_section import TableSectionCollection
        return TableSectionCollection(self, dict(tag_name='tfoot',
                                                 **self._extract_selector(*args, **kwargs)))

    def th(self, *args, **kwargs):
        from .elements.html_elements import TableHeaderCell
        return TableHeaderCell(self, dict(tag_name='th', **self._extract_selector(*args, **kwargs)))

    def ths(self, *args, **kwargs):
        from .elements.html_elements import TableHeaderCellCollection
        return TableHeaderCellCollection(self, dict(tag_name='th',
                                                    **self._extract_selector(*args, **kwargs)))

    def thead(self, *args, **kwargs):
        from .elements.table_section import TableSection
        return TableSection(self, dict(tag_name='thead', **self._extract_selector(*args, **kwargs)))

    def theads(self, *args, **kwargs):
        from .elements.table_section import TableSectionCollection
        return TableSectionCollection(self, dict(tag_name='thead',
                                                 **self._extract_selector(*args, **kwargs)))

    def time(self, *args, **kwargs):
        from .elements.html_elements import Time
        return Time(self, dict(tag_name='time', **self._extract_selector(*args, **kwargs)))

    def times(self, *args, **kwargs):
        from .elements.html_elements import TimeCollection
        return TimeCollection(self, dict(tag_name='time',
                                         **self._extract_selector(*args, **kwargs)))

    def title(self, *args, **kwargs):
        from .elements.html_elements import Title
        return Title(self, dict(tag_name='title', **self._extract_selector(*args, **kwargs)))

    def titles(self, *args, **kwargs):
        from .elements.html_elements import TitleCollection
        return TitleCollection(self, dict(tag_name='title',
                                          **self._extract_selector(*args, **kwargs)))

    def tr(self, *args, **kwargs):
        from .elements.table_row import TableRow
        return TableRow(self, dict(tag_name='tr', **self._extract_selector(*args, **kwargs)))

    def trs(self, *args, **kwargs):
        from .elements.html_elements import TableRowCollection
        return TableRowCollection(self, dict(tag_name='tr',
                                             **self._extract_selector(*args, **kwargs)))

    def track(self, *args, **kwargs):
        from .elements.html_elements import Track
        return Track(self, dict(tag_name='track', **self._extract_selector(*args, **kwargs)))

    def tracks(self, *args, **kwargs):
        from .elements.html_elements import TrackCollection
        return TrackCollection(self, dict(tag_name='track',
                                          **self._extract_selector(*args, **kwargs)))

    def u(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='u', **self._extract_selector(*args, **kwargs)))

    def us(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='u',
                                                **self._extract_selector(*args, **kwargs)))

    def ul(self, *args, **kwargs):
        from .elements.html_elements import UList
        return UList(self, dict(tag_name='ul', **self._extract_selector(*args, **kwargs)))

    def uls(self, *args, **kwargs):
        from .elements.html_elements import UListCollection
        return UListCollection(self, dict(tag_name='ul', **self._extract_selector(*args, **kwargs)))

    def var(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='var', **self._extract_selector(*args, **kwargs)))

    def vars(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='var',
                                                **self._extract_selector(*args, **kwargs)))

    def video(self, *args, **kwargs):
        from .elements.html_elements import Video
        return Video(self, dict(tag_name='video', **self._extract_selector(*args, **kwargs)))

    def videos(self, *args, **kwargs):
        from .elements.html_elements import VideoCollection
        return VideoCollection(self, dict(tag_name='video',
                                          **self._extract_selector(*args, **kwargs)))

    def wbr(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(tag_name='wbr', **self._extract_selector(*args, **kwargs)))

    def wbrs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(tag_name='wbr',
                                                **self._extract_selector(*args, **kwargs)))
