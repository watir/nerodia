from watir_snake import tag_to_class
from watir_snake.elements.area import Area
from watir_snake.elements.button import Button
from watir_snake.elements.dlist import DList
from watir_snake.elements.form import Form
from watir_snake.elements.html_elements import HTMLElement, Audio, Base, Quote, Body, BR, Canvas, \
    TableCaption, TableCol, Data, DataList, Mod, Details, Dialog, Div, Embed, FieldSet, FrameSet, \
    Heading, Head, HR, Html, Keygen, Label, Legend, LI, Map, Menu, MenuItem, Meta, Meter, Object, \
    OList, OptGroup, Output, Paragraph, Param, Pre, Progress, Script, Source, Span, Style, \
    TableDataCell, Template, TableHeaderCell, Time, Title, Track, UList, Video
from watir_snake.elements.iframe import IFrame
from watir_snake.elements.image import Image
from watir_snake.elements.input import Input
from watir_snake.elements.link import Anchor
from watir_snake.elements.option import Option
from watir_snake.elements.select import Select
from watir_snake.elements.table import Table
from watir_snake.elements.table_row import TableRow
from watir_snake.elements.table_section import TableSection
from watir_snake.elements.text_area import TextArea

tag_to_class['link'] = Anchor
tag_to_class['abbr'] = HTMLElement
tag_to_class['address'] = HTMLElement
tag_to_class['area'] = Area
tag_to_class['article'] = HTMLElement
tag_to_class['aside'] = HTMLElement
tag_to_class['audio'] = Audio
tag_to_class['b'] = HTMLElement
tag_to_class['base'] = Base
tag_to_class['bdi'] = HTMLElement
tag_to_class['bdo'] = HTMLElement
tag_to_class['blockquote'] = Quote
tag_to_class['body'] = Body
tag_to_class['br'] = BR
tag_to_class['button'] = Button
tag_to_class['canvas'] = Canvas
tag_to_class['caption'] = TableCaption
tag_to_class['cite'] = HTMLElement
tag_to_class['code'] = HTMLElement
tag_to_class['col'] = TableCol
tag_to_class['colgroup'] = TableCol
tag_to_class['data'] = Data
tag_to_class['datalist'] = DataList
tag_to_class['dd'] = HTMLElement
tag_to_class['delete'] = Mod
tag_to_class['details'] = Details
tag_to_class['dfn'] = HTMLElement
tag_to_class['dialog'] = Dialog
tag_to_class['div'] = Div
tag_to_class['dl'] = DList
tag_to_class['dt'] = HTMLElement
tag_to_class['em'] = HTMLElement
tag_to_class['embed'] = Embed
tag_to_class['fieldset'] = FieldSet
tag_to_class['figcaption'] = HTMLElement
tag_to_class['figure'] = HTMLElement
tag_to_class['footer'] = HTMLElement
tag_to_class['form'] = Form
tag_to_class['frameset'] = FrameSet
tag_to_class['h1'] = Heading
tag_to_class['h2'] = Heading
tag_to_class['h3'] = Heading
tag_to_class['h4'] = Heading
tag_to_class['h5'] = Heading
tag_to_class['h6'] = Heading
tag_to_class['head'] = Head
tag_to_class['header'] = HTMLElement
tag_to_class['hgroup'] = HTMLElement
tag_to_class['hr'] = HR
tag_to_class['html'] = Html
tag_to_class['ital'] = HTMLElement
tag_to_class['iframe'] = IFrame
tag_to_class['img'] = Image
tag_to_class['input'] = Input
tag_to_class['ins'] = Mod
tag_to_class['kbd'] = HTMLElement
tag_to_class['keygen'] = Keygen
tag_to_class['label'] = Label
tag_to_class['legend'] = Legend
tag_to_class['li'] = LI
tag_to_class['main'] = HTMLElement
tag_to_class['map'] = Map
tag_to_class['mark'] = HTMLElement
tag_to_class['menu'] = Menu
tag_to_class['menuitem'] = MenuItem
tag_to_class['meta'] = Meta
tag_to_class['meter'] = Meter
tag_to_class['nav'] = HTMLElement
tag_to_class['noscript'] = HTMLElement
tag_to_class['object'] = Object
tag_to_class['ol'] = OList
tag_to_class['optgroup'] = OptGroup
tag_to_class['option'] = Option
tag_to_class['output'] = Output
tag_to_class['p'] = Paragraph
tag_to_class['param'] = Param
tag_to_class['pre'] = Pre
tag_to_class['progress'] = Progress
tag_to_class['q'] = Quote
tag_to_class['rp'] = HTMLElement
tag_to_class['rt'] = HTMLElement
tag_to_class['ruby'] = HTMLElement
tag_to_class['s'] = HTMLElement
tag_to_class['samp'] = HTMLElement
tag_to_class['script'] = Script
tag_to_class['section'] = HTMLElement
tag_to_class['select'] = Select
tag_to_class['select_list'] = Select
tag_to_class['small'] = HTMLElement
tag_to_class['source'] = Source
tag_to_class['span'] = Span
tag_to_class['strong'] = HTMLElement
tag_to_class['style'] = Style
tag_to_class['sub'] = HTMLElement
tag_to_class['summary'] = HTMLElement
tag_to_class['sup'] = HTMLElement
tag_to_class['table'] = Table
tag_to_class['tbody'] = TableSection
tag_to_class['td'] = TableDataCell
tag_to_class['template'] = Template
tag_to_class['textarea'] = TextArea
tag_to_class['tfoot'] = TableSection
tag_to_class['th'] = TableHeaderCell
tag_to_class['thead'] = TableSection
tag_to_class['time'] = Time
tag_to_class['title'] = Title
tag_to_class['tr'] = TableRow
tag_to_class['track'] = Track
tag_to_class['u'] = HTMLElement
tag_to_class['ul'] = UList
tag_to_class['var'] = HTMLElement
tag_to_class['video'] = Video
tag_to_class['wbr'] = HTMLElement
