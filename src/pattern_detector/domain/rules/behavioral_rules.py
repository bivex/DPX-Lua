"""GoF Behavioral design pattern detection rules for Lua & Luau (11/11)."""

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


class ChainOfResponsibilityMiddlewareRule(BaseRule):
    """Detects Chain of Responsibility middleware functions forwarding requests."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "next" in fn.parameters and ("next(" in fn.body or "next_handler" in fn.name):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_CHAIN_MIDDLEWARE",
                        description=f"Function '{fn.name}' implements Chain of Responsibility pipeline passing control to 'next' handler",
                        weight=0.88,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class CommandUndoRedoPayloadRule(BaseRule):
    """Detects Command pattern encapsulating actions as tables with execute() and undo()."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            has_exec = any(fn.name in ("execute", "redo", "apply") for fn in c.methods)
            has_undo = any(fn.name in ("undo", "revert", "rollback") for fn in c.methods)
            if has_exec and has_undo:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_COMMAND_PAYLOAD",
                        description=f"Table '{c.name}' encapsulates reversible action with execute() and undo() methods (Command pattern)",
                        weight=0.95,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.COMMAND_UNDO_REDO_PAYLOAD,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class InterpreterDslEvaluatorRule(BaseRule):
    """Detects Interpreter pattern evaluating table-based ASTs or mini-language domain expressions."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("eval", "evaluate", "interpret", "exec_ast", "eval_expr") or "Interpreter" in fn.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_INTERPRETER_DSL",
                        description=f"Function '{fn.name}' evaluates domain AST or mini-language DSL instructions",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.INTERPRETER_DSL_EVALUATOR,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class IteratorStatelessPairsIpairsRule(BaseRule):
    """Detects custom stateless or stateful iterator functions (generic for-loop protocol)."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name.startswith("iter") or fn.name in ("iterate", "items", "entries", "values", "keys"):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_ITERATOR_CUSTOM",
                        description=f"Function '{fn.name}' implements custom iterator generator conforming to Lua generic for-loop protocol",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ITERATOR_STATELESS_PAIRS_IPAIRS,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class MediatorGameEventCoordinatorRule(BaseRule):
    """Detects Mediator pattern coordinating communication across game subsystems."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "Mediator" in c.name or "Coordinator" in c.name or "EventManager" in c.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_MEDIATOR_COORDINATOR",
                        description=f"Table '{c.name}' acts as a central Mediator coordinating decoupled game subsystems",
                        weight=0.88,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MEDIATOR_GAME_EVENT_COORDINATOR,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.88, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class MementoTableSnapshotRule(BaseRule):
    """Detects Memento state snapshots for savestates, rollback netcode, and checkpoints."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.name in ("save_state", "restore_state", "serialize_state", "snapshot", "create_checkpoint") or "Snapshot" in fn.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_MEMENTO_SNAPSHOT",
                        description=f"Function '{fn.name}' captures or restores state snapshots (Memento pattern)",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.MEMENTO_TABLE_SNAPSHOT,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class ObserverSignalListenerRule(BaseRule):
    """Detects Observer pattern dispatching notifications to subscriber callbacks."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            has_sub = any(fn.name in ("subscribe", "listen", "on", "watch", "add_listener") for fn in c.methods)
            has_pub = any(fn.name in ("notify", "emit", "publish", "dispatch", "fire") for fn in c.methods)
            if has_sub or has_pub or "Observer" in c.name or "Broadcaster" in c.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_OBSERVER_SIGNAL",
                        description=f"Table '{c.name}' implements Observer pattern dispatching event notifications to listeners",
                        weight=0.90,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.OBSERVER_SIGNAL_LISTENER,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class StateMachineTableFsmRule(BaseRule):
    """Detects Finite State Machine managing states via tables of enter, update, exit hooks."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            has_fsm_hooks = any(fn.name in ("change_state", "transition_to", "set_state", "enter", "exit") for fn in c.methods)
            if has_fsm_hooks or "FSM" in c.name or "StateMachine" in c.name:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_STATE_FSM",
                        description=f"Class/Table '{c.name}' implements Finite State Machine managing transitions and lifecycle states",
                        weight=0.92,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.STATE_MACHINE_TABLE_FSM,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class StrategyTableFunctionInjectionRule(BaseRule):
    """Detects Strategy pattern injecting algorithm closures into algorithms."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if "strategy" in [p.lower() for p in fn.parameters] or "comparator" in [p.lower() for p in fn.parameters]:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_STRATEGY_INJECTION",
                        description=f"Function '{fn.name}' accepts interchangeable strategy closures (Strategy pattern)",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.STRATEGY_TABLE_FUNCTION_INJECTION,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class TemplateMethodHookLifecycleRule(BaseRule):
    """Detects Template Method lifecycle skeleton coordinating optional hook overrides."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            has_update = any(fn.name == "update" for fn in c.methods)
            has_hooks = any(fn.name.startswith("on_") or fn.name.startswith("before_") or fn.name.startswith("after_") for fn in c.methods)
            if has_update and has_hooks:
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_TEMPLATE_METHOD",
                        description=f"Class '{c.name}' defines Template Method lifecycle skeleton coordinating extensible hook callbacks",
                        weight=0.90,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.TEMPLATE_METHOD_HOOK_LIFECYCLE,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class VisitorSceneWalkerRule(BaseRule):
    """Detects Visitor pattern traversing nested table hierarchies with node callbacks."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if (
                fn.name in ("visit", "walk", "traverse", "accept")
                or fn.name.startswith("walk_")
                or fn.name.startswith("visit_")
                or fn.name.startswith("traverse_")
                or "Visitor" in fn.name
            ):
                evidences = [
                    Evidence(
                        rule_code="BEHAVIORAL_VISITOR_WALKER",
                        description=f"Function '{fn.name}' implements Visitor pattern traversing hierarchical table nodes with callbacks",
                        weight=0.90,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.VISITOR_SCENE_WALKER,
                        pattern_category=PatternCategory.BEHAVIORAL,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections
