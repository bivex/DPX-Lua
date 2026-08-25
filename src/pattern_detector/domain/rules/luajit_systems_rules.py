"""LuaJIT FFI and systems performance optimization rules."""

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


class LuajitFfiCBindingRule(BaseRule):
    """Detects direct C ABI calling and memory access via LuaJIT FFI (ffi.cdef / ffi.load)."""

    FFI_PATTERN = re.compile(r"\bffi\.(?:cdef|load|new|cast|typeof|copy|fill)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_ffi or self.FFI_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="LUAJIT_FFI_C_BINDING",
                        description=f"Function '{fn.name}' calls native C ABI directly via LuaJIT FFI",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.LUAJIT_FFI_C_BINDING,
                        pattern_category=PatternCategory.LUAJIT_FFI_SYSTEMS,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TablePreallocationCacheRule(BaseRule):
    """Detects table pre-allocation (table.create(N)) to prevent hash rehashing GC churn."""

    PREALLOC_PATTERN = re.compile(r"\btable\.(?:create|clone|clear)\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.PREALLOC_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="LUA_TABLE_PREALLOCATION",
                        description=f"Function '{fn.name}' pre-allocates table capacity to eliminate dynamic rehash overhead",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TABLE_PREALLOCATION_CACHE,
                        pattern_category=PatternCategory.LUAJIT_FFI_SYSTEMS,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class PackedBitfieldManipulationRule(BaseRule):
    """Detects bitwise manipulation via bit/bit32 libraries (bit.band, bit.bor, bit.lshift)."""

    BIT_PATTERN = re.compile(r"\b(?:bit|bit32)\.(?:band|bor|bxor|bnot|lshift|rshift|arshift)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if self.BIT_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="LUA_PACKED_BITFIELD",
                        description=f"Function '{fn.name}' performs bitwise flags manipulation via bit/bit32 primitives",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PACKED_BITFIELD_MANIPULATION,
                        pattern_category=PatternCategory.LUAJIT_FFI_SYSTEMS,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
