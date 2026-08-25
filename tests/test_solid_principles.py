"""Unit tests for SOLID principles and smells in Lua & Luau."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.solid_principles_rules import (
    DeepTableNestingDemeterRule,
    FatMetatableInterfaceIspRule,
    MonolithicModuleSrpRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_monolithic_module_srp() -> None:
    methods = "\n".join([f"function MegaModule.fn{i}() end" for i in range(16)])
    code = f"""
local MegaModule = {{}}
{methods}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("mega.lua", code)])

    rule = MonolithicModuleSrpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MONOLITHIC_MODULE_SRP


def test_fat_metatable_interface_isp() -> None:
    methods = "\n".join([f"function FatClass:method{i}() end" for i in range(13)])
    code = f"""
local FatClass = setmetatable({{}}, {{}})
{methods}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("fat.lua", code)])

    rule = FatMetatableInterfaceIspRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FAT_METATABLE_INTERFACE_ISP


def test_deep_table_nesting_demeter() -> None:
    code = """
local function process(order)
    local zip = order.customer.profile.address.country.zipcode
    return zip
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("demeter.lua", code)])

    rule = DeepTableNestingDemeterRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DEEP_TABLE_NESTING_DEMETER
