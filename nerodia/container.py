class Container(object):
    def element(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, self._extract_selector(*args, **kwargs))

    def elements(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, self._extract_selector(*args, **kwargs))

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
        return Anchor(self, dict(self._extract_selector(*args, **kwargs), tag_name='a'))

    def links(self, *args, **kwargs):
        from .elements.html_elements import AnchorCollection
        return AnchorCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='a'))

    def abbr(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='abbr'))

    def abbrs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                     tag_name='abbr'))

    def address(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='address'))

    def addresses(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                     tag_name='address'))

    def area(self, *args, **kwargs):
        from .elements.area import Area
        return Area(self, dict(self._extract_selector(*args, **kwargs), tag_name='area'))

    def areas(self, *args, **kwargs):
        from .elements.html_elements import AreaCollection
        return AreaCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='area'))

    def article(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='article'))

    def articles(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='article'))

    def aside(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='aside'))

    def asides(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='aside'))

    def audio(self, *args, **kwargs):
        from .elements.html_elements import Audio
        return Audio(self, dict(self._extract_selector(*args, **kwargs), tag_name='audio'))

    def audios(self, *args, **kwargs):
        from .elements.html_elements import AudioCollection
        return AudioCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='audio'))

    def b(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='b'))

    def bs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='b'))

    def base(self, *args, **kwargs):
        from .elements.html_elements import Base
        return Base(self, dict(self._extract_selector(*args, **kwargs), tag_name='base'))

    def bases(self, *args, **kwargs):
        from .elements.html_elements import BaseCollection
        return BaseCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='base'))

    def bdi(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='bdi'))

    def bdis(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='bdi'))

    def bdo(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='bdo'))

    def bdos(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='bdo'))

    def blockquote(self, *args, **kwargs):
        from .elements.html_elements import Quote
        return Quote(self, dict(self._extract_selector(*args, **kwargs), tag_name='blockquote'))

    def blockquotes(self, *args, **kwargs):
        from .elements.html_elements import QuoteCollection
        return QuoteCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='blockquote'))

    def body(self, *args, **kwargs):
        from .elements.html_elements import Body
        return Body(self, dict(self._extract_selector(*args, **kwargs), tag_name='body'))

    def bodys(self, *args, **kwargs):
        from .elements.html_elements import BodyCollection
        return BodyCollection(self, dict(self._extract_selector(*args, **kwargs),
                                         tag_name='body'))

    def br(self, *args, **kwargs):
        from .elements.html_elements import BR
        return BR(self, dict(self._extract_selector(*args, **kwargs), tag_name='br'))

    def brs(self, *args, **kwargs):
        from .elements.html_elements import BRCollection
        return BRCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='br'))

    def button(self, *args, **kwargs):
        from .elements.button import Button
        return Button(self, dict(self._extract_selector(*args, **kwargs), tag_name='button'))

    def buttons(self, *args, **kwargs):
        from .elements.html_elements import ButtonCollection
        return ButtonCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='button'))

    def canvas(self, *args, **kwargs):
        from .elements.html_elements import Canvas
        return Canvas(self, dict(self._extract_selector(*args, **kwargs), tag_name='canvas'))

    def canvases(self, *args, **kwargs):
        from .elements.html_elements import CanvasCollection
        return CanvasCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='canvas'))

    def caption(self, *args, **kwargs):
        from .elements.html_elements import TableCaption
        return TableCaption(self, dict(self._extract_selector(*args, **kwargs),
                                       tag_name='caption'))

    def captions(self, *args, **kwargs):
        from .elements.html_elements import TableCaptionCollection
        return TableCaptionCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                 tag_name='caption'))

    def checkbox(self, *args, **kwargs):
        from .elements.check_box import CheckBox
        return CheckBox(self, dict(self._extract_selector(*args, **kwargs), tag_name='input',
                                   type='checkbox',))

    def checkboxes(self, *args, **kwargs):
        from .elements.check_box import CheckBoxCollection
        return CheckBoxCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='input', type='checkbox',))

    def cite(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='cite'))

    def cites(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='cite'))

    def code(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='code'))

    def codes(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='code'))

    def col(self, *args, **kwargs):
        from .elements.html_elements import TableCol
        return TableCol(self, dict(self._extract_selector(*args, **kwargs), tag_name='col'))

    def cols(self, *args, **kwargs):
        from .elements.html_elements import TableColCollection
        return TableColCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='col'))

    def colgroup(self, *args, **kwargs):
        from .elements.html_elements import TableCol
        return TableCol(self, dict(self._extract_selector(*args, **kwargs), tag_name='colgroup'))

    def colgroups(self, *args, **kwargs):
        from .elements.html_elements import TableColCollection
        return TableColCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='colgroup'))

    def data(self, *args, **kwargs):
        from .elements.html_elements import Data
        return Data(self, dict(self._extract_selector(*args, **kwargs), tag_name='data'))

    def datas(self, *args, **kwargs):
        from .elements.html_elements import DataCollection
        return DataCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='data'))

    def datalist(self, *args, **kwargs):
        from .elements.html_elements import DataList
        return DataList(self, dict(self._extract_selector(*args, **kwargs), tag_name='datalist'))

    def datalists(self, *args, **kwargs):
        from .elements.html_elements import DataListCollection
        return DataListCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='datalist'))

    def dd(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='dd'))

    def dds(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='dd'))

    # 'del' is an invalid method name, use delete/deletes instead
    def delete(self, *args, **kwargs):
        from .elements.html_elements import Mod
        return Mod(self, dict(self._extract_selector(*args, **kwargs), tag_name='del'))

    def deletes(self, *args, **kwargs):
        from .elements.html_elements import ModCollection
        return ModCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='del'))

    def details(self, *args, **kwargs):
        from .elements.html_elements import Details
        return Details(self, dict(self._extract_selector(*args, **kwargs), tag_name='details'))

    def detailses(self, *args, **kwargs):
        from .elements.html_elements import DetailsCollection
        return DetailsCollection(self, dict(self._extract_selector(*args, **kwargs),
                                            tag_name='details'))

    def dfn(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='dfn'))

    def dfns(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='dfn'))

    def dialog(self, *args, **kwargs):
        from .elements.html_elements import Dialog
        return Dialog(self, dict(self._extract_selector(*args, **kwargs), tag_name='dialog'))

    def dialogs(self, *args, **kwargs):
        from .elements.html_elements import DialogCollection
        return DialogCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='dialog'))

    def div(self, *args, **kwargs):
        from .elements.html_elements import Div
        return Div(self, dict(self._extract_selector(*args, **kwargs), tag_name='div'))

    def divs(self, *args, **kwargs):
        from .elements.html_elements import DivCollection
        return DivCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='div'))

    def dl(self, *args, **kwargs):
        from .elements.d_list import DList
        return DList(self, dict(self._extract_selector(*args, **kwargs), tag_name='dl'))

    def dls(self, *args, **kwargs):
        from .elements.html_elements import DListCollection
        return DListCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='dl'))

    def dt(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='dt'))

    def dts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='dt'))

    def em(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='em'))

    def ems(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='em'))

    def embed(self, *args, **kwargs):
        from .elements.html_elements import Embed
        return Embed(self, dict(self._extract_selector(*args, **kwargs), tag_name='embed'))

    def embeds(self, *args, **kwargs):
        from .elements.html_elements import EmbedCollection
        return EmbedCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='embed'))

    def fieldset(self, *args, **kwargs):
        from .elements.html_elements import FieldSet
        return FieldSet(self, dict(self._extract_selector(*args, **kwargs), tag_name='fieldset'))

    field_set = fieldset

    def fieldsets(self, *args, **kwargs):
        from .elements.html_elements import FieldSetCollection
        return FieldSetCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='fieldset'))

    field_sets = fieldsets

    def figcaption(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs),
                                      tag_name='figcaption'))

    def figcaptions(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='figcaption'))

    def figure(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='figure'))

    def figures(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='figure'))

    def file_field(self, *args, **kwargs):
        from .elements.file_field import FileField
        return FileField(self, dict(self._extract_selector(*args, **kwargs), tag_name='input',
                                    type='file'))

    def file_fields(self, *args, **kwargs):
        from .elements.file_field import FileFieldCollection
        return FileFieldCollection(self, dict(self._extract_selector(*args, **kwargs),
                                              tag_name='input', type='file'))

    def font(self, *args, **kwargs):
        from .elements.font import Font
        return Font(self, dict(self._extract_selector(*args, **kwargs), tag_name='font'))

    def fonts(self, *args, **kwargs):
        from .elements.html_elements import FontCollection
        return FontCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='font'))

    def footer(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='footer'))

    def footers(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='footer'))

    def form(self, *args, **kwargs):
        from .elements.form import Form
        return Form(self, dict(self._extract_selector(*args, **kwargs), tag_name='form'))

    def forms(self, *args, **kwargs):
        from .elements.html_elements import FormCollection
        return FormCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='form'))

    def frame(self, *args, **kwargs):
        from .elements.i_frame import Frame
        return Frame(self, dict(self._extract_selector(*args, **kwargs), tag_name='frame'))

    def frames(self, *args, **kwargs):
        from .elements.i_frame import FrameCollection
        return FrameCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='frame'))

    def frameset(self, *args, **kwargs):
        from .elements.html_elements import FrameSet
        return FrameSet(self, dict(self._extract_selector(*args, **kwargs), tag_name='frameset'))

    def framesets(self, *args, **kwargs):
        from .elements.html_elements import FrameSetCollection
        return FrameSetCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='frameset'))

    def h1(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(self._extract_selector(*args, **kwargs), tag_name='h1'))

    def h1s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='h1'))

    def h2(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(self._extract_selector(*args, **kwargs), tag_name='h2'))

    def h2s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='h2'))

    def h3(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(self._extract_selector(*args, **kwargs), tag_name='h3'))

    def h3s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='h3'))

    def h4(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(self._extract_selector(*args, **kwargs), tag_name='h4'))

    def h4s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='h4'))

    def h5(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(self._extract_selector(*args, **kwargs), tag_name='h5'))

    def h5s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='h5'))

    def h6(self, *args, **kwargs):
        from .elements.html_elements import Heading
        return Heading(self, dict(self._extract_selector(*args, **kwargs), tag_name='h6'))

    def h6s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        return HeadingCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='h6'))

    def head(self, *args, **kwargs):
        from .elements.html_elements import Head
        return Head(self, dict(self._extract_selector(*args, **kwargs), tag_name='head'))

    def heads(self, *args, **kwargs):
        from .elements.html_elements import HeadCollection
        return HeadCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='head'))

    def header(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='header'))

    def headers(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='header'))

    def hgroup(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='hgroup'))

    def hgroups(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='hgroup'))

    def hidden(self, *args, **kwargs):
        from .elements.hidden import Hidden
        return Hidden(self, dict(self._extract_selector(*args, **kwargs), tag_name='input',
                                 type='hidden'))

    def hiddens(self, *args, **kwargs):
        from .elements.hidden import HiddenCollection
        return HiddenCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='input', type='hidden'))

    def hr(self, *args, **kwargs):
        from .elements.html_elements import HR
        return HR(self, dict(self._extract_selector(*args, **kwargs), tag_name='hr'))

    def hrs(self, *args, **kwargs):
        from .elements.html_elements import HRCollection
        return HRCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='hr'))

    def html(self, *args, **kwargs):
        from .elements.html_elements import Html
        return Html(self, dict(self._extract_selector(*args, **kwargs), tag_name='html'))

    def htmls(self, *args, **kwargs):
        from .elements.html_elements import HtmlCollection
        return HtmlCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='html'))

    # Plural of 'i' cannot be a method name, use ital/itals instead
    def ital(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='i'))

    def itals(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='i'))

    def iframe(self, *args, **kwargs):
        from .elements.i_frame import IFrame
        return IFrame(self, dict(self._extract_selector(*args, **kwargs), tag_name='iframe'))

    def iframes(self, *args, **kwargs):
        from .elements.html_elements import IFrameCollection
        return IFrameCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='iframe'))

    def img(self, *args, **kwargs):
        from .elements.image import Image
        return Image(self, dict(self._extract_selector(*args, **kwargs), tag_name='img'))

    def imgs(self, *args, **kwargs):
        from .elements.html_elements import ImageCollection
        return ImageCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='img'))

    def input(self, *args, **kwargs):
        from .elements.html_elements import Input
        return Input(self, dict(self._extract_selector(*args, **kwargs), tag_name='input'))

    def inputs(self, *args, **kwargs):
        from .elements.html_elements import InputCollection
        return InputCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='input'))

    def ins(self, *args, **kwargs):
        from .elements.html_elements import Mod
        return Mod(self, dict(self._extract_selector(*args, **kwargs), tag_name='ins'))

    def inses(self, *args, **kwargs):
        from .elements.html_elements import ModCollection
        return ModCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='ins'))

    def kbd(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='kbd'))

    def kbds(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='kbd'))

    def keygen(self, *args, **kwargs):
        from .elements.html_elements import Keygen
        return Keygen(self, dict(self._extract_selector(*args, **kwargs), tag_name='keygen'))

    def keygens(self, *args, **kwargs):
        from .elements.html_elements import KeygenCollection
        return KeygenCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='keygen'))

    def label(self, *args, **kwargs):
        from .elements.html_elements import Label
        return Label(self, dict(self._extract_selector(*args, **kwargs), tag_name='label'))

    def labels(self, *args, **kwargs):
        from .elements.html_elements import LabelCollection
        return LabelCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='label'))

    def legend(self, *args, **kwargs):
        from .elements.html_elements import Legend
        return Legend(self, dict(self._extract_selector(*args, **kwargs), tag_name='legend'))

    def legends(self, *args, **kwargs):
        from .elements.html_elements import LegendCollection
        return LegendCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='legend'))

    def li(self, *args, **kwargs):
        from .elements.html_elements import LI
        return LI(self, dict(self._extract_selector(*args, **kwargs), tag_name='li'))

    def lis(self, *args, **kwargs):
        from .elements.html_elements import LICollection
        return LICollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='li'))

    def main(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='main'))

    def mains(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='main'))

    def map(self, *args, **kwargs):
        from .elements.html_elements import Map
        return Map(self, dict(self._extract_selector(*args, **kwargs), tag_name='map'))

    def maps(self, *args, **kwargs):
        from .elements.html_elements import MapCollection
        return MapCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='map'))

    def mark(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='mark'))

    def marks(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='mark'))

    def menu(self, *args, **kwargs):
        from .elements.html_elements import Menu
        return Menu(self, dict(self._extract_selector(*args, **kwargs), tag_name='menu'))

    def menus(self, *args, **kwargs):
        from .elements.html_elements import MenuCollection
        return MenuCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='menu'))

    def menuitem(self, *args, **kwargs):
        from .elements.html_elements import MenuItem
        return MenuItem(self, dict(self._extract_selector(*args, **kwargs), tag_name='menuitem'))

    def menuitems(self, *args, **kwargs):
        from .elements.html_elements import MenuItemCollection
        return MenuItemCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='menuitem'))

    def meta(self, *args, **kwargs):
        from .elements.html_elements import Meta
        return Meta(self, dict(self._extract_selector(*args, **kwargs), tag_name='meta'))

    def metas(self, *args, **kwargs):
        from .elements.html_elements import MetaCollection
        return MetaCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='meta'))

    def meter(self, *args, **kwargs):
        from .elements.html_elements import Meter
        return Meter(self, dict(self._extract_selector(*args, **kwargs), tag_name='meter'))

    def meters(self, *args, **kwargs):
        from .elements.html_elements import MeterCollection
        return MeterCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='meter'))

    def nav(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='nav'))

    def navs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='nav'))

    def noscript(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='noscript'))

    def noscripts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='noscript'))

    def object(self, *args, **kwargs):
        from .elements.html_elements import Object
        return Object(self, dict(self._extract_selector(*args, **kwargs), tag_name='object'))

    def objects(self, *args, **kwargs):
        from .elements.html_elements import ObjectCollection
        return ObjectCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='object'))

    def ol(self, *args, **kwargs):
        from .elements.list import OList
        return OList(self, dict(self._extract_selector(*args, **kwargs), tag_name='ol'))

    def ols(self, *args, **kwargs):
        from .elements.html_elements import OListCollection
        return OListCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='ol'))

    def optgroup(self, *args, **kwargs):
        from .elements.html_elements import OptGroup
        return OptGroup(self, dict(self._extract_selector(*args, **kwargs), tag_name='optgroup'))

    def optgroups(self, *args, **kwargs):
        from .elements.html_elements import OptGroupCollection
        return OptGroupCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='optgroup'))

    def option(self, *args, **kwargs):
        from .elements.option import Option
        return Option(self, dict(self._extract_selector(*args, **kwargs), tag_name='option'))

    def options(self, *args, **kwargs):
        from .elements.html_elements import OptionCollection
        return OptionCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='option'))

    def output(self, *args, **kwargs):
        from .elements.html_elements import Output
        return Output(self, dict(self._extract_selector(*args, **kwargs), tag_name='output'))

    def outputs(self, *args, **kwargs):
        from .elements.html_elements import OutputCollection
        return OutputCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='output'))

    def p(self, *args, **kwargs):
        from .elements.html_elements import Paragraph
        return Paragraph(self, dict(self._extract_selector(*args, **kwargs), tag_name='p'))

    def ps(self, *args, **kwargs):
        from .elements.html_elements import ParagraphCollection
        return ParagraphCollection(self, dict(self._extract_selector(*args, **kwargs),
                                              tag_name='p'))

    def param(self, *args, **kwargs):
        from .elements.html_elements import Param
        return Param(self, dict(self._extract_selector(*args, **kwargs), tag_name='param'))

    def params(self, *args, **kwargs):
        from .elements.html_elements import ParamCollection
        return ParamCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='param'))

    def pre(self, *args, **kwargs):
        from .elements.html_elements import Pre
        return Pre(self, dict(self._extract_selector(*args, **kwargs), tag_name='pre'))

    def pres(self, *args, **kwargs):
        from .elements.html_elements import PreCollection
        return PreCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='pre'))

    def progress(self, *args, **kwargs):
        from .elements.html_elements import Progress
        return Progress(self, dict(self._extract_selector(*args, **kwargs), tag_name='progress'))

    def progresses(self, *args, **kwargs):
        from .elements.html_elements import ProgressCollection
        return ProgressCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='progress'))

    def q(self, *args, **kwargs):
        from .elements.html_elements import Quote
        return Quote(self, dict(self._extract_selector(*args, **kwargs), tag_name='q'))

    def qs(self, *args, **kwargs):
        from .elements.html_elements import QuoteCollection
        return QuoteCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='q'))

    def radio(self, *args, **kwargs):
        from .elements.radio import Radio
        return Radio(self, dict(self._extract_selector(*args, **kwargs), tag_name='input',
                                type='radio'))

    def radios(self, *args, **kwargs):
        from .elements.radio import RadioCollection
        return RadioCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='input', type='radio'))

    def rp(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='rp'))

    def rps(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='rp'))

    def rt(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='rt'))

    def rts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='rt'))

    def ruby(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='ruby'))

    def rubies(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='ruby'))

    def s(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='s'))

    def ss(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='s'))

    def samp(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='samp'))

    def samps(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='samp'))

    def script(self, *args, **kwargs):
        from .elements.html_elements import Script
        return Script(self, dict(self._extract_selector(*args, **kwargs), tag_name='script'))

    def scripts(self, *args, **kwargs):
        from .elements.html_elements import ScriptCollection
        return ScriptCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='script'))

    def section(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='section'))

    def sections(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='section'))

    def select(self, *args, **kwargs):
        from .elements.select import Select
        return Select(self, dict(self._extract_selector(*args, **kwargs), tag_name='select'))

    select_list = select

    def selects(self, *args, **kwargs):
        from .elements.html_elements import SelectCollection
        return SelectCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='select'))

    select_lists = selects

    def small(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='small'))

    def smalls(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='small'))

    def source(self, *args, **kwargs):
        from .elements.html_elements import Source
        return Source(self, dict(self._extract_selector(*args, **kwargs), tag_name='source'))

    def sources(self, *args, **kwargs):
        from .elements.html_elements import SourceCollection
        return SourceCollection(self, dict(self._extract_selector(*args, **kwargs),
                                           tag_name='source'))

    def span(self, *args, **kwargs):
        from .elements.html_elements import Span
        return Span(self, dict(self._extract_selector(*args, **kwargs), tag_name='span'))

    def spans(self, *args, **kwargs):
        from .elements.html_elements import SpanCollection
        return SpanCollection(self, dict(self._extract_selector(*args, **kwargs),
                                         tag_name='span'))

    def strong(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='strong'))

    def strongs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='strong'))

    def style(self, *args, **kwargs):
        from .elements.html_elements import Style
        return Style(self, dict(self._extract_selector(*args, **kwargs), tag_name='style'))

    def styles(self, *args, **kwargs):
        from .elements.html_elements import StyleCollection
        return StyleCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='style'))

    def sub(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='sub'))

    def subs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='sub'))

    def summary(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='summary'))

    def summaries(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='summary'))

    def sup(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='sup'))

    def sups(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='sup'))

    def table(self, *args, **kwargs):
        from .elements.table import Table
        return Table(self, dict(self._extract_selector(*args, **kwargs), tag_name='table'))

    def tables(self, *args, **kwargs):
        from .elements.html_elements import TableCollection
        return TableCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='table'))

    def tbody(self, *args, **kwargs):
        from .elements.table_section import TableSection
        return TableSection(self, dict(self._extract_selector(*args, **kwargs), tag_name='tbody'))

    def tbodys(self, *args, **kwargs):
        from .elements.html_elements import TableSectionCollection
        return TableSectionCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                 tag_name='tbody'))

    def td(self, *args, **kwargs):
        from .elements.table_data_cell import TableDataCell
        return TableDataCell(self, dict(self._extract_selector(*args, **kwargs), tag_name='td'))

    def tds(self, *args, **kwargs):
        from .elements.html_elements import TableDataCellCollection
        return TableDataCellCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                  tag_name='td'))

    def template(self, *args, **kwargs):
        from .elements.html_elements import Template
        return Template(self, dict(self._extract_selector(*args, **kwargs), tag_name='template'))

    def templates(self, *args, **kwargs):
        from .elements.html_elements import TemplateCollection
        return TemplateCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='template'))

    def textarea(self, *args, **kwargs):
        from .elements.text_area import TextArea
        return TextArea(self, dict(self._extract_selector(*args, **kwargs), tag_name='textarea'))

    def textareas(self, *args, **kwargs):
        from .elements.html_elements import TextAreaCollection
        return TextAreaCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='textarea'))

    def text_field(self, *args, **kwargs):
        from .elements.text_field import TextField
        return TextField(self, dict(self._extract_selector(*args, **kwargs), tag_name='input'))

    def text_fields(self, *args, **kwargs):
        from .elements.text_field import TextFieldCollection
        return TextFieldCollection(self, dict(self._extract_selector(*args, **kwargs),
                                              tag_name='input'))

    def tfoot(self, *args, **kwargs):
        from .elements.table_section import TableSection
        return TableSection(self, dict(self._extract_selector(*args, **kwargs), tag_name='tfoot'))

    def tfoots(self, *args, **kwargs):
        from .elements.table_section import TableSectionCollection
        return TableSectionCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                 tag_name='tfoot'))

    def th(self, *args, **kwargs):
        from .elements.html_elements import TableHeaderCell
        return TableHeaderCell(self, dict(self._extract_selector(*args, **kwargs), tag_name='th'))

    def ths(self, *args, **kwargs):
        from .elements.html_elements import TableHeaderCellCollection
        return TableHeaderCellCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                    tag_name='th'))

    def thead(self, *args, **kwargs):
        from .elements.table_section import TableSection
        return TableSection(self, dict(self._extract_selector(*args, **kwargs), tag_name='thead'))

    def theads(self, *args, **kwargs):
        from .elements.table_section import TableSectionCollection
        return TableSectionCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                 tag_name='thead'))

    def time(self, *args, **kwargs):
        from .elements.html_elements import Time
        return Time(self, dict(self._extract_selector(*args, **kwargs), tag_name='time'))

    def times(self, *args, **kwargs):
        from .elements.html_elements import TimeCollection
        return TimeCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='time'))

    def title(self, *args, **kwargs):
        from .elements.html_elements import Title
        return Title(self, dict(self._extract_selector(*args, **kwargs), tag_name='title'))

    def titles(self, *args, **kwargs):
        from .elements.html_elements import TitleCollection
        return TitleCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='title'))

    def tr(self, *args, **kwargs):
        from .elements.table_row import TableRow
        return TableRow(self, dict(self._extract_selector(*args, **kwargs), tag_name='tr'))

    def trs(self, *args, **kwargs):
        from .elements.html_elements import TableRowCollection
        return TableRowCollection(self, dict(self._extract_selector(*args, **kwargs),
                                             tag_name='tr'))

    def track(self, *args, **kwargs):
        from .elements.html_elements import Track
        return Track(self, dict(self._extract_selector(*args, **kwargs), tag_name='track'))

    def tracks(self, *args, **kwargs):
        from .elements.html_elements import TrackCollection
        return TrackCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='track'))

    def u(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='u'))

    def us(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='u'))

    def ul(self, *args, **kwargs):
        from .elements.list import UList
        return UList(self, dict(self._extract_selector(*args, **kwargs), tag_name='ul'))

    def uls(self, *args, **kwargs):
        from .elements.html_elements import UListCollection
        return UListCollection(self, dict(self._extract_selector(*args, **kwargs), tag_name='ul'))

    def var(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='var'))

    def vars(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='var'))

    def video(self, *args, **kwargs):
        from .elements.html_elements import Video
        return Video(self, dict(self._extract_selector(*args, **kwargs), tag_name='video'))

    def videos(self, *args, **kwargs):
        from .elements.html_elements import VideoCollection
        return VideoCollection(self, dict(self._extract_selector(*args, **kwargs),
                                          tag_name='video'))

    def wbr(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, dict(self._extract_selector(*args, **kwargs), tag_name='wbr'))

    def wbrs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, dict(self._extract_selector(*args, **kwargs),
                                                tag_name='wbr'))
