import six

from .element import Element
from ..element_collection import ElementCollection
from ..meta_elements import MetaSVGElement


@six.add_metaclass(MetaSVGElement)
class SVGElement(Element):
    pass


@six.add_metaclass(MetaSVGElement)
class SVGElementCollection(ElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class MPath(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MPathCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Animation(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class AnimationCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class AnimateTransform(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class AnimateTransformCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class AnimateMotion(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class AnimateMotionCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Set(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class SetCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Animate(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class AnimateCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class View(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class ViewCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Cursor(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class CursorCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Pattern(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class PatternCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Stop(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class StopCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshPatch(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshPatchCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshRow(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshRowCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Gradient(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class GradientCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshGradient(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshGradientCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class RadialGradient(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class RadialGradientCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class LinearGradient(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class LinearGradientCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Marker(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MarkerCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Symbol(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class SymbolCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Metadata(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MetadataCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Desc(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class DescCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Graphics(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class GraphicsCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class ForeignObject(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class ForeignObjectCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class TextContent(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class TextContentCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class TextPath(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class TextPathCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class TextPositioning(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class TextPositioningCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class TSpan(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class TSpanCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Switch(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class SwitchCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Use(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class UseCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Defs(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class DefsCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class G(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class GCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class SVG(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class SVGCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Geometry(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class GeometryCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Polygon(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class PolygonCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Polyline(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class PolylineCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Line(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class LineCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Ellipse(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class EllipseCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Circle(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class CircleCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Rect(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class RectCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Path(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class PathCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Hatchpath(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class HatchpathCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Hatch(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class HatchCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Meshpatch(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshpatchCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Meshrow(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshrowCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Solidcolor(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class SolidcolorCollection(SVGElementCollection):
    pass


@six.add_metaclass(MetaSVGElement)
class Mesh(SVGElement):
    pass


@six.add_metaclass(MetaSVGElement)
class MeshCollection(SVGElementCollection):
    pass
