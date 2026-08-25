"""Value objects, Enums, and domain primitives for Lua & Luau static analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PatternCategory(str, Enum):
    """Broad architectural classification for Lua/Luau patterns and findings."""

    LUA_IDIOMATIC_METATABLE = "lua_idiomatic_metatable"
    GAMEDEV_ROBLOX_NEOVIM = "gamedev_roblox_neovim"
    LUAJIT_FFI_SYSTEMS = "luajit_ffi_systems"
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    HAZARDS_MEMORY_LEAK = "hazards_memory_leak"
    PRINCIPLE = "principle"


class PatternType(str, Enum):
    """Exhaustive catalog of Lua/Luau patterns, metatables, gamedev architectures, and hazards."""

    # 1. Lua & Luau Idiomatic & Metatable OOP (6)
    METATABLE_PROTOTYPE_OOP = "metatable_prototype_oop"
    OPERATOR_OVERLOADING_METAMETHODS = "operator_overloading_metamethods"
    CLOSURE_MODULE_ENCAPSULATION = "closure_module_encapsulation"
    COROUTINE_COOPERATIVE_TASK = "coroutine_cooperative_task"
    LUAU_STATIC_TYPE_ANNOTATION = "luau_static_type_annotation"
    PCALL_XPCALL_RAILWAY_ERROR = "pcall_xpcall_railway_error"

    # 2. GameDev, Roblox & Neovim Extension Architectures (4)
    ROBLOX_INSTANCE_REPLICATION_BRIDGE = "roblox_instance_replication_bridge"
    ECS_COMPONENT_TABLE_LAYOUT = "ecs_component_table_layout"
    NEOVIM_PLUGIN_API_FACADE = "neovim_plugin_api_facade"
    EVENT_SIGNAL_LISTENER_BUS = "event_signal_listener_bus"

    # 3. LuaJIT FFI & Systems Performance (3)
    LUAJIT_FFI_C_BINDING = "luajit_ffi_c_binding"
    TABLE_PREALLOCATION_CACHE = "table_preallocation_cache"
    PACKED_BITFIELD_MANIPULATION = "packed_bitfield_manipulation"

    # 4. Creational Patterns (5/5)
    SINGLETON_MODULE_CACHE = "singleton_module_cache"
    FACTORY_CONSTRUCTOR_METHOD = "factory_constructor_method"
    ABSTRACT_FACTORY_THEME_PROVIDER = "abstract_factory_theme_provider"
    BUILDER_FLUENT_TABLE_CONFIG = "builder_fluent_table_config"
    PROTOTYPE_DEEP_CLONE_TABLE = "prototype_deep_clone_table"

    # 5. Structural Patterns (7/7)
    ADAPTER_METATABLE_WRAPPER = "adapter_metatable_wrapper"
    BRIDGE_DRIVER_RENDERER = "bridge_driver_renderer"
    COMPOSITE_SCENE_GRAPH_NODE = "composite_scene_graph_node"
    DECORATOR_FUNCTION_WRAPPER = "decorator_function_wrapper"
    FACADE_INIT_MODULE_API = "facade_init_module_api"
    FLYWEIGHT_SHARED_META_TABLE = "flyweight_shared_meta_table"
    PROXY_LAZY_TABLE_INDEXER = "proxy_lazy_table_indexer"

    # 6. Behavioral Patterns (11/11)
    CHAIN_OF_RESPONSIBILITY_MIDDLEWARE = "chain_of_responsibility_middleware"
    COMMAND_UNDO_REDO_PAYLOAD = "command_undo_redo_payload"
    INTERPRETER_DSL_EVALUATOR = "interpreter_dsl_evaluator"
    ITERATOR_STATELESS_PAIRS_IPAIRS = "iterator_stateless_pairs_ipairs"
    MEDIATOR_GAME_EVENT_COORDINATOR = "mediator_game_event_coordinator"
    MEMENTO_TABLE_SNAPSHOT = "memento_table_snapshot"
    OBSERVER_SIGNAL_LISTENER = "observer_signal_listener"
    STATE_MACHINE_TABLE_FSM = "state_machine_table_fsm"
    STRATEGY_TABLE_FUNCTION_INJECTION = "strategy_table_function_injection"
    TEMPLATE_METHOD_HOOK_LIFECYCLE = "template_method_hook_lifecycle"
    VISITOR_SCENE_WALKER = "visitor_scene_walker"

    # 7. Hazards & Performance Traps (4)
    GLOBAL_VARIABLE_LEAK_HAZARD = "global_variable_leak_hazard"
    TABLE_REHASH_LOOP_HAZARD = "table_rehash_loop_hazard"
    NIL_INDEXING_METATABLE_HAZARD = "nil_indexing_metatable_hazard"
    COROUTINE_UNHANDLED_DEADLOCK_HAZARD = "coroutine_unhandled_deadlock_hazard"

    # 8. SOLID Principles & Smells (3)
    MONOLITHIC_MODULE_SRP = "monolithic_module_srp"
    FAT_METATABLE_INTERFACE_ISP = "fat_metatable_interface_isp"
    DEEP_TABLE_NESTING_DEMETER = "deep_table_nesting_demeter"


class ConfidenceLevel(str, Enum):
    """Categorical confidence level ranking."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass(frozen=True)
class SourceLocation:
    """Precise source code location in a Lua file (.lua, .luau)."""

    file_path: str
    line: int
    column: int = 1

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column}"


@dataclass
class Evidence:
    """Individual heuristic or signal contributing to pattern detection."""

    rule_code: str
    description: str
    weight: float
    location: SourceLocation | None = None


@dataclass
class Confidence:
    """Aggregated detection confidence score and heuristic evidence trail."""

    score: float
    evidences: list[Evidence] = field(default_factory=list)

    @property
    def level(self) -> ConfidenceLevel:
        if self.score >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        if self.score >= 0.70:
            return ConfidenceLevel.HIGH
        if self.score >= 0.50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    @property
    def percentage_str(self) -> str:
        return f"{int(round(self.score * 100))}%"
