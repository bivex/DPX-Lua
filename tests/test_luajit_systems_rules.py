"""Unit tests for LuaJIT FFI and systems optimization rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.luajit_systems_rules import (
    LuajitFfiCBindingRule,
    PackedBitfieldManipulationRule,
    TablePreallocationCacheRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_luajit_ffi_c_binding() -> None:
    code = """
local function init_c_audio()
    ffi.cdef[[
        typedef struct { float x, y, z; } Vec3;
        void play_sound_native(int id, float volume);
    ]]
    local lib = ffi.load("audio_engine")
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("ffi.lua", code)])

    rule = LuajitFfiCBindingRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.LUAJIT_FFI_C_BINDING


def test_table_preallocation_cache() -> None:
    code = """
local function create_particles(count)
    local pool = table.create(count)
    for i = 1, count do
        pool[i] = { x = 0, y = 0 }
    end
    return pool
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("pool.lua", code)])

    rule = TablePreallocationCacheRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TABLE_PREALLOCATION_CACHE


def test_packed_bitfield_manipulation() -> None:
    code = """
local function check_flags(flags, mask)
    return bit.band(flags, mask) ~= 0
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("flags.lua", code)])

    rule = PackedBitfieldManipulationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PACKED_BITFIELD_MANIPULATION
