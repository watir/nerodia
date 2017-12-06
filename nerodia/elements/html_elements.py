import six

from .element import Element
from ..element_collection import ElementCollection
from ..meta_elements import MetaHTMLElement


@six.add_metaclass(MetaHTMLElement)
class HTMLElement(Element):
    _attr_id = (str, 'id')
    _attr_class_name = (str, 'className')


@six.add_metaclass(MetaHTMLElement)
class HTMLElementCollection(ElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class FontCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Directory(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class DirectoryCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class FrameSet(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class FrameSetCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Marquee(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MarqueeCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Applet(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class AppletCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Canvas(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class CanvasCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Template(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TemplateCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Script(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class ScriptCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Dialog(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class DialogCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class MenuItem(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MenuItemCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Menu(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MenuCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Details(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class DetailsCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Legend(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class LegendCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class FieldSet(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class FieldSetCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Meter(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MeterCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Progress(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class ProgressCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Output(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class OutputCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Keygen(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class KeygenCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TextAreaCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class OptionCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class OptGroup(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class OptGroupCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class DataList(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class DataListCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class SelectCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class ButtonCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Input(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class InputCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Label(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class LabelCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class FormCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableCellCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableHeaderCell(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableHeaderCellCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableDataCellCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableRowCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableSectionCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableCol(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableColCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableCaption(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TableCaptionCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class AreaCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Map(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MapCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Media(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MediaCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Audio(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class AudioCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Video(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class VideoCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Track(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TrackCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Param(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class ParamCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Object(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class ObjectCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Embed(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class EmbedCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class IFrameCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class ImageCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Source(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class SourceCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Picture(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class PictureCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Mod(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class ModCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class BR(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class BRCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Span(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class SpanCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Time(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TimeCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Data(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class DataCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class AnchorCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Div(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class DivCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class DListCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class LI(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class LICollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class UListCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class OListCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Quote(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class QuoteCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Pre(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class PreCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class HR(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class HRCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Paragraph(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class ParagraphCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Heading(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class HeadingCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Body(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class BodyCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Style(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class StyleCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Meta(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class MetaCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Base(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class BaseCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Title(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class TitleCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Head(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class HeadCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Html(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class HtmlCollection(HTMLElementCollection):
    pass


@six.add_metaclass(MetaHTMLElement)
class Unknown(HTMLElement):
    pass


@six.add_metaclass(MetaHTMLElement)
class UnknownCollection(HTMLElementCollection):
    pass
