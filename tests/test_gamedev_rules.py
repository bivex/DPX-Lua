"""Unit tests for Lua GameDev (Roblox, Neovim, Love2D) rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.gamedev_rules import (
    EcsComponentTableLayoutRule,
    EventSignalListenerBusRule,
    NeovimPluginApiFacadeRule,
    RobloxInstanceReplicationBridgeRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_roblox_instance_replication_bridge() -> None:
    code = """
local function spawn_effect(pos)
    local part = Instance.new("Part")
    part.Position = pos
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    local RemoteEvent = ReplicatedStorage.PlaySound
    RemoteEvent:FireServer("explosion")
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("roblox.lua", code)])

    rule = RobloxInstanceReplicationBridgeRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ROBLOX_INSTANCE_REPLICATION_BRIDGE


def test_ecs_component_table_layout() -> None:
    code = """
local ECSWorld = {}
ECSWorld.__index = ECSWorld

function ECSWorld.new()
    return setmetatable({ components = {}, entities = {} }, ECSWorld)
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("ecs.lua", code)])

    rule = EcsComponentTableLayoutRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ECS_COMPONENT_TABLE_LAYOUT


def test_neovim_plugin_api_facade() -> None:
    code = """
local function setup_keymaps()
    vim.keymap.set("n", "<leader>ff", "<cmd>Telescope find_files<cr>")
    vim.api.nvim_create_user_command("ReloadConfig", function() end, {})
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("nvim.lua", code)])

    rule = NeovimPluginApiFacadeRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.NEOVIM_PLUGIN_API_FACADE


def test_event_signal_listener_bus() -> None:
    code = """
local CustomSignal = {}
CustomSignal.__index = CustomSignal

function CustomSignal:Connect(fn)
    table.insert(self.listeners, fn)
end

function CustomSignal:Fire(...)
    for _, fn in ipairs(self.listeners) do
        fn(...)
    end
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("signal.lua", code)])

    rule = EventSignalListenerBusRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.EVENT_SIGNAL_LISTENER_BUS
