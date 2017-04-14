import six

from .element import Element
from ..meta_elements import MetaSVGElement


@six.add_metaclass(MetaSVGElement)
class SVGElement(Element):
    pass

# TODO: collection
@six.add_metaclass(MetaSVGElement)
class SVGElementCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MPath(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MPathCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Animation(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class AnimationCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class AnimateTransform(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class AnimateTransformCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class AnimateMotion(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class AnimateMotionCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Set(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class SetCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Animate(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class AnimateCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class View(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class ViewCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Cursor(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class CursorCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Pattern(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class PatternCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Stop(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class StopCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MeshPatch(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MeshPatchCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MeshRow(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MeshRowCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Gradient(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class GradientCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MeshGradient(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MeshGradientCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class RadialGradient(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class RadialGradientCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class LinearGradient(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class LinearGradientCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Marker(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MarkerCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Symbol(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class SymbolCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Metadata(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class MetadataCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Desc(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class DescCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Graphics(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class GraphicsCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class ForeignObject(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class ForeignObjectCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TextContent(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TextContentCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TextPath(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TextPathCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TextPositioning(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TextPositioningCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TSpan(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class TSpanCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Switch(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class SwitchCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Use(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class UseCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Defs(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class DefsCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class G(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class GCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class SVG(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class SVGCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Geometry(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class GeometryCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Polygon(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class PolygonCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Polyline(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class PolylineCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Line(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class LineCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Ellipse(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class EllipseCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Circle(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class CircleCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Rect(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class RectCollection(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class Path(SVGElement):
    pass

@six.add_metaclass(MetaSVGElement)
class PathCollection(SVGElement):
    pass

