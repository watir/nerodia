class Container(object):
    # TODO: include XpathSupport
    # TODO: include Atoms

    def element(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, self._extract_selector(*args, **kwargs))

    # private

    def _extract_selector(self, *args, **kwargs):
        if args and len(args) == 2:
            return {args[0]: args[1]}
        elif len(kwargs) > 1:
            return kwargs
        elif len(kwargs) == 0:
            return {}

        raise ValueError('expected kwargs, got {}'.format(kwargs))

    # Plural of 'a' cannot be a method name, use link/links instead
    def link(self, *args, **kwargs):
        from .elements.link import Anchor
        return Anchor(self, self._extract_selector(tag_name='a', *args, **kwargs))

    def links(self, *args, **kwargs):
        from .elements.html_elements import AnchorCollection
        return AnchorCollection(self, self._extract_selector(tag_name='a', *args, **kwargs))

    def abbr(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, self._extract_selector(tag_name='abbr', *args, **kwargs))

    def abbrs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self, self._extract_selector(tag_name='abbr', *args, **kwargs))

    def address(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, self._extract_selector(tag_name='address', *args, **kwargs))

    def addresses(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection(self,
                                     self._extract_selector(tag_name='address', *args, **kwargs))

    def area(self, *args, **kwargs):
        from .elements.area import Area
        return Area(self, self._extract_selector(tag_name='area', *args, **kwargs))

    def areas(self, *args, **kwargs):
        from .elements.html_elements import AreaCollection
        return AreaCollection(self, self._extract_selector(tag_name='area', *args, **kwargs))

    def article(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        return HTMLElement(self, self._extract_selector(tag_name='article', *args, **kwargs))

    def articles(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        return HTMLElementCollection.new(self, self._extract_selector(tag_name='article', *args,
                                                                      **kwargs))

    def aside(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement.new(self, self._extract_selector(tag_name='aside', *args, **kwargs))

    def asides(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='aside', *args, **kwargs))

    def audio(self, *args, **kwargs):
        from .elements.html_elements import Audio
        Audio(self, self._extract_selector(tag_name='audio', *args, **kwargs))

    def audios(self, *args, **kwargs):
        from .elements.html_elements import AudioCollection
        AudioCollection(self, self._extract_selector(tag_name='audio', *args, **kwargs))

    def b(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='b', *args, **kwargs))

    def bs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='b', *args, **kwargs))

    def base(self, *args, **kwargs):
        from .elements.html_elements import Base
        Base(self, self._extract_selector(tag_name='base', *args, **kwargs))

    def bases(self, *args, **kwargs):
        from .elements.html_elements import BaseCollection
        BaseCollection(self, self._extract_selector(tag_name='base', *args, **kwargs))

    def bdi(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='bdi', *args, **kwargs))

    def bdis(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='bdi', *args, **kwargs))

    def bdo(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='bdo', *args, **kwargs))

    def bdos(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='bdo', *args, **kwargs))

    def blockquote(self, *args, **kwargs):
        from .elements.html_elements import Quote
        Quote(self, self._extract_selector(tag_name='blockquote', *args, **kwargs))

    def blockquotes(self, *args, **kwargs):
        from .elements.html_elements import QuoteCollection
        QuoteCollection(self, self._extract_selector(tag_name='blockquote', *args, **kwargs))

    def body(self, *args, **kwargs):
        from .elements.html_elements import Body
        Body(self, self._extract_selector(tag_name='body', *args, **kwargs))

    def bodys(self, *args, **kwargs):
        from .elements.html_elements import BodyCollection
        BodyCollection(self, self._extract_selector(tag_name='body', *args, **kwargs))

    def br(self, *args, **kwargs):
        from .elements.html_elements import BR
        BR(self, self._extract_selector(tag_name='br', *args, **kwargs))

    def brs(self, *args, **kwargs):
        from .elements.html_elements import BRCollection
        BRCollection(self, self._extract_selector(tag_name='br', *args, **kwargs))

    def button(self, *args, **kwargs):
        from .elements.button import Button
        Button(self, self._extract_selector(tag_name='button', *args, **kwargs))

    def buttons(self, *args, **kwargs):
        from .elements.html_elements import ButtonCollection
        ButtonCollection(self, self._extract_selector(tag_name='button', *args, **kwargs))

    def canvas(self, *args, **kwargs):
        from .elements.html_elements import Canvas
        Canvas(self, self._extract_selector(tag_name='canvas', *args, **kwargs))

    def canvases(self, *args, **kwargs):
        from .elements.html_elements import CanvasCollection
        CanvasCollection(self, self._extract_selector(tag_name='canvas', *args, **kwargs))

    def caption(self, *args, **kwargs):
        from .elements.html_elements import TableCaption
        TableCaption(self, self._extract_selector(tag_name='caption', *args, **kwargs))

    def captions(self, *args, **kwargs):
        from .elements.html_elements import TableCaptionCollection
        TableCaptionCollection(self, self._extract_selector(tag_name='caption', *args, **kwargs))

    def cite(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='cite', *args, **kwargs))

    def cites(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='cite', *args, **kwargs))

    def code(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='code', *args, **kwargs))

    def codes(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='code', *args, **kwargs))

    def col(self, *args, **kwargs):
        from .elements.html_elements import TableCol
        TableCol(self, self._extract_selector(tag_name='col', *args, **kwargs))

    def cols(self, *args, **kwargs):
        from .elements.html_elements import TableColCollection
        TableColCollection(self, self._extract_selector(tag_name='col', *args, **kwargs))

    def colgroup(self, *args, **kwargs):
        from .elements.html_elements import TableCol
        TableCol(self, self._extract_selector(tag_name='colgroup', *args, **kwargs))

    def colgroups(self, *args, **kwargs):
        from .elements.html_elements import TableColCollection
        TableColCollection(self, self._extract_selector(tag_name='colgroup', *args, **kwargs))

    def data(self, *args, **kwargs):
        from .elements.html_elements import Data
        Data(self, self._extract_selector(tag_name='data', *args, **kwargs))

    def datas(self, *args, **kwargs):
        from .elements.html_elements import DataCollection
        DataCollection(self, self._extract_selector(tag_name='data', *args, **kwargs))

    def datalist(self, *args, **kwargs):
        from .elements.html_elements import DataList
        DataList(self, self._extract_selector(tag_name='datalist', *args, **kwargs))

    def datalists(self, *args, **kwargs):
        from .elements.html_elements import DataListCollection
        DataListCollection(self, self._extract_selector(tag_name='datalist', *args, **kwargs))

    def dd(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='dd', *args, **kwargs))

    def dds(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='dd', *args, **kwargs))

    # 'del' is an invalid method name, use delete/deletes instead
    def delete(self, *args, **kwargs):
        from .elements.html_elements import Mod
        Mod(self, self._extract_selector(tag_name='del', *args, **kwargs))

    def deletes(self, *args, **kwargs):
        from .elements.html_elements import ModCollection
        ModCollection(self, self._extract_selector(tag_name='del', *args, **kwargs))

    def details(self, *args, **kwargs):
        from .elements.html_elements import Details
        Details(self, self._extract_selector(tag_name='details', *args, **kwargs))

    def detailses(self, *args, **kwargs):
        from .elements.html_elements import DetailsCollection
        DetailsCollection(self, self._extract_selector(tag_name='details', *args, **kwargs))

    def dfn(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='dfn', *args, **kwargs))

    def dfns(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='dfn', *args, **kwargs))

    def dialog(self, *args, **kwargs):
        from .elements.html_elements import Dialog
        Dialog(self, self._extract_selector(tag_name='dialog', *args, **kwargs))

    def dialogs(self, *args, **kwargs):
        from .elements.html_elements import DialogCollection
        DialogCollection(self, self._extract_selector(tag_name='dialog', *args, **kwargs))

    def div(self, *args, **kwargs):
        from .elements.html_elements import Div
        Div(self, self._extract_selector(tag_name='div', *args, **kwargs))

    def divs(self, *args, **kwargs):
        from .elements.html_elements import DivCollection
        DivCollection(self, self._extract_selector(tag_name='div', *args, **kwargs))

    def dl(self, *args, **kwargs):
        from .elements.dlist import DList
        DList(self, self._extract_selector(tag_name='dl', *args, **kwargs))

    def dls(self, *args, **kwargs):
        from .elements.html_elements import DListCollection
        DListCollection(self, self._extract_selector(tag_name='dl', *args, **kwargs))

    def dt(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='dt', *args, **kwargs))

    def dts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='dt', *args, **kwargs))

    def em(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='em', *args, **kwargs))

    def ems(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='em', *args, **kwargs))

    def embed(self, *args, **kwargs):
        from .elements.html_elements import Embed
        Embed(self, self._extract_selector(tag_name='embed', *args, **kwargs))

    def embeds(self, *args, **kwargs):
        from .elements.html_elements import EmbedCollection
        EmbedCollection(self, self._extract_selector(tag_name='embed', *args, **kwargs))

    def fieldset(self, *args, **kwargs):
        from .elements.html_elements import FieldSet
        FieldSet(self, self._extract_selector(tag_name='fieldset', *args, **kwargs))

    def fieldsets(self, *args, **kwargs):
        from .elements.html_elements import FieldSetCollection
        FieldSetCollection(self, self._extract_selector(tag_name='fieldset', *args, **kwargs))

    def figcaption(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='figcaption', *args, **kwargs))

    def figcaptions(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='figcaption', *args,
                                                           **kwargs))

    def figure(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='figure', *args, **kwargs))

    def figures(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='figure', *args, **kwargs))

    def footer(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='footer', *args, **kwargs))

    def footers(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='footer', *args, **kwargs))

    def form(self, *args, **kwargs):
        from .elements.form import Form
        Form(self, self._extract_selector(tag_name='form', *args, **kwargs))

    def forms(self, *args, **kwargs):
        from .elements.html_elements import FormCollection
        FormCollection(self, self._extract_selector(tag_name='form', *args, **kwargs))

    def frameset(self, *args, **kwargs):
        from .elements.html_elements import FrameSet
        FrameSet(self, self._extract_selector(tag_name='frameset', *args, **kwargs))

    def framesets(self, *args, **kwargs):
        from .elements.html_elements import FrameSetCollection
        FrameSetCollection(self, self._extract_selector(tag_name='frameset', *args, **kwargs))

    def h1(self, *args, **kwargs):
        from .elements.html_elements import Heading
        Heading(self, self._extract_selector(tag_name='h1', *args, **kwargs))

    def h1s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        HeadingCollection(self, self._extract_selector(tag_name='h1', *args, **kwargs))

    def h2(self, *args, **kwargs):
        from .elements.html_elements import Heading
        Heading(self, self._extract_selector(tag_name='h2', *args, **kwargs))

    def h2s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        HeadingCollection(self, self._extract_selector(tag_name='h2', *args, **kwargs))

    def h3(self, *args, **kwargs):
        from .elements.html_elements import Heading
        Heading(self, self._extract_selector(tag_name='h3', *args, **kwargs))

    def h3s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        HeadingCollection(self, self._extract_selector(tag_name='h3', *args, **kwargs))

    def h4(self, *args, **kwargs):
        from .elements.html_elements import Heading
        Heading(self, self._extract_selector(tag_name='h4', *args, **kwargs))

    def h4s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        HeadingCollection(self, self._extract_selector(tag_name='h4', *args, **kwargs))

    def h5(self, *args, **kwargs):
        from .elements.html_elements import Heading
        Heading(self, self._extract_selector(tag_name='h5', *args, **kwargs))

    def h5s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        HeadingCollection(self, self._extract_selector(tag_name='h5', *args, **kwargs))

    def h6(self, *args, **kwargs):
        from .elements.html_elements import Heading
        Heading(self, self._extract_selector(tag_name='h6', *args, **kwargs))

    def h6s(self, *args, **kwargs):
        from .elements.html_elements import HeadingCollection
        HeadingCollection(self, self._extract_selector(tag_name='h6', *args, **kwargs))

    def head(self, *args, **kwargs):
        from .elements.html_elements import Head
        Head(self, self._extract_selector(tag_name='head', *args, **kwargs))

    def heads(self, *args, **kwargs):
        from .elements.html_elements import HeadCollection
        HeadCollection(self, self._extract_selector(tag_name='head', *args, **kwargs))

    def header(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='header', *args, **kwargs))

    def headers(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='header', *args, **kwargs))

    def hgroup(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='hgroup', *args, **kwargs))

    def hgroups(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='hgroup', *args, **kwargs))

    def hr(self, *args, **kwargs):
        from .elements.html_elements import HR
        HR(self, self._extract_selector(tag_name='hr', *args, **kwargs))

    def hrs(self, *args, **kwargs):
        from .elements.html_elements import HRCollection
        HRCollection(self, self._extract_selector(tag_name='hr', *args, **kwargs))

    def html(self, *args, **kwargs):
        from .elements.html_elements import Html
        Html(self, self._extract_selector(tag_name='html', *args, **kwargs))

    def htmls(self, *args, **kwargs):
        from .elements.html_elements import HtmlCollection
        HtmlCollection(self, self._extract_selector(tag_name='html', *args, **kwargs))

    # Plural of 'i' cannot be a method name, use ital/itals instead
    def ital(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='i', *args, **kwargs))

    def itals(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='i', *args, **kwargs))

    def iframe(self, *args, **kwargs):
        from .elements.iframe import IFrame
        IFrame(self, self._extract_selector(tag_name='iframe', *args, **kwargs))

    def iframes(self, *args, **kwargs):
        from .elements.html_elements import IFrameCollection
        IFrameCollection(self, self._extract_selector(tag_name='iframe', *args, **kwargs))

    def img(self, *args, **kwargs):
        from .elements.image import Image
        Image(self, self._extract_selector(tag_name='img', *args, **kwargs))

    def imgs(self, *args, **kwargs):
        from .elements.html_elements import ImageCollection
        ImageCollection(self, self._extract_selector(tag_name='img', *args, **kwargs))

    def input(self, *args, **kwargs):
        from .elements.input import Input
        Input(self, self._extract_selector(tag_name='input', *args, **kwargs))

    def inputs(self, *args, **kwargs):
        from .elements.html_elements import InputCollection
        InputCollection(self, self._extract_selector(tag_name='input', *args, **kwargs))

    def ins(self, *args, **kwargs):
        from .elements.html_elements import Mod
        Mod(self, self._extract_selector(tag_name='ins', *args, **kwargs))

    def inses(self, *args, **kwargs):
        from .elements.html_elements import ModCollection
        ModCollection(self, self._extract_selector(tag_name='ins', *args, **kwargs))

    def kbd(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='kbd', *args, **kwargs))

    def kbds(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='kbd', *args, **kwargs))

    def keygen(self, *args, **kwargs):
        from .elements.html_elements import Keygen
        Keygen(self, self._extract_selector(tag_name='keygen', *args, **kwargs))

    def keygens(self, *args, **kwargs):
        from .elements.html_elements import KeygenCollection
        KeygenCollection(self, self._extract_selector(tag_name='keygen', *args, **kwargs))

    def label(self, *args, **kwargs):
        from .elements.html_elements import Label
        Label(self, self._extract_selector(tag_name='label', *args, **kwargs))

    def labels(self, *args, **kwargs):
        from .elements.html_elements import LabelCollection
        LabelCollection(self, self._extract_selector(tag_name='label', *args, **kwargs))

    def legend(self, *args, **kwargs):
        from .elements.html_elements import Legend
        Legend(self, self._extract_selector(tag_name='legend', *args, **kwargs))

    def legends(self, *args, **kwargs):
        from .elements.html_elements import LegendCollection
        LegendCollection(self, self._extract_selector(tag_name='legend', *args, **kwargs))

    def li(self, *args, **kwargs):
        from .elements.html_elements import LI
        LI(self, self._extract_selector(tag_name='li', *args, **kwargs))

    def lis(self, *args, **kwargs):
        from .elements.html_elements import LICollection
        LICollection(self, self._extract_selector(tag_name='li', *args, **kwargs))

    def main(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='main', *args, **kwargs))

    def mains(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='main', *args, **kwargs))

    def map(self, *args, **kwargs):
        from .elements.html_elements import Map
        Map(self, self._extract_selector(tag_name='map', *args, **kwargs))

    def maps(self, *args, **kwargs):
        from .elements.html_elements import MapCollection
        MapCollection(self, self._extract_selector(tag_name='map', *args, **kwargs))

    def mark(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='mark', *args, **kwargs))

    def marks(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='mark', *args, **kwargs))

    def menu(self, *args, **kwargs):
        from .elements.html_elements import Menu
        Menu(self, self._extract_selector(tag_name='menu', *args, **kwargs))

    def menus(self, *args, **kwargs):
        from .elements.html_elements import MenuCollection
        MenuCollection(self, self._extract_selector(tag_name='menu', *args, **kwargs))

    def menuitem(self, *args, **kwargs):
        from .elements.html_elements import MenuItem
        MenuItem(self, self._extract_selector(tag_name='menuitem', *args, **kwargs))

    def menuitems(self, *args, **kwargs):
        from .elements.html_elements import MenuItemCollection
        MenuItemCollection(self, self._extract_selector(tag_name='menuitem', *args, **kwargs))

    def meta(self, *args, **kwargs):
        from .elements.html_elements import Meta
        Meta(self, self._extract_selector(tag_name='meta', *args, **kwargs))

    def metas(self, *args, **kwargs):
        from .elements.html_elements import MetaCollection
        MetaCollection(self, self._extract_selector(tag_name='meta', *args, **kwargs))

    def meter(self, *args, **kwargs):
        from .elements.html_elements import Meter
        Meter(self, self._extract_selector(tag_name='meter', *args, **kwargs))

    def meters(self, *args, **kwargs):
        from .elements.html_elements import MeterCollection
        MeterCollection(self, self._extract_selector(tag_name='meter', *args, **kwargs))

    def nav(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='nav', *args, **kwargs))

    def navs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='nav', *args, **kwargs))

    def noscript(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='noscript', *args, **kwargs))

    def noscripts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='noscript', *args, **kwargs))

    def object(self, *args, **kwargs):
        from .elements.html_elements import Object
        Object(self, self._extract_selector(tag_name='object', *args, **kwargs))

    def objects(self, *args, **kwargs):
        from .elements.html_elements import ObjectCollection
        ObjectCollection(self, self._extract_selector(tag_name='object', *args, **kwargs))

    def ol(self, *args, **kwargs):
        from .elements.html_elements import OList
        OList(self, self._extract_selector(tag_name='ol', *args, **kwargs))

    def ols(self, *args, **kwargs):
        from .elements.html_elements import OListCollection
        OListCollection(self, self._extract_selector(tag_name='ol', *args, **kwargs))

    def optgroup(self, *args, **kwargs):
        from .elements.html_elements import OptGroup
        OptGroup(self, self._extract_selector(tag_name='optgroup', *args, **kwargs))

    def optgroups(self, *args, **kwargs):
        from .elements.html_elements import OptGroupCollection
        OptGroupCollection(self, self._extract_selector(tag_name='optgroup', *args, **kwargs))

    def option(self, *args, **kwargs):
        from .elements.option import Option
        Option(self, self._extract_selector(tag_name='option', *args, **kwargs))

    def options(self, *args, **kwargs):
        from .elements.html_elements import OptionCollection
        OptionCollection(self, self._extract_selector(tag_name='option', *args, **kwargs))

    def output(self, *args, **kwargs):
        from .elements.html_elements import Output
        Output(self, self._extract_selector(tag_name='output', *args, **kwargs))

    def outputs(self, *args, **kwargs):
        from .elements.html_elements import OutputCollection
        OutputCollection(self, self._extract_selector(tag_name='output', *args, **kwargs))

    def p(self, *args, **kwargs):
        from .elements.html_elements import Paragraph
        Paragraph(self, self._extract_selector(tag_name='p', *args, **kwargs))

    def ps(self, *args, **kwargs):
        from .elements.html_elements import ParagraphCollection
        ParagraphCollection(self, self._extract_selector(tag_name='p', *args, **kwargs))

    def param(self, *args, **kwargs):
        from .elements.html_elements import Param
        Param(self, self._extract_selector(tag_name='param', *args, **kwargs))

    def params(self, *args, **kwargs):
        from .elements.html_elements import ParamCollection
        ParamCollection(self, self._extract_selector(tag_name='param', *args, **kwargs))

    def pre(self, *args, **kwargs):
        from .elements.html_elements import Pre
        Pre(self, self._extract_selector(tag_name='pre', *args, **kwargs))

    def pres(self, *args, **kwargs):
        from .elements.html_elements import PreCollection
        PreCollection(self, self._extract_selector(tag_name='pre', *args, **kwargs))

    def progress(self, *args, **kwargs):
        from .elements.html_elements import Progress
        Progress(self, self._extract_selector(tag_name='progress', *args, **kwargs))

    def progresses(self, *args, **kwargs):
        from .elements.html_elements import ProgressCollection
        ProgressCollection(self, self._extract_selector(tag_name='progress', *args, **kwargs))

    def q(self, *args, **kwargs):
        from .elements.html_elements import Quote
        Quote(self, self._extract_selector(tag_name='q', *args, **kwargs))

    def qs(self, *args, **kwargs):
        from .elements.html_elements import QuoteCollection
        QuoteCollection(self, self._extract_selector(tag_name='q', *args, **kwargs))

    def rp(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='rp', *args, **kwargs))

    def rps(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='rp', *args, **kwargs))

    def rt(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='rt', *args, **kwargs))

    def rts(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='rt', *args, **kwargs))

    def ruby(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='ruby', *args, **kwargs))

    def rubies(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='ruby', *args, **kwargs))

    def s(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='s', *args, **kwargs))

    def ss(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='s', *args, **kwargs))

    def samp(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='samp', *args, **kwargs))

    def samps(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='samp', *args, **kwargs))

    def script(self, *args, **kwargs):
        from .elements.html_elements import Script
        Script(self, self._extract_selector(tag_name='script', *args, **kwargs))

    def scripts(self, *args, **kwargs):
        from .elements.html_elements import ScriptCollection
        ScriptCollection(self, self._extract_selector(tag_name='script', *args, **kwargs))

    def section(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='section', *args, **kwargs))

    def sections(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='section', *args, **kwargs))

    def select(self, *args, **kwargs):
        from .elements.select import Select
        Select(self, self._extract_selector(tag_name='select', *args, **kwargs))

    def selects(self, *args, **kwargs):
        from .elements.html_elements import SelectCollection
        SelectCollection(self, self._extract_selector(tag_name='select', *args, **kwargs))

    def small(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='small', *args, **kwargs))

    def smalls(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='small', *args, **kwargs))

    def source(self, *args, **kwargs):
        from .elements.html_elements import Source
        Source(self, self._extract_selector(tag_name='source', *args, **kwargs))

    def sources(self, *args, **kwargs):
        from .elements.html_elements import SourceCollection
        SourceCollection(self, self._extract_selector(tag_name='source', *args, **kwargs))

    def span(self, *args, **kwargs):
        from .elements.html_elements import Span
        Span(self, self._extract_selector(tag_name='span', *args, **kwargs))

    def spans(self, *args, **kwargs):
        from .elements.html_elements import SpanCollection
        SpanCollection(self, self._extract_selector(tag_name='span', *args, **kwargs))

    def strong(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='strong', *args, **kwargs))

    def strongs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='strong', *args, **kwargs))

    def style(self, *args, **kwargs):
        from .elements.html_elements import Style
        Style(self, self._extract_selector(tag_name='style', *args, **kwargs))

    def styles(self, *args, **kwargs):
        from .elements.html_elements import StyleCollection
        StyleCollection(self, self._extract_selector(tag_name='style', *args, **kwargs))

    def sub(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='sub', *args, **kwargs))

    def subs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='sub', *args, **kwargs))

    def summary(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='summary', *args, **kwargs))

    def summaries(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='summary', *args, **kwargs))

    def sup(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='sup', *args, **kwargs))

    def sups(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='sup', *args, **kwargs))

    def table(self, *args, **kwargs):
        from .elements.table import Table
        Table(self, self._extract_selector(tag_name='table', *args, **kwargs))

    def tables(self, *args, **kwargs):
        from .elements.html_elements import TableCollection
        TableCollection(self, self._extract_selector(tag_name='table', *args, **kwargs))

    def tbody(self, *args, **kwargs):
        from .elements.table_section import TableSection
        TableSection(self, self._extract_selector(tag_name='tbody', *args, **kwargs))

    def tbodys(self, *args, **kwargs):
        from .elements.html_elements import TableSectionCollection
        TableSectionCollection(self, self._extract_selector(tag_name='tbody', *args, **kwargs))

    def td(self, *args, **kwargs):
        from .elements.html_elements import TableDataCell
        TableDataCell(self, self._extract_selector(tag_name='td', *args, **kwargs))

    def tds(self, *args, **kwargs):
        from .elements.html_elements import TableDataCellCollection
        TableDataCellCollection(self, self._extract_selector(tag_name='td', *args, **kwargs))

    def template(self, *args, **kwargs):
        from .elements.html_elements import Template
        Template(self, self._extract_selector(tag_name='template', *args, **kwargs))

    def templates(self, *args, **kwargs):
        from .elements.html_elements import TemplateCollection
        TemplateCollection(self, self._extract_selector(tag_name='template', *args, **kwargs))

    def textarea(self, *args, **kwargs):
        from .elements.text_area import TextArea
        TextArea(self, self._extract_selector(tag_name='textarea', *args, **kwargs))

    def textareas(self, *args, **kwargs):
        from .elements.html_elements import TextAreaCollection
        TextAreaCollection(self, self._extract_selector(tag_name='textarea', *args, **kwargs))

    def tfoot(self, *args, **kwargs):
        from .elements.table_section import TableSection
        TableSection(self, self._extract_selector(tag_name='tfoot', *args, **kwargs))

    def tfoots(self, *args, **kwargs):
        from .elements.html_elements import TableSectionCollection
        TableSectionCollection(self, self._extract_selector(tag_name='tfoot', *args, **kwargs))

    def th(self, *args, **kwargs):
        from .elements.html_elements import TableHeaderCell
        TableHeaderCell(self, self._extract_selector(tag_name='th', *args, **kwargs))

    def ths(self, *args, **kwargs):
        from .elements.html_elements import TableHeaderCellCollection
        TableHeaderCellCollection(self, self._extract_selector(tag_name='th', *args, **kwargs))

    def thead(self, *args, **kwargs):
        from .elements.table_section import TableSection
        TableSection(self, self._extract_selector(tag_name='thead', *args, **kwargs))

    def theads(self, *args, **kwargs):
        from .elements.html_elements import TableSectionCollection
        TableSectionCollection(self, self._extract_selector(tag_name='thead', *args, **kwargs))

    def time(self, *args, **kwargs):
        from .elements.html_elements import Time
        Time(self, self._extract_selector(tag_name='time', *args, **kwargs))

    def times(self, *args, **kwargs):
        from .elements.html_elements import TimeCollection
        TimeCollection(self, self._extract_selector(tag_name='time', *args, **kwargs))

    def title(self, *args, **kwargs):
        from .elements.html_elements import Title
        Title(self, self._extract_selector(tag_name='title', *args, **kwargs))

    def titles(self, *args, **kwargs):
        from .elements.html_elements import TitleCollection
        TitleCollection(self, self._extract_selector(tag_name='title', *args, **kwargs))

    def tr(self, *args, **kwargs):
        from .elements.table_row import TableRow
        TableRow(self, self._extract_selector(tag_name='tr', *args, **kwargs))

    def trs(self, *args, **kwargs):
        from .elements.html_elements import TableRowCollection
        TableRowCollection(self, self._extract_selector(tag_name='tr', *args, **kwargs))

    def track(self, *args, **kwargs):
        from .elements.html_elements import Track
        Track(self, self._extract_selector(tag_name='track', *args, **kwargs))

    def tracks(self, *args, **kwargs):
        from .elements.html_elements import TrackCollection
        TrackCollection(self, self._extract_selector(tag_name='track', *args, **kwargs))

    def u(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='u', *args, **kwargs))

    def us(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='u', *args, **kwargs))

    def ul(self, *args, **kwargs):
        from .elements.html_elements import UList
        UList(self, self._extract_selector(tag_name='ul', *args, **kwargs))

    def uls(self, *args, **kwargs):
        from .elements.html_elements import UListCollection
        UListCollection(self, self._extract_selector(tag_name='ul', *args, **kwargs))

    def var(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='var', *args, **kwargs))

    def vars(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='var', *args, **kwargs))

    def video(self, *args, **kwargs):
        from .elements.html_elements import Video
        Video(self, self._extract_selector(tag_name='video', *args, **kwargs))

    def videos(self, *args, **kwargs):
        from .elements.html_elements import VideoCollection
        VideoCollection(self, self._extract_selector(tag_name='video', *args, **kwargs))

    def wbr(self, *args, **kwargs):
        from .elements.html_elements import HTMLElement
        HTMLElement(self, self._extract_selector(tag_name='wbr', *args, **kwargs))

    def wbrs(self, *args, **kwargs):
        from .elements.html_elements import HTMLElementCollection
        HTMLElementCollection(self, self._extract_selector(tag_name='wbr', *args, **kwargs))
