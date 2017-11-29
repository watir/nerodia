from nerodia import tag_to_class
from .elements.area import Area
from .elements.button import Button
from .elements.d_list import DList
from .elements.form import Form
from .elements.html_elements import HTMLElement, Audio, Base, Quote, Body, BR, Canvas, \
    TableCaption, TableCol, Data, DataList, Mod, Details, Dialog, Div, Embed, FieldSet, FrameSet, \
    Heading, Head, HR, Html, Input, Keygen, Label, Legend, LI, Map, Menu, MenuItem, Meta, Meter, Object, \
    OptGroup, Output, Paragraph, Param, Pre, Progress, Script, Source, Span, Style, \
    Template, TableHeaderCell, Time, Title, Track, Video, AnchorCollection, \
    HTMLElementCollection, AreaCollection, AudioCollection, BaseCollection, QuoteCollection, \
    BodyCollection, BRCollection, ButtonCollection, CanvasCollection, TableCaptionCollection, \
    TableColCollection, DataCollection, DataListCollection, ModCollection, DetailsCollection, \
    DialogCollection, DivCollection, DListCollection, EmbedCollection, FieldSetCollection, \
    FormCollection, FrameSetCollection, HeadingCollection, HeadCollection, HRCollection, \
    HtmlCollection, IFrameCollection, ImageCollection, InputCollection, KeygenCollection, \
    LabelCollection, LegendCollection, LICollection, MapCollection, MenuCollection, \
    MenuItemCollection, MetaCollection, MeterCollection, ObjectCollection, OListCollection, \
    OptGroupCollection, OptionCollection, OutputCollection, ParagraphCollection, ParamCollection, \
    PreCollection, ProgressCollection, ScriptCollection, SelectCollection, SourceCollection, \
    SpanCollection, StyleCollection, TableDataCellCollection, TemplateCollection, TextAreaCollection, \
    TableCollection, TableHeaderCellCollection, TableSectionCollection, TimeCollection, TitleCollection, \
    TableRowCollection, TrackCollection, UListCollection, VideoCollection
from .elements.i_frame import IFrame
from .elements.image import Image
from .elements.link import Anchor
from .elements.list import OList, UList
from .elements.option import Option
from .elements.select import Select
from .elements.table import Table
from .elements.table_data_cell import TableDataCell
from .elements.table_row import TableRow
from .elements.table_section import TableSection
from .elements.text_area import TextArea

