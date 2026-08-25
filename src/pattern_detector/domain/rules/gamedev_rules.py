"""GameDev (Roblox, Neovim, Love2D) and Extension architecture rules for Lua & Luau."""

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


class RobloxInstanceReplicationBridgeRule(BaseRule):
    """Detects Roblox Engine Client/Server networking and Instance lifecycle."""

    ROBLOX_PATTERN = re.compile(r"\b(game:GetService|Instance\.new|RemoteEvent|RemoteFunction|BindableEvent|Players\.LocalPlayer)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_roblox or self.ROBLOX_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="GAMEDEV_ROBLOX_REPLICATION",
                        description=f"Function '{fn.name}' integrates with Roblox Engine networking (RemoteEvent / Instance.new / Service APIs)",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ROBLOX_INSTANCE_REPLICATION_BRIDGE,
                        pattern_category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class EcsComponentTableLayoutRule(BaseRule):
    """Detects Entity Component System (ECS) data-oriented tables."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            if "ECS" in c.name or "World" in c.name or "Component" in c.name or "System" in c.name:
                evidences = [
                    Evidence(
                        rule_code="GAMEDEV_ECS_COMPONENT_LAYOUT",
                        description=f"Class/Table '{c.name}' implements Data-Oriented Entity Component System (ECS) architecture",
                        weight=0.90,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.ECS_COMPONENT_TABLE_LAYOUT,
                        pattern_category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.90, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections


class NeovimPluginApiFacadeRule(BaseRule):
    """Detects Neovim Lua extension integration (vim.api, vim.keymap, vim.lsp)."""

    NVIM_PATTERN = re.compile(r"\bvim\.(api|keymap|lsp|fn|opt|cmd)\b")

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for fn in model.all_functions:
            if fn.has_neovim or self.NVIM_PATTERN.search(fn.body):
                evidences = [
                    Evidence(
                        rule_code="GAMEDEV_NEOVIM_API_FACADE",
                        description=f"Function '{fn.name}' integrates with Neovim C-API / editor subsystem via vim.* facades",
                        weight=0.95,
                        location=fn.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.NEOVIM_PLUGIN_API_FACADE,
                        pattern_category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
                        target_name=fn.name,
                        target_kind="fn",
                        confidence=Confidence(score=0.95, evidences=evidences),
                        primary_location=fn.location,
                        evidences=evidences,
                    )
                )
        return detections


class EventSignalListenerBusRule(BaseRule):
    """Detects custom Signal/Event dispatcher pattern (:Connect(fn) and :Fire(...))."""

    def evaluate(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []
        for c in model.all_classes:
            has_signal = any(fn.name in ("Connect", "connect", "Fire", "fire", "Disconnect", "disconnect") for fn in c.methods)
            if has_signal or "Signal" in c.name or "Emitter" in c.name:
                evidences = [
                    Evidence(
                        rule_code="GAMEDEV_EVENT_SIGNAL_BUS",
                        description=f"Class/Table '{c.name}' implements custom Signal/Event listener subscription bus (:Connect / :Fire)",
                        weight=0.92,
                        location=c.location,
                    )
                ]
                detections.append(
                    Detection(
                        pattern_type=PatternType.EVENT_SIGNAL_LISTENER_BUS,
                        pattern_category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
                        target_name=c.name,
                        target_kind="class",
                        confidence=Confidence(score=0.92, evidences=evidences),
                        primary_location=c.location,
                        evidences=evidences,
                    )
                )
        return detections
