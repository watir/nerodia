import watir_snake
from watir_snake import elements


class Container(object):
    # TODO: include XpathSupport
    # TODO: include Atoms

    def element(self, *args, **kwargs):
        return elements.HTMLElement(self, self._extract_selector(*args, **kwargs))

    # private
    def _extract_selector(self, *args, **kwargs):
        if args and len(args) == 2:
            return {args[0]: args[1]}
        elif len(kwargs) > 1:
            return kwargs
        elif len(kwargs) == 0:
            return {}

        raise ValueError("expected kwargs, got {}".format(kwargs))

    # Plural of 'a' cannot be a method name, use link/links instead
    def link(self, *args, **kwargs):
        return elements.Anchor(self, self._extract_selector(tag_name='a', *args, **kwargs))

    def links(self, *args, **kwargs):
        return elements.AnchorCollection(self,
                                         self._extract_selector(tag_name='a', *args, **kwargs))

    watir_snake.tag_to_class['link'] = elements.Anchor

    def abbr(self, *args, **kwargs):
        return elements.HTMLElement(self, self._extract_selector(tag_name='abbr', *args, **kwargs))

    def abbrs(self, *args, **kwargs):
        return elements.HTMLElementCollection(self, self._extract_selector(tag_name='abbr', *args,
                                                                           **kwargs))

    watir_snake.tag_to_class['abbr'] = elements.HTMLElement

    def address(self, *args, **kwargs):
        return elements.HTMLElement(self,
                                    self._extract_selector(tag_name='address', *args, **kwargs))

    def addresses(self, *args, **kwargs):
        return elements.HTMLElementCollection(self,
                                              self._extract_selector(tag_name='address', *args,
                                                                     **kwargs))

    watir_snake.tag_to_class['address'] = elements.HTMLElement

    def area(self, *args, **kwargs):
        return elements.Area(self, self._extract_selector(tag_name='area', *args, **kwargs))

    def areas(self, *args, **kwargs):
        return elements.AreaCollection(self,
                                       self._extract_selector(tag_name='area', *args, **kwargs))

    watir_snake.tag_to_class['area'] = elements.Area

    def article(self, *args, **kwargs):
        return elements.HTMLElement(self,
                                    self._extract_selector(tag_name='article', *args, **kwargs))

    def articles(self, *args, **kwargs):
        return elements.HTMLElementCollection.new(self,
                                                  self._extract_selector(tag_name='article', *args,
                                                                         **kwargs))

    watir_snake.tag_to_class['article'] = elements.HTMLElement

    def aside(self, *args, **kwargs):
        elements.HTMLElement.new(self, self._extract_selector(tag_name='aside', *args, **kwargs))

    def asides(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name='aside', *args, **kwargs))

    watir_snake.tag_to_class['aside'] = elements.HTMLElement

    def audio(self, *args, **kwargs):
        elements.Audio(self, self._extract_selector(tag_name="audio", *args, **kwargs))

    def audios(self, *args, **kwargs):
        elements.AudioCollection(self, self._extract_selector(tag_name="audio", *args, **kwargs))

    watir_snake.tag_to_class['audio'] = elements.Audio

    def b(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="b", *args, **kwargs))

    def bs(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="b", *args, **kwargs))

    watir_snake.tag_to_class['b'] = elements.HTMLElement

    def base(self, *args, **kwargs):
        elements.Base(self, self._extract_selector(tag_name="base", *args, **kwargs))

    def bases(self, *args, **kwargs):
        elements.BaseCollection(self, self._extract_selector(tag_name="base", *args, **kwargs))

    watir_snake.tag_to_class['base'] = elements.Base

    def bdi(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="bdi", *args, **kwargs))

    def bdis(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="bdi", *args, **kwargs))

    watir_snake.tag_to_class['bdi'] = elements.HTMLElement

    def bdo(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="bdo", *args, **kwargs))

    def bdos(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="bdo", *args, **kwargs))

    watir_snake.tag_to_class['bdo'] = elements.HTMLElement

    def blockquote(self, *args, **kwargs):
        elements.Quote(self, self._extract_selector(tag_name="blockquote", *args, **kwargs))

    def blockquotes(self, *args, **kwargs):
        elements.QuoteCollection(self,
                                 self._extract_selector(tag_name="blockquote", *args, **kwargs))

    watir_snake.tag_to_class['blockquote'] = elements.Quote

    def body(self, *args, **kwargs):
        elements.Body(self, self._extract_selector(tag_name="body", *args, **kwargs))

    def bodys(self, *args, **kwargs):
        elements.BodyCollection(self, self._extract_selector(tag_name="body", *args, **kwargs))

    watir_snake.tag_to_class['body'] = elements.Body

    def br(self, *args, **kwargs):
        elements.BR(self, self._extract_selector(tag_name="br", *args, **kwargs))

    def brs(self, *args, **kwargs):
        elements.BRCollection(self, self._extract_selector(tag_name="br", *args, **kwargs))

    watir_snake.tag_to_class['br'] = elements.BR

    def button(self, *args, **kwargs):
        elements.Button(self, self._extract_selector(tag_name="button", *args, **kwargs))

    def buttons(self, *args, **kwargs):
        elements.ButtonCollection(self, self._extract_selector(tag_name="button", *args, **kwargs))

    watir_snake.tag_to_class['button'] = elements.Button

    def canvas(self, *args, **kwargs):
        elements.Canvas(self, self._extract_selector(tag_name="canvas", *args, **kwargs))

    def canvases(self, *args, **kwargs):
        elements.CanvasCollection(self, self._extract_selector(tag_name="canvas", *args, **kwargs))

    watir_snake.tag_to_class['canvas'] = elements.Canvas

    def caption(self, *args, **kwargs):
        elements.TableCaption(self, self._extract_selector(tag_name="caption", *args, **kwargs))

    def captions(self, *args, **kwargs):
        elements.TableCaptionCollection(self,
                                        self._extract_selector(tag_name="caption", *args, **kwargs))

    watir_snake.tag_to_class['caption'] = elements.TableCaption

    def cite(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="cite", *args, **kwargs))

    def cites(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="cite", *args, **kwargs))

    watir_snake.tag_to_class['cite'] = elements.HTMLElement

    def code(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="code", *args, **kwargs))

    def codes(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="code", *args, **kwargs))

    watir_snake.tag_to_class['code'] = elements.HTMLElement

    def col(self, *args, **kwargs):
        elements.TableCol(self, self._extract_selector(tag_name="col", *args, **kwargs))

    def cols(self, *args, **kwargs):
        elements.TableColCollection(self, self._extract_selector(tag_name="col", *args, **kwargs))

    watir_snake.tag_to_class['col'] = elements.TableCol

    def colgroup(self, *args, **kwargs):
        elements.TableCol(self, self._extract_selector(tag_name="colgroup", *args, **kwargs))

    def colgroups(self, *args, **kwargs):
        elements.TableColCollection(self,
                                    self._extract_selector(tag_name="colgroup", *args, **kwargs))

    watir_snake.tag_to_class['colgroup'] = elements.TableCol

    def data(self, *args, **kwargs):
        elements.Data(self, self._extract_selector(tag_name="data", *args, **kwargs))

    def datas(self, *args, **kwargs):
        elements.DataCollection(self, self._extract_selector(tag_name="data", *args, **kwargs))

    watir_snake.tag_to_class['data'] = elements.Data

    def datalist(self, *args, **kwargs):
        elements.DataList(self, self._extract_selector(tag_name="datalist", *args, **kwargs))

    def datalists(self, *args, **kwargs):
        elements.DataListCollection(self,
                                    self._extract_selector(tag_name="datalist", *args, **kwargs))

    watir_snake.tag_to_class['datalist'] = elements.DataList

    def dd(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="dd", *args, **kwargs))

    def dds(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="dd", *args, **kwargs))

    watir_snake.tag_to_class['dd'] = elements.HTMLElement

    # 'del' is an invalid method name, use delete/deletes instead
    def delete(self, *args, **kwargs):
        elements.Mod(self, self._extract_selector(tag_name="del", *args, **kwargs))

    def deletes(self, *args, **kwargs):
        elements.ModCollection(self, self._extract_selector(tag_name="del", *args, **kwargs))

    watir_snake.tag_to_class['delete'] = elements.Mod

    def details(self, *args, **kwargs):
        elements.Details(self, self._extract_selector(tag_name="details", *args, **kwargs))

    def detailses(self, *args, **kwargs):
        elements.DetailsCollection(self,
                                   self._extract_selector(tag_name="details", *args, **kwargs))

    watir_snake.tag_to_class['details'] = elements.Details

    def dfn(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="dfn", *args, **kwargs))

    def dfns(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="dfn", *args, **kwargs))

    watir_snake.tag_to_class['dfn'] = elements.HTMLElement

    def dialog(self, *args, **kwargs):
        elements.Dialog(self, self._extract_selector(tag_name="dialog", *args, **kwargs))

    def dialogs(self, *args, **kwargs):
        elements.DialogCollection(self, self._extract_selector(tag_name="dialog", *args, **kwargs))

    watir_snake.tag_to_class['dialog'] = elements.Dialog

    def div(self, *args, **kwargs):
        elements.Div(self, self._extract_selector(tag_name="div", *args, **kwargs))

    def divs(self, *args, **kwargs):
        elements.DivCollection(self, self._extract_selector(tag_name="div", *args, **kwargs))

    watir_snake.tag_to_class['div'] = elements.Div

    def dl(self, *args, **kwargs):
        elements.DList(self, self._extract_selector(tag_name="dl", *args, **kwargs))

    def dls(self, *args, **kwargs):
        elements.DListCollection(self, self._extract_selector(tag_name="dl", *args, **kwargs))

    watir_snake.tag_to_class['dl'] = elements.DList

    def dt(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="dt", *args, **kwargs))

    def dts(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="dt", *args, **kwargs))

    watir_snake.tag_to_class['dt'] = elements.HTMLElement

    def em(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="em", *args, **kwargs))

    def ems(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="em", *args, **kwargs))

    watir_snake.tag_to_class['em'] = elements.HTMLElement

    def embed(self, *args, **kwargs):
        elements.Embed(self, self._extract_selector(tag_name="embed", *args, **kwargs))

    def embeds(self, *args, **kwargs):
        elements.EmbedCollection(self, self._extract_selector(tag_name="embed", *args, **kwargs))

    watir_snake.tag_to_class['embed'] = elements.Embed

    def fieldset(self, *args, **kwargs):
        elements.FieldSet(self, self._extract_selector(tag_name="fieldset", *args, **kwargs))

    def fieldsets(self, *args, **kwargs):
        elements.FieldSetCollection(self,
                                    self._extract_selector(tag_name="fieldset", *args, **kwargs))

    watir_snake.tag_to_class['fieldset'] = elements.FieldSet

    def figcaption(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="figcaption", *args, **kwargs))

    def figcaptions(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="figcaption", *args,
                                                                    **kwargs))

    watir_snake.tag_to_class['figcaption'] = elements.HTMLElement

    def figure(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="figure", *args, **kwargs))

    def figures(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="figure", *args, **kwargs))

    watir_snake.tag_to_class['figure'] = elements.HTMLElement

    def footer(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="footer", *args, **kwargs))

    def footers(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="footer", *args, **kwargs))

    watir_snake.tag_to_class['footer'] = elements.HTMLElement

    def form(self, *args, **kwargs):
        elements.Form(self, self._extract_selector(tag_name="form", *args, **kwargs))

    def forms(self, *args, **kwargs):
        elements.FormCollection(self, self._extract_selector(tag_name="form", *args, **kwargs))

    watir_snake.tag_to_class['form'] = elements.Form

    def frameset(self, *args, **kwargs):
        elements.FrameSet(self, self._extract_selector(tag_name="frameset", *args, **kwargs))

    def framesets(self, *args, **kwargs):
        elements.FrameSetCollection(self,
                                    self._extract_selector(tag_name="frameset", *args, **kwargs))

    watir_snake.tag_to_class['frameset'] = elements.FrameSet

    def h1(self, *args, **kwargs):
        elements.Heading(self, self._extract_selector(tag_name="h1", *args, **kwargs))

    def h1s(self, *args, **kwargs):
        elements.HeadingCollection(self, self._extract_selector(tag_name="h1", *args, **kwargs))

    watir_snake.tag_to_class['h1'] = elements.Heading

    def h2(self, *args, **kwargs):
        elements.Heading(self, self._extract_selector(tag_name="h2", *args, **kwargs))

    def h2s(self, *args, **kwargs):
        elements.HeadingCollection(self, self._extract_selector(tag_name="h2", *args, **kwargs))

    watir_snake.tag_to_class['h2'] = elements.Heading

    def h3(self, *args, **kwargs):
        elements.Heading(self, self._extract_selector(tag_name="h3", *args, **kwargs))

    def h3s(self, *args, **kwargs):
        elements.HeadingCollection(self, self._extract_selector(tag_name="h3", *args, **kwargs))

    watir_snake.tag_to_class['h3'] = elements.Heading

    def h4(self, *args, **kwargs):
        elements.Heading(self, self._extract_selector(tag_name="h4", *args, **kwargs))

    def h4s(self, *args, **kwargs):
        elements.HeadingCollection(self, self._extract_selector(tag_name="h4", *args, **kwargs))

    watir_snake.tag_to_class['h4'] = elements.Heading

    def h5(self, *args, **kwargs):
        elements.Heading(self, self._extract_selector(tag_name="h5", *args, **kwargs))

    def h5s(self, *args, **kwargs):
        elements.HeadingCollection(self, self._extract_selector(tag_name="h5", *args, **kwargs))

    watir_snake.tag_to_class['h5'] = elements.Heading

    def h6(self, *args, **kwargs):
        elements.Heading(self, self._extract_selector(tag_name="h6", *args, **kwargs))

    def h6s(self, *args, **kwargs):
        elements.HeadingCollection(self, self._extract_selector(tag_name="h6", *args, **kwargs))

    watir_snake.tag_to_class['h6'] = elements.Heading

    def head(self, *args, **kwargs):
        elements.Head(self, self._extract_selector(tag_name="head", *args, **kwargs))

    def heads(self, *args, **kwargs):
        elements.HeadCollection(self, self._extract_selector(tag_name="head", *args, **kwargs))

    watir_snake.tag_to_class['head'] = elements.Head

    def header(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="header", *args, **kwargs))

    def headers(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="header", *args, **kwargs))

    watir_snake.tag_to_class['header'] = elements.HTMLElement

    def hgroup(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="hgroup", *args, **kwargs))

    def hgroups(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="hgroup", *args, **kwargs))

    watir_snake.tag_to_class['hgroup'] = elements.HTMLElement

    def hr(self, *args, **kwargs):
        elements.HR(self, self._extract_selector(tag_name="hr", *args, **kwargs))

    def hrs(self, *args, **kwargs):
        elements.HRCollection(self, self._extract_selector(tag_name="hr", *args, **kwargs))

    watir_snake.tag_to_class['hr'] = elements.HR

    def html(self, *args, **kwargs):
        elements.Html(self, self._extract_selector(tag_name="html", *args, **kwargs))

    def htmls(self, *args, **kwargs):
        elements.HtmlCollection(self, self._extract_selector(tag_name="html", *args, **kwargs))

    watir_snake.tag_to_class['html'] = elements.Html

    # Plural of 'i' cannot be a method name, use ital/itals instead
    def ital(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="i", *args, **kwargs))

    def itals(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="i", *args, **kwargs))

    watir_snake.tag_to_class['ital'] = elements.HTMLElement

    def iframe(self, *args, **kwargs):
        elements.IFrame(self, self._extract_selector(tag_name="iframe", *args, **kwargs))

    def iframes(self, *args, **kwargs):
        elements.IFrameCollection(self, self._extract_selector(tag_name="iframe", *args, **kwargs))

    watir_snake.tag_to_class['iframe'] = elements.IFrame

    def img(self, *args, **kwargs):
        elements.Image(self, self._extract_selector(tag_name="img", *args, **kwargs))

    def imgs(self, *args, **kwargs):
        elements.ImageCollection(self, self._extract_selector(tag_name="img", *args, **kwargs))

    watir_snake.tag_to_class['img'] = elements.Image

    def input(self, *args, **kwargs):
        elements.Input(self, self._extract_selector(tag_name="input", *args, **kwargs))

    def inputs(self, *args, **kwargs):
        elements.InputCollection(self, self._extract_selector(tag_name="input", *args, **kwargs))

    watir_snake.tag_to_class['input'] = elements.Input

    def ins(self, *args, **kwargs):
        elements.Mod(self, self._extract_selector(tag_name="ins", *args, **kwargs))

    def inses(self, *args, **kwargs):
        elements.ModCollection(self, self._extract_selector(tag_name="ins", *args, **kwargs))

    watir_snake.tag_to_class['ins'] = elements.Mod

    def kbd(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="kbd", *args, **kwargs))

    def kbds(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="kbd", *args, **kwargs))

    watir_snake.tag_to_class['kbd'] = elements.HTMLElement

    def keygen(self, *args, **kwargs):
        elements.Keygen(self, self._extract_selector(tag_name="keygen", *args, **kwargs))

    def keygens(self, *args, **kwargs):
        elements.KeygenCollection(self, self._extract_selector(tag_name="keygen", *args, **kwargs))

    watir_snake.tag_to_class['keygen'] = elements.Keygen

    def label(self, *args, **kwargs):
        elements.Label(self, self._extract_selector(tag_name="label", *args, **kwargs))

    def labels(self, *args, **kwargs):
        elements.LabelCollection(self, self._extract_selector(tag_name="label", *args, **kwargs))

    watir_snake.tag_to_class['label'] = elements.Label

    def legend(self, *args, **kwargs):
        elements.Legend(self, self._extract_selector(tag_name="legend", *args, **kwargs))

    def legends(self, *args, **kwargs):
        elements.LegendCollection(self, self._extract_selector(tag_name="legend", *args, **kwargs))

    watir_snake.tag_to_class['legend'] = elements.Legend

    def li(self, *args, **kwargs):
        elements.LI(self, self._extract_selector(tag_name="li", *args, **kwargs))

    def lis(self, *args, **kwargs):
        elements.LICollection(self, self._extract_selector(tag_name="li", *args, **kwargs))

    watir_snake.tag_to_class['li'] = elements.LI

    def main(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="main", *args, **kwargs))

    def mains(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="main", *args, **kwargs))

    watir_snake.tag_to_class['main'] = elements.HTMLElement

    def map(self, *args, **kwargs):
        elements.Map(self, self._extract_selector(tag_name="map", *args, **kwargs))

    def maps(self, *args, **kwargs):
        elements.MapCollection(self, self._extract_selector(tag_name="map", *args, **kwargs))

    watir_snake.tag_to_class['map'] = elements.Map

    def mark(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="mark", *args, **kwargs))

    def marks(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="mark", *args, **kwargs))

    watir_snake.tag_to_class['mark'] = elements.HTMLElement

    def menu(self, *args, **kwargs):
        elements.Menu(self, self._extract_selector(tag_name="menu", *args, **kwargs))

    def menus(self, *args, **kwargs):
        elements.MenuCollection(self, self._extract_selector(tag_name="menu", *args, **kwargs))

    watir_snake.tag_to_class['menu'] = elements.Menu

    def menuitem(self, *args, **kwargs):
        elements.MenuItem(self, self._extract_selector(tag_name="menuitem", *args, **kwargs))

    def menuitems(self, *args, **kwargs):
        elements.MenuItemCollection(self,
                                    self._extract_selector(tag_name="menuitem", *args, **kwargs))

    watir_snake.tag_to_class['menuitem'] = elements.MenuItem

    def meta(self, *args, **kwargs):
        elements.Meta(self, self._extract_selector(tag_name="meta", *args, **kwargs))

    def metas(self, *args, **kwargs):
        elements.MetaCollection(self, self._extract_selector(tag_name="meta", *args, **kwargs))

    watir_snake.tag_to_class['meta'] = elements.Meta

    def meter(self, *args, **kwargs):
        elements.Meter(self, self._extract_selector(tag_name="meter", *args, **kwargs))

    def meters(self, *args, **kwargs):
        elements.MeterCollection(self, self._extract_selector(tag_name="meter", *args, **kwargs))

    watir_snake.tag_to_class['meter'] = elements.Meter

    def nav(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="nav", *args, **kwargs))

    def navs(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="nav", *args, **kwargs))

    watir_snake.tag_to_class['nav'] = elements.HTMLElement

    def noscript(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="noscript", *args, **kwargs))

    def noscripts(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="noscript", *args, **kwargs))

    watir_snake.tag_to_class['noscript'] = elements.HTMLElement

    def object(self, *args, **kwargs):
        elements.Object(self, self._extract_selector(tag_name="object", *args, **kwargs))

    def objects(self, *args, **kwargs):
        elements.ObjectCollection(self, self._extract_selector(tag_name="object", *args, **kwargs))

    watir_snake.tag_to_class['object'] = elements.Object

    def ol(self, *args, **kwargs):
        elements.OList(self, self._extract_selector(tag_name="ol", *args, **kwargs))

    def ols(self, *args, **kwargs):
        elements.OListCollection(self, self._extract_selector(tag_name="ol", *args, **kwargs))

    watir_snake.tag_to_class['ol'] = elements.OList

    def optgroup(self, *args, **kwargs):
        elements.OptGroup(self, self._extract_selector(tag_name="optgroup", *args, **kwargs))

    def optgroups(self, *args, **kwargs):
        elements.OptGroupCollection(self,
                                    self._extract_selector(tag_name="optgroup", *args, **kwargs))

    watir_snake.tag_to_class['optgroup'] = elements.OptGroup

    def option(self, *args, **kwargs):
        elements.Option(self, self._extract_selector(tag_name="option", *args, **kwargs))

    def options(self, *args, **kwargs):
        elements.OptionCollection(self, self._extract_selector(tag_name="option", *args, **kwargs))

    watir_snake.tag_to_class['option'] = elements.Option

    def output(self, *args, **kwargs):
        elements.Output(self, self._extract_selector(tag_name="output", *args, **kwargs))

    def outputs(self, *args, **kwargs):
        elements.OutputCollection(self, self._extract_selector(tag_name="output", *args, **kwargs))

    watir_snake.tag_to_class['output'] = elements.Output

    def p(self, *args, **kwargs):
        elements.Paragraph(self, self._extract_selector(tag_name="p", *args, **kwargs))

    def ps(self, *args, **kwargs):
        elements.ParagraphCollection(self, self._extract_selector(tag_name="p", *args, **kwargs))

    watir_snake.tag_to_class['p'] = elements.Paragraph

    def param(self, *args, **kwargs):
        elements.Param(self, self._extract_selector(tag_name="param", *args, **kwargs))

    def params(self, *args, **kwargs):
        elements.ParamCollection(self, self._extract_selector(tag_name="param", *args, **kwargs))

    watir_snake.tag_to_class['param'] = elements.Param

    def pre(self, *args, **kwargs):
        elements.Pre(self, self._extract_selector(tag_name="pre", *args, **kwargs))

    def pres(self, *args, **kwargs):
        elements.PreCollection(self, self._extract_selector(tag_name="pre", *args, **kwargs))

    watir_snake.tag_to_class['pre'] = elements.Pre

    def progress(self, *args, **kwargs):
        elements.Progress(self, self._extract_selector(tag_name="progress", *args, **kwargs))

    def progresses(self, *args, **kwargs):
        elements.ProgressCollection(self,
                                    self._extract_selector(tag_name="progress", *args, **kwargs))

    watir_snake.tag_to_class['progress'] = elements.Progress

    def q(self, *args, **kwargs):
        elements.Quote(self, self._extract_selector(tag_name="q", *args, **kwargs))

    def qs(self, *args, **kwargs):
        elements.QuoteCollection(self, self._extract_selector(tag_name="q", *args, **kwargs))

    watir_snake.tag_to_class['q'] = elements.Quote

    def rp(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="rp", *args, **kwargs))

    def rps(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="rp", *args, **kwargs))

    watir_snake.tag_to_class['rp'] = elements.HTMLElement

    def rt(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="rt", *args, **kwargs))

    def rts(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="rt", *args, **kwargs))

    watir_snake.tag_to_class['rt'] = elements.HTMLElement

    def ruby(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="ruby", *args, **kwargs))

    def rubies(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="ruby", *args, **kwargs))

    watir_snake.tag_to_class['ruby'] = elements.HTMLElement

    def s(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="s", *args, **kwargs))

    def ss(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="s", *args, **kwargs))

    watir_snake.tag_to_class['s'] = elements.HTMLElement

    def samp(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="samp", *args, **kwargs))

    def samps(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="samp", *args, **kwargs))

    watir_snake.tag_to_class['samp'] = elements.HTMLElement

    def script(self, *args, **kwargs):
        elements.Script(self, self._extract_selector(tag_name="script", *args, **kwargs))

    def scripts(self, *args, **kwargs):
        elements.ScriptCollection(self, self._extract_selector(tag_name="script", *args, **kwargs))

    watir_snake.tag_to_class['script'] = elements.Script

    def section(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="section", *args, **kwargs))

    def sections(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="section", *args, **kwargs))

    watir_snake.tag_to_class['section'] = elements.HTMLElement

    def select(self, *args, **kwargs):
        elements.Select(self, self._extract_selector(tag_name="select", *args, **kwargs))

    def selects(self, *args, **kwargs):
        elements.SelectCollection(self, self._extract_selector(tag_name="select", *args, **kwargs))

    watir_snake.tag_to_class['select'] = elements.Select

    def small(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="small", *args, **kwargs))

    def smalls(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="small", *args, **kwargs))

    watir_snake.tag_to_class['small'] = elements.HTMLElement

    def source(self, *args, **kwargs):
        elements.Source(self, self._extract_selector(tag_name="source", *args, **kwargs))

    def sources(self, *args, **kwargs):
        elements.SourceCollection(self, self._extract_selector(tag_name="source", *args, **kwargs))

    watir_snake.tag_to_class['source'] = elements.Source

    def span(self, *args, **kwargs):
        elements.Span(self, self._extract_selector(tag_name="span", *args, **kwargs))

    def spans(self, *args, **kwargs):
        elements.SpanCollection(self, self._extract_selector(tag_name="span", *args, **kwargs))

    watir_snake.tag_to_class['span'] = elements.Span

    def strong(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="strong", *args, **kwargs))

    def strongs(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="strong", *args, **kwargs))

    watir_snake.tag_to_class['strong'] = elements.HTMLElement

    def style(self, *args, **kwargs):
        elements.Style(self, self._extract_selector(tag_name="style", *args, **kwargs))

    def styles(self, *args, **kwargs):
        elements.StyleCollection(self, self._extract_selector(tag_name="style", *args, **kwargs))

    watir_snake.tag_to_class['style'] = elements.Style

    def sub(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="sub", *args, **kwargs))

    def subs(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="sub", *args, **kwargs))

    watir_snake.tag_to_class['sub'] = elements.HTMLElement

    def summary(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="summary", *args, **kwargs))

    def summaries(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="summary", *args, **kwargs))

    watir_snake.tag_to_class['summary'] = elements.HTMLElement

    def sup(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="sup", *args, **kwargs))

    def sups(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="sup", *args, **kwargs))

    watir_snake.tag_to_class['sup'] = elements.HTMLElement

    def table(self, *args, **kwargs):
        elements.Table(self, self._extract_selector(tag_name="table", *args, **kwargs))

    def tables(self, *args, **kwargs):
        elements.TableCollection(self, self._extract_selector(tag_name="table", *args, **kwargs))

    watir_snake.tag_to_class['table'] = elements.Table

    def tbody(self, *args, **kwargs):
        elements.TableSection(self, self._extract_selector(tag_name="tbody", *args, **kwargs))

    def tbodys(self, *args, **kwargs):
        elements.TableSectionCollection(self,
                                        self._extract_selector(tag_name="tbody", *args, **kwargs))

    watir_snake.tag_to_class['tbody'] = elements.TableSection

    def td(self, *args, **kwargs):
        elements.TableDataCell(self, self._extract_selector(tag_name="td", *args, **kwargs))

    def tds(self, *args, **kwargs):
        elements.TableDataCellCollection(self,
                                         self._extract_selector(tag_name="td", *args, **kwargs))

    watir_snake.tag_to_class['td'] = elements.TableDataCell

    def template(self, *args, **kwargs):
        elements.Template(self, self._extract_selector(tag_name="template", *args, **kwargs))

    def templates(self, *args, **kwargs):
        elements.TemplateCollection(self,
                                    self._extract_selector(tag_name="template", *args, **kwargs))

    watir_snake.tag_to_class['template'] = elements.Template

    def textarea(self, *args, **kwargs):
        elements.TextArea(self, self._extract_selector(tag_name="textarea", *args, **kwargs))

    def textareas(self, *args, **kwargs):
        elements.TextAreaCollection(self,
                                    self._extract_selector(tag_name="textarea", *args, **kwargs))

    watir_snake.tag_to_class['textarea'] = elements.TextArea

    def tfoot(self, *args, **kwargs):
        elements.TableSection(self, self._extract_selector(tag_name="tfoot", *args, **kwargs))

    def tfoots(self, *args, **kwargs):
        elements.TableSectionCollection(self,
                                        self._extract_selector(tag_name="tfoot", *args, **kwargs))

    watir_snake.tag_to_class['tfoot'] = elements.TableSection

    def th(self, *args, **kwargs):
        elements.TableHeaderCell(self, self._extract_selector(tag_name="th", *args, **kwargs))

    def ths(self, *args, **kwargs):
        elements.TableHeaderCellCollection(self,
                                           self._extract_selector(tag_name="th", *args, **kwargs))

    watir_snake.tag_to_class['th'] = elements.TableHeaderCell

    def thead(self, *args, **kwargs):
        elements.TableSection(self, self._extract_selector(tag_name="thead", *args, **kwargs))

    def theads(self, *args, **kwargs):
        elements.TableSectionCollection(self,
                                        self._extract_selector(tag_name="thead", *args, **kwargs))

    watir_snake.tag_to_class['thead'] = elements.TableSection

    def time(self, *args, **kwargs):
        elements.Time(self, self._extract_selector(tag_name="time", *args, **kwargs))

    def times(self, *args, **kwargs):
        elements.TimeCollection(self, self._extract_selector(tag_name="time", *args, **kwargs))

    watir_snake.tag_to_class['time'] = elements.Time

    def title(self, *args, **kwargs):
        elements.Title(self, self._extract_selector(tag_name="title", *args, **kwargs))

    def titles(self, *args, **kwargs):
        elements.TitleCollection(self, self._extract_selector(tag_name="title", *args, **kwargs))

    watir_snake.tag_to_class['title'] = elements.Title

    def tr(self, *args, **kwargs):
        elements.TableRow(self, self._extract_selector(tag_name="tr", *args, **kwargs))

    def trs(self, *args, **kwargs):
        elements.TableRowCollection(self, self._extract_selector(tag_name="tr", *args, **kwargs))

    watir_snake.tag_to_class['tr'] = elements.TableRow

    def track(self, *args, **kwargs):
        elements.Track(self, self._extract_selector(tag_name="track", *args, **kwargs))

    def tracks(self, *args, **kwargs):
        elements.TrackCollection(self, self._extract_selector(tag_name="track", *args, **kwargs))

    watir_snake.tag_to_class['track'] = elements.Track

    def u(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="u", *args, **kwargs))

    def us(self, *args, **kwargs):
        elements.HTMLElementCollection(self, self._extract_selector(tag_name="u", *args, **kwargs))

    watir_snake.tag_to_class['u'] = elements.HTMLElement

    def ul(self, *args, **kwargs):
        elements.UList(self, self._extract_selector(tag_name="ul", *args, **kwargs))

    def uls(self, *args, **kwargs):
        elements.UListCollection(self, self._extract_selector(tag_name="ul", *args, **kwargs))

    watir_snake.tag_to_class['ul'] = elements.UList

    def var(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="var", *args, **kwargs))

    def vars(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="var", *args, **kwargs))

    watir_snake.tag_to_class['var'] = elements.HTMLElement

    def video(self, *args, **kwargs):
        elements.Video(self, self._extract_selector(tag_name="video", *args, **kwargs))

    def videos(self, *args, **kwargs):
        elements.VideoCollection(self, self._extract_selector(tag_name="video", *args, **kwargs))

    watir_snake.tag_to_class['video'] = elements.Video

    def wbr(self, *args, **kwargs):
        elements.HTMLElement(self, self._extract_selector(tag_name="wbr", *args, **kwargs))

    def wbrs(self, *args, **kwargs):
        elements.HTMLElementCollection(self,
                                       self._extract_selector(tag_name="wbr", *args, **kwargs))

    watir_snake.tag_to_class['wbr'] = elements.HTMLElement
