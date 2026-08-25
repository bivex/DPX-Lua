"""Unit tests for Lua & Luau Idiomatic and Metatable OOP rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.idiomatic_rules import (
    ClosureModuleEncapsulationRule,
    CoroutineCooperativeTaskRule,
    LuauStaticTypeAnnotationRule,
    MetatablePrototypeOopRule,
    OperatorOverloadingMetamethodsRule,
    PcallXpcallRailwayErrorRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_metatable_prototype_oop() -> None:
    code = """
local Player = {}
Player.__index = Player

function Player.new(name)
    local self = setmetatable({}, Player)
    self.name = name
    return self
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("player.lua", code)])

    rule = MetatablePrototypeOopRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.METATABLE_PROTOTYPE_OOP


def test_operator_overloading_metamethods() -> None:
    code = """
local Vector2 = {}
Vector2.__index = Vector2
Vector2.__add = function(a, b) return Vector2.new(a.x + b.x, a.y + b.y) end
Vector2.__tostring = function(self) return string.format("(%f, %f)", self.x, self.y) end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("vec.lua", code)])

    rule = OperatorOverloadingMetamethodsRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.OPERATOR_OVERLOADING_METAMETHODS


def test_closure_module_encapsulation() -> None:
    code = """
local M = {}
local private_counter = 0

function M.increment()
    private_counter = private_counter + 1
    return private_counter
end

return M
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("counter.lua", code)])

    rule = ClosureModuleEncapsulationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CLOSURE_MODULE_ENCAPSULATION


def test_coroutine_cooperative_task() -> None:
    code = """
local function game_loop()
    local co = coroutine.create(function()
        for i = 1, 10 do
            coroutine.yield(i)
        end
    end)
    return co
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("loop.lua", code)])

    rule = CoroutineCooperativeTaskRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COROUTINE_COOPERATIVE_TASK


def test_luau_static_type_annotation() -> None:
    code = """
export type PlayerData = {
    level: number,
    coins: number,
    inventory: { string }
}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("types.luau", code)])

    rule = LuauStaticTypeAnnotationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.LUAU_STATIC_TYPE_ANNOTATION


def test_pcall_xpcall_railway_error() -> None:
    code = """
local function safe_parse(json_str)
    local success, result = pcall(http.parse_json, json_str)
    if not success then
        return nil, result
    end
    return result
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("parse.lua", code)])

    rule = PcallXpcallRailwayErrorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PCALL_XPCALL_RAILWAY_ERROR
