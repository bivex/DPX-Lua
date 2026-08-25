"""SOLID principles and code quality rules for Lua & Luau."""

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


class MonolithicModuleSrpRule(BaseRule):
    """Detects monolithic module tables declaring excessive functions (>= 15), violating Single Responsibility."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if c.total_methods_count >= 15:
                evidences = [
                    Evidence(
                        rule_code="SRP_MONOLITHIC_MODULE",
                        description=f"Module/Table '{c.name}' defines {c.total_methods_count} methods; consider decomposing into cohesive sub-modules",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MONOLITHIC_MODULE_SRP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=c.name,
                        target_kind="module",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class FatMetatableInterfaceIspRule(BaseRule):
    """Detects fat class metatables defining excessive methods (>= 12), violating Interface Segregation."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if c.has_setmetatable and c.total_methods_count >= 12:
                evidences = [
                    Evidence(
                        rule_code="ISP_FAT_METATABLE_INTERFACE",
                        description=f"Class metatable '{c.name}' defines {c.total_methods_count} methods; decompose into focused role traits or mixins",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.FAT_METATABLE_INTERFACE_ISP,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class DeepTableNestingDemeterRule(BaseRule):
    """Detects deep chained table property access (>= 4 levels e.g. a.b.c.d.e), violating Law of Demeter."""

    CHAIN_PATTERN = re.compile(r"\b[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+){4,}\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            matches = self.CHAIN_PATTERN.findall(fn.body)
            if matches:
                evidences = [
                    Evidence(
                        rule_code="DEMETER_DEEP_TABLE_NESTING",
                        description=f"Function '{fn.name}' chains deep table access ('{matches[0]}'); encapsulate in intermediate helper methods",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.DEEP_TABLE_NESTING_DEMETER,
                        pattern_category=PatternCategory.PRINCIPLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
