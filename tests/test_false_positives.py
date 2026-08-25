"""Tests verifying zero false positives on clean, idiomatic Lua code."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.hazards_rules import (
    GlobalVariableLeakHazardRule,
    NilIndexingMetatableHazardRule,
    TableRehashLoopHazardRule,
)
from pattern_detector.domain.rules.solid_principles_rules import MonolithicModuleSrpRule


def test_clean_local_variables_no_global_leak() -> None:
    code = """
local score = 100
local name = "hero"
local function get_score()
    return score
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("clean.lua", code)])

    rule = GlobalVariableLeakHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_preallocated_table_no_rehash_hazard() -> None:
    code = """
local function populate_items(raw_data)
    local items = table.create(#raw_data)
    for i, v in ipairs(raw_data) do
        table.insert(items, v.name)
    end
    return items
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("clean_prealloc.lua", code)])

    rule = TableRehashLoopHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_guarded_indexing_no_nil_hazard() -> None:
    code = """
local function get_damage(player)
    if player and player.inventory and player.inventory.weapons then
        return player.inventory.weapons.primary.damage
    end
    return 0
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("guarded.lua", code)])

    rule = NilIndexingMetatableHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_small_module_no_srp() -> None:
    code = """
local MathUtil = {}

function MathUtil.add(a, b) return a + b end
function MathUtil.sub(a, b) return a - b end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("math_util.lua", code)])

    rule = MonolithicModuleSrpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0
