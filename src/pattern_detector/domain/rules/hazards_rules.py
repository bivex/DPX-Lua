"""Hazards, Memory Leaks, and Anti-pattern rules for Lua & Luau."""

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


class GlobalVariableLeakHazardRule(BaseRule):
    """Detects unintentional global variable assignments polluting _G without the 'local' keyword."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for g in model.all_global_assignments:
            evidences = [
                Evidence(
                    rule_code="HAZARD_GLOBAL_LEAK",
                    description=f"Variable '{g.name}' is assigned globally without 'local' keyword, contaminating _G global namespace and risking GC memory leak",
                    weight=0.92,
                    location=g.location,
                )
            ]
            detections.append(
                Detection(
                    pattern_type=PatternType.GLOBAL_VARIABLE_LEAK_HAZARD,
                    pattern_category=PatternCategory.HAZARDS_MEMORY_LEAK,
                    target_name=g.name,
                    target_kind="variable",
                    confidence=Confidence(score=0.92, evidences=evidences),
                    primary_location=g.location,
                    evidences=evidences,
                )
            )
        return detections


class TableRehashLoopHazardRule(BaseRule):
    """Detects table.insert or dynamic key insertions inside hot loops without preallocation."""

    INSERT_IN_LOOP_PATTERN = re.compile(r"\bfor\s+[a-zA-Z0-9_,\s]+\s+in\s+.*?\bdo[\s\S]*?\btable\.insert\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.INSERT_IN_LOOP_PATTERN.search(fn.body) and "table.create" not in fn.body:
                evidences = [
                    Evidence(
                        rule_code="HAZARD_TABLE_REHASH_LOOP",
                        description=f"Function '{fn.name}' inserts into un-preallocated table inside a loop, causing GC pressure and repetitive hash array rehashing",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TABLE_REHASH_LOOP_HAZARD,
                        pattern_category=PatternCategory.HAZARDS_MEMORY_LEAK,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class NilIndexingMetatableHazardRule(BaseRule):
    """Detects unsafe deep chained table indexing without nil guards."""

    DEEP_INDEX_PATTERN = re.compile(r"[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.DEEP_INDEX_PATTERN.search(fn.body) and "if " not in fn.body:
                evidences = [
                    Evidence(
                        rule_code="HAZARD_NIL_INDEXING",
                        description=f"Function '{fn.name}' performs deep chained indexing without nil guards, risking 'attempt to index a nil value' crash",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.NIL_INDEXING_METATABLE_HAZARD,
                        pattern_category=PatternCategory.HAZARDS_MEMORY_LEAK,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class CoroutineUnhandledDeadlockHazardRule(BaseRule):
    """Detects coroutine.yield() without a scheduled resume keeper or error handler."""

    YIELD_PATTERN = re.compile(r"\bcoroutine\.yield\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.YIELD_PATTERN.search(fn.body) and "coroutine.resume" not in fn.body and "task.spawn" not in fn.body:
                evidences = [
                    Evidence(
                        rule_code="HAZARD_COROUTINE_DEADLOCK",
                        description=f"Function '{fn.name}' yields coroutine execution without local resume keeper or timeout monitor",
                        weight=0.85,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COROUTINE_UNHANDLED_DEADLOCK_HAZARD,
                        pattern_category=PatternCategory.HAZARDS_MEMORY_LEAK,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.85, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
