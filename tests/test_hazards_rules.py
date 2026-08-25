"""Unit tests for Lua & Luau hazards, leaks, and anti-patterns."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.hazards_rules import (
    CoroutineUnhandledDeadlockHazardRule,
    GlobalVariableLeakHazardRule,
    NilIndexingMetatableHazardRule,
    TableRehashLoopHazardRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_global_variable_leak_hazard() -> None:
    code = """
score = 100
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("leak.lua", code)])

    rule = GlobalVariableLeakHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.GLOBAL_VARIABLE_LEAK_HAZARD


def test_table_rehash_loop_hazard() -> None:
    code = """
local function populate_items(raw_data)
    local items = {}
    for i, v in ipairs(raw_data) do
        table.insert(items, v.name)
    end
    return items
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("loop.lua", code)])

    rule = TableRehashLoopHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TABLE_REHASH_LOOP_HAZARD


def test_nil_indexing_metatable_hazard() -> None:
    code = """
local function get_nested_val(player)
    return player.inventory.weapons.primary.damage
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("nil.lua", code)])

    rule = NilIndexingMetatableHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.NIL_INDEXING_METATABLE_HAZARD


def test_coroutine_unhandled_deadlock_hazard() -> None:
    code = """
local function worker()
    coroutine.yield("waiting forever")
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("worker.lua", code)])

    rule = CoroutineUnhandledDeadlockHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COROUTINE_UNHANDLED_DEADLOCK_HAZARD