tag_to_class['a'] = Anchor
tag_to_class['a_collection'] = AnchorCollection
tag_to_class['link'] = Anchor
tag_to_class['link_collection'] = AnchorCollection
tag_to_class['abbr'] = HTMLElement
tag_to_class['abbr_collection'] = HTMLElementCollection
tag_to_class['address'] = HTMLElement
tag_to_class['address_collection'] = HTMLElementCollection
tag_to_class['area'] = Area
tag_to_class['area_collection'] = AreaCollection
tag_to_class['article'] = HTMLElement
tag_to_class['article_collection'] = HTMLElementCollection
tag_to_class['aside'] = HTMLElement
tag_to_class['aside_collection'] = HTMLElementCollection
tag_to_class['audio'] = Audio
tag_to_class['audio_collection'] = AudioCollection
tag_to_class['b'] = HTMLElement
tag_to_class['b_collection'] = HTMLElementCollection
tag_to_class['base'] = Base
tag_to_class['base_collection'] = BaseCollection
tag_to_class['bdi'] = HTMLElement
tag_to_class['bdi_collection'] = HTMLElementCollection
tag_to_class['bdo'] = HTMLElement
tag_to_class['bdo_collection'] = HTMLElementCollection
tag_to_class['blockquote'] = Quote
tag_to_class['blockquote_collection'] = QuoteCollection
tag_to_class['body'] = Body
tag_to_class['body_collection'] = BodyCollection
tag_to_class['br'] = BR
tag_to_class['br_collection'] = BRCollection
tag_to_class['button'] = Button
tag_to_class['button_collection'] = ButtonCollection
tag_to_class['canvas'] = Canvas
tag_to_class['canvas_collection'] = CanvasCollection
tag_to_class['caption'] = TableCaption
tag_to_class['caption_collection'] = TableCaptionCollection
tag_to_class['cite'] = HTMLElement
tag_to_class['cite_collection'] = HTMLElementCollection
tag_to_class['code'] = HTMLElement
tag_to_class['code_collection'] = HTMLElementCollection
tag_to_class['col'] = TableCol
tag_to_class['col_collection'] = TableColCollection
tag_to_class['colgroup'] = TableCol
tag_to_class['colgroup_collection'] = TableColCollection
tag_to_class['data'] = Data
tag_to_class['data_collection'] = DataCollection
tag_to_class['datalist'] = DataList
tag_to_class['datalist_collection'] = DataListCollection
tag_to_class['dd'] = HTMLElement
tag_to_class['dd_collection'] = HTMLElementCollection
tag_to_class['del'] = Mod
tag_to_class['del_collection'] = ModCollection
tag_to_class['delete'] = Mod
tag_to_class['delete_collection'] = ModCollection
tag_to_class['details'] = Details
tag_to_class['details_collection'] = DetailsCollection
tag_to_class['dfn'] = HTMLElement
tag_to_class['dfn_collection'] = HTMLElementCollection
tag_to_class['dialog'] = Dialog
tag_to_class['dialog_collection'] = DialogCollection
tag_to_class['div'] = Div
tag_to_class['div_collection'] = DivCollection
tag_to_class['dl'] = DList
tag_to_class['dl_collection'] = DListCollection
tag_to_class['dt'] = HTMLElement
tag_to_class['dt_collection'] = HTMLElementCollection
tag_to_class['em'] = HTMLElement
tag_to_class['em_collection'] = HTMLElementCollection
tag_to_class['embed'] = Embed
tag_to_class['embed_collection'] = EmbedCollection
tag_to_class['fieldset'] = FieldSet
tag_to_class['fieldset_collection'] = FieldSetCollection
tag_to_class['figcaption'] = HTMLElement
tag_to_class['figcaption_collection'] = HTMLElementCollection
tag_to_class['figure'] = HTMLElement
tag_to_class['figure_collection'] = HTMLElementCollection
tag_to_class['footer'] = HTMLElement
tag_to_class['footer_collection'] = HTMLElementCollection
tag_to_class['form'] = Form
tag_to_class['form_collection'] = FormCollection
tag_to_class['frameset'] = FrameSet
tag_to_class['frameset_collection'] = FrameSetCollection
tag_to_class['h1'] = Heading
tag_to_class['h1_collection'] = HeadingCollection
tag_to_class['h2'] = Heading
tag_to_class['h2_collection'] = HeadingCollection
tag_to_class['h3'] = Heading
tag_to_class['h3_collection'] = HeadingCollection
tag_to_class['h4'] = Heading
tag_to_class['h4_collection'] = HeadingCollection
tag_to_class['h5'] = Heading
tag_to_class['h5_collection'] = HeadingCollection
tag_to_class['h6'] = Heading
tag_to_class['h6_collection'] = HeadingCollection
tag_to_class['head'] = Head
tag_to_class['head_collection'] = HeadCollection
tag_to_class['header'] = HTMLElement
tag_to_class['header_collection'] = HTMLElementCollection
tag_to_class['hgroup'] = HTMLElement
tag_to_class['hgroup_collection'] = HTMLElementCollection
tag_to_class['hr'] = HR
tag_to_class['hr_collection'] = HRCollection
tag_to_class['html'] = Html
tag_to_class['html_collection'] = HtmlCollection
tag_to_class['i'] = HTMLElement
tag_to_class['i_collection'] = HTMLElementCollection
tag_to_class['ital'] = HTMLElement
tag_to_class['ital_collection'] = HTMLElementCollection
tag_to_class['iframe'] = IFrame
tag_to_class['iframe_collection'] = IFrameCollection
tag_to_class['img'] = Image
tag_to_class['img_collection'] = ImageCollection
tag_to_class['input'] = Input
tag_to_class['input_collection'] = InputCollection
tag_to_class['ins'] = Mod
tag_to_class['ins_collection'] = ModCollection
tag_to_class['kbd'] = HTMLElement
tag_to_class['kbd_collection'] = HTMLElementCollection
tag_to_class['keygen'] = Keygen
tag_to_class['keygen_collection'] = KeygenCollection
tag_to_class['label'] = Label
tag_to_class['label_collection'] = LabelCollection
tag_to_class['legend'] = Legend
tag_to_class['legend_collection'] = LegendCollection
tag_to_class['li'] = LI
tag_to_class['li_collection'] = LICollection
tag_to_class['main'] = HTMLElement
tag_to_class['main_collection'] = HTMLElementCollection
tag_to_class['map'] = Map
tag_to_class['map_collection'] = MapCollection
tag_to_class['mark'] = HTMLElement
tag_to_class['mark_collection'] = HTMLElementCollection
tag_to_class['menu'] = Menu
tag_to_class['menu_collection'] = MenuCollection
tag_to_class['menuitem'] = MenuItem
tag_to_class['menuitem_collection'] = MenuItemCollection
tag_to_class['meta'] = Meta
tag_to_class['meta_collection'] = MetaCollection
tag_to_class['meter'] = Meter
tag_to_class['meter_collection'] = MeterCollection
tag_to_class['nav'] = HTMLElement
tag_to_class['nav_collection'] = HTMLElementCollection
tag_to_class['noscript'] = HTMLElement
tag_to_class['noscript_collection'] = HTMLElementCollection
tag_to_class['object'] = Object
tag_to_class['object_collection'] = ObjectCollection
tag_to_class['ol'] = OList
tag_to_class['ol_collection'] = OListCollection
tag_to_class['optgroup'] = OptGroup
tag_to_class['optgroup_collection'] = OptGroupCollection
tag_to_class['option'] = Option
tag_to_class['option_collection'] = OptionCollection
tag_to_class['output'] = Output
tag_to_class['output_collection'] = OutputCollection
tag_to_class['p'] = Paragraph
tag_to_class['p_collection'] = ParagraphCollection
tag_to_class['param'] = Param
tag_to_class['param_collection'] = ParamCollection
tag_to_class['pre'] = Pre
tag_to_class['pre_collection'] = PreCollection
tag_to_class['progress'] = Progress
tag_to_class['progress_collection'] = ProgressCollection
tag_to_class['q'] = Quote
tag_to_class['q_collection'] = QuoteCollection
tag_to_class['rp'] = HTMLElement
tag_to_class['rp_collection'] = HTMLElementCollection
tag_to_class['rt'] = HTMLElement
tag_to_class['rt_collection'] = HTMLElementCollection
tag_to_class['ruby'] = HTMLElement
tag_to_class['ruby_collection'] = HTMLElementCollection
tag_to_class['s'] = HTMLElement
tag_to_class['s_collection'] = HTMLElementCollection
tag_to_class['samp'] = HTMLElement
tag_to_class['samp_collection'] = HTMLElementCollection
tag_to_class['script'] = Script
tag_to_class['script_collection'] = ScriptCollection
tag_to_class['section'] = HTMLElement
tag_to_class['section_collection'] = HTMLElementCollection
tag_to_class['select'] = Select
tag_to_class['select_collection'] = SelectCollection
tag_to_class['select_list'] = Select
tag_to_class['select_list_collection'] = SelectCollection
tag_to_class['small'] = HTMLElement
tag_to_class['small_collection'] = HTMLElementCollection
tag_to_class['source'] = Source
tag_to_class['source_collection'] = SourceCollection
tag_to_class['span'] = Span
tag_to_class['span_collection'] = SpanCollection
tag_to_class['strong'] = HTMLElement
tag_to_class['strong_collection'] = HTMLElementCollection
tag_to_class['style'] = Style
tag_to_class['style_collection'] = StyleCollection
tag_to_class['sub'] = HTMLElement
tag_to_class['sub_collection'] = HTMLElementCollection
tag_to_class['summary'] = HTMLElement
tag_to_class['summary_collection'] = HTMLElementCollection
tag_to_class['sup'] = HTMLElement
tag_to_class['sup_collection'] = HTMLElementCollection
tag_to_class['table'] = Table
tag_to_class['table_collection'] = TableCollection
tag_to_class['tbody'] = TableSection
tag_to_class['tbody_collection'] = TableSectionCollection
tag_to_class['td'] = TableDataCell
tag_to_class['td_collection'] = TableDataCellCollection
tag_to_class['template'] = Template
tag_to_class['template_collection'] = TemplateCollection
tag_to_class['textarea'] = TextArea
tag_to_class['textarea_collection'] = TextAreaCollection
tag_to_class['tfoot'] = TableSection
tag_to_class['tfoot_collection'] = TableSectionCollection
tag_to_class['th'] = TableHeaderCell
tag_to_class['th_collection'] = TableHeaderCellCollection
tag_to_class['thead'] = TableSection
tag_to_class['thead_collection'] = TableSectionCollection
tag_to_class['time'] = Time
tag_to_class['time_collection'] = TimeCollection
tag_to_class['title'] = Title
tag_to_class['title_collection'] = TitleCollection
tag_to_class['tr'] = TableRow
tag_to_class['tr_collection'] = TableRowCollection
tag_to_class['track'] = Track
tag_to_class['track_collection'] = TrackCollection
tag_to_class['u'] = HTMLElement
tag_to_class['u_collection'] = HTMLElementCollection
tag_to_class['ul'] = UList
tag_to_class['ul_collection'] = UListCollection
tag_to_class['var'] = HTMLElement
tag_to_class['var_collection'] = HTMLElementCollection
tag_to_class['video'] = Video
tag_to_class['video_collection'] = VideoCollection
tag_to_class['wbr'] = HTMLElement
tag_to_class['wbr_collection'] = HTMLElementCollection
