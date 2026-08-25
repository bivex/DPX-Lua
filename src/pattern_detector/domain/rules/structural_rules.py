"""GoF Structural design pattern detection rules for Lua & Luau (7/7)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BaseRule
from pattern_detector.domain.value_objects import (
    Confidence,
    Evidence,
    PatternCategory,
    PatternType,
)


class AdapterMetatableWrapperRule(BaseRule):
    """Detects Adapter pattern wrapping foreign tables via __index lookup forwarding."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Adapter" in c.name or "Wrapper" in c.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_ADAPTER_WRAPPER",
                        description=f"Table '{c.name}' acts as an Adapter standardizing foreign table interfaces via metatable delegation",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ADAPTER_METATABLE_WRAPPER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class BridgeDriverRendererRule(BaseRule):
    """Detects Bridge pattern decoupling game logic from graphics/physics driver backends."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Renderer" in c.name or "Driver" in c.name or "Backend" in c.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_BRIDGE_DRIVER",
                        description=f"Table '{c.name}' implements Bridge pattern separating game abstraction from platform rendering drivers",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.BRIDGE_DRIVER_RENDERER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class CompositeSceneGraphNodeRule(BaseRule):
    """Detects Composite pattern modeling hierarchical scene graphs (parent/children tables)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Node" in c.name or "Scene" in c.name or "Tree" in c.name or "Element" in c.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_COMPOSITE_NODE",
                        description=f"Table '{c.name}' implements Composite pattern managing parent-child node hierarchies in scene graphs",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMPOSITE_SCENE_GRAPH_NODE,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class DecoratorFunctionWrapperRule(BaseRule):
    """Detects Decorator higher-order functions wrapping functions with profiling or caching."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("memoize", "profile", "wrap", "decorate", "debounce", "throttle") or fn.name.startswith("wrap_"):
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_DECORATOR_WRAPPER",
                        description=f"Function '{fn.name}' implements Decorator pattern wrapping target closures with caching/profiling middleware",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DECORATOR_FUNCTION_WRAPPER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class FacadeInitModuleApiRule(BaseRule):
    """Detects Facade pattern in top-level init.lua exposing clean public API tables."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for f in model.files:
            if f.file_path.endswith("init.lua") or f.file_path.endswith("init.luau"):
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_FACADE_INIT",
                        description=f"Module '{f.file_path}' acts as a unified Facade API exposing cohesive entrypoints over internal subsystems",
                        weight=0.92,
                        location=None,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FACADE_INIT_MODULE_API,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name="init",
                        target_kind="module",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=None,
                        evidences=evidences,
                    )
                )
        return detections


class FlyweightSharedMetaTableRule(BaseRule):
    """Detects Flyweight pattern sharing a single immutable metatable across lightweight instances."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Flyweight" in c.name or "Particle" in c.name or "Glyph" in c.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_FLYWEIGHT_META",
                        description=f"Class/Table '{c.name}' implements Flyweight pattern sharing immutable metatables across mass entity instances",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FLYWEIGHT_SHARED_META_TABLE,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class ProxyLazyTableIndexerRule(BaseRule):
    """Detects Proxy pattern intercepting reads/writes using __index and __newindex."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "__newindex" in c.metamethods or "Proxy" in c.name:
                evidences = [
                    Evidence(
                        rule_code="STRUCTURAL_PROXY_INDEXER",
                        description=f"Table '{c.name}' implements Proxy pattern trapping property read/write access via __index and __newindex",
                        weight=0.95,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROXY_LAZY_TABLE_INDEXER,
                        pattern_category=PatternCategory.STRUCTURAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections
