"""Lua & Luau Idiomatic and Metatable OOP architectural rules."""

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


class MetatablePrototypeOopRule(BaseRule):
    """Detects prototype-based OOP via setmetatable(self, Class) and __index dispatch."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if c.has_setmetatable or "__index" in c.metamethods or any(fn.name in ("new", "init", "create") for fn in c.methods):
                evidences = [
                    Evidence(
                        rule_code="LUA_METATABLE_PROTOTYPE_OOP",
                        description=f"Class/Table '{c.name}' implements Metatable Prototype OOP with {len(c.methods)} method(s) and __index dispatch",
                        weight=0.95,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.METATABLE_PROTOTYPE_OOP,
                        pattern_category=PatternCategory.LUA_IDIOMATIC_METATABLE,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class OperatorOverloadingMetamethodsRule(BaseRule):
    """Detects operator overloading metamethods (__add, __sub, __mul, __tostring, __call)."""

    OPERATOR_METAS = {"__add", "__sub", "__mul", "__div", "__mod", "__pow", "__unm", "__concat", "__len", "__eq", "__lt", "__le", "__tostring", "__call"}

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            matched = [m for m in c.metamethods if m in self.OPERATOR_METAS]
            if matched:
                evidences = [
                    Evidence(
                        rule_code="LUA_OPERATOR_OVERLOADING_META",
                        description=f"Class '{c.name}' overloads operator metamethod(s): {', '.join(matched)}",
                        weight=0.95,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.OPERATOR_OVERLOADING_METAMETHODS,
                        pattern_category=PatternCategory.LUA_IDIOMATIC_METATABLE,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class ClosureModuleEncapsulationRule(BaseRule):
    """Detects local module table encapsulation (local M = {} ... return M)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for f in model.files:
            if any(c.is_local for c in f.classes) and "return " in f.raw_content:
                local_cls = [c.name for c in f.classes if c.is_local]
                name = local_cls[0] if local_cls else "Module"
                evidences = [
                    Evidence(
                        rule_code="LUA_CLOSURE_MODULE_ENCAPSULATION",
                        description=f"Module in '{f.file_path}' encapsulates private state in local upvalues returning public API table '{name}'",
                        weight=0.92,
                        location=f.classes[0].location if f.classes else None,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.CLOSURE_MODULE_ENCAPSULATION,
                        pattern_category=PatternCategory.LUA_IDIOMATIC_METATABLE,
                        target_name=name,
                        target_kind="module",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=f.classes[0].location if f.classes else None,
                        evidences=evidences,
                    )
                )
        return detections


class CoroutineCooperativeTaskRule(BaseRule):
    """Detects cooperative multitasking via coroutine.create, resume, and yield."""

    CORO_PATTERN = re.compile(r"\bcoroutine\.(?:create|resume|yield|wrap|status|running)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_coroutine or self.CORO_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="LUA_COROUTINE_COOPERATIVE",
                        description=f"Function '{fn.name}' implements cooperative task scheduling / frame yielding via coroutine primitives",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COROUTINE_COOPERATIVE_TASK,
                        pattern_category=PatternCategory.LUA_IDIOMATIC_METATABLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class LuauStaticTypeAnnotationRule(BaseRule):
    """Detects Luau gradual static typing ('type Vector3 = { x: number, y: number }')."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for t in model.all_type_aliases:
            evidences = [
                Evidence(
                    rule_code="LUAU_STATIC_TYPE_ANNOTATION",
                    description=f"Luau type alias '{t.name}' enforces gradual static type checking ('{t.type_def}')",
                    weight=0.95,
                    location=t.location,
                )
            ]
            detections.append(
                Detection(
                    pattern_type=PatternType.LUAU_STATIC_TYPE_ANNOTATION,
                    pattern_category=PatternCategory.LUA_IDIOMATIC_METATABLE,
                    target_name=t.name,
                    target_kind="type",
                    confidence=Confidence(score=0.95, evidences=evidences),
                    primary_location=t.location,
                    evidences=evidences,
                )
            )
        return detections


class PcallXpcallRailwayErrorRule(BaseRule):
    """Detects safe error handling via pcall(fn, ...) / xpcall(fn, err_handler)."""

    PCALL_PATTERN = re.compile(r"\b(pcall|xpcall)\s*\(")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_pcall or self.PCALL_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="LUA_PCALL_PROTECTED_ERROR",
                        description=f"Function '{fn.name}' executes protected call (pcall/xpcall) capturing runtime failures safely",
                        weight=0.92,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.PCALL_XPCALL_RAILWAY_ERROR,
                        pattern_category=PatternCategory.LUA_IDIOMATIC_METATABLE,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
