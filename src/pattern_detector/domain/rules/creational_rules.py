"""GoF Creational design pattern detection rules for Lua & Luau (5/5)."""

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


class SingletonModuleCacheRule(BaseRule):
    """Detects Singleton pattern via module caching in package.loaded or singleton instance tables."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Singleton" in c.name or "Registry" in c.name or "Instance" in c.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_SINGLETON_CACHE",
                        description=f"Table '{c.name}' acts as a Singleton coordinator cached across require() calls",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.SINGLETON_MODULE_CACHE,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class FactoryConstructorMethodRule(BaseRule):
    """Detects Factory pattern constructor methods (Class:new(...) or create_object(...))."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("new", "create", "instantiate", "spawn") or fn.name.startswith("create_"):
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_FACTORY_CONSTRUCTOR",
                        description=f"Function/Method '{fn.name}' implements Factory Constructor initializing and returning configured instance tables",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FACTORY_CONSTRUCTOR_METHOD,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class AbstractFactoryThemeProviderRule(BaseRule):
    """Detects Abstract Factory creating families of related UI or game objects."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Factory" in c.name or "Provider" in c.name:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_ABSTRACT_FACTORY_THEME",
                        description=f"Table '{c.name}' implements Abstract Factory pattern generating families of UI or game entity objects",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ABSTRACT_FACTORY_THEME_PROVIDER,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class BuilderFluentTableConfigRule(BaseRule):
    """Detects Builder fluent method chaining returning 'self'."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.is_method and "return self" in fn.body:
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_BUILDER_FLUENT_CHAIN",
                        description=f"Method '{fn.name}' implements Builder fluent chaining returning 'self' for method cascading",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.BUILDER_FLUENT_TABLE_CONFIG,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class PrototypeDeepCloneTableRule(BaseRule):
    """Detects Prototype deep table cloning."""

    CLONE_PATTERN = re.compile(r"\bfunction\s+(?:[a-zA-Z0-9_]+[:.])?(?:clone|deep_copy|copy)\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("clone", "deep_copy", "deepcopy", "copy") or self.CLONE_PATTERN.search(fn.raw_text):
                evidences = [
                    Evidence(
                        rule_code="CREATIONAL_PROTOTYPE_CLONE",
                        description=f"Function '{fn.name}' implements Prototype pattern cloning tables and nested metatables for new instances",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PROTOTYPE_DEEP_CLONE_TABLE,
                        pattern_category=PatternCategory.CREATIONAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
