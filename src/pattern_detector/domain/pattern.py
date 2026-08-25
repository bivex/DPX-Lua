"""Comprehensive pattern catalog and metadata for Lua & Luau static analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pattern_detector.domain.value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternDefinition:
    """Detailed architectural specification of a Lua / Luau pattern or hazard."""

    type: PatternType
    category: PatternCategory
    name: str
    description: str
    lua_version: str = "Lua 5.1 - 5.4 / LuaJIT / Luau"
    recommendation: str = ""


PATTERN_CATALOG: dict[PatternType, PatternDefinition] = {
    # 1. Lua & Luau Idiomatic & Metatable OOP
    PatternType.METATABLE_PROTOTYPE_OOP: PatternDefinition(
        type=PatternType.METATABLE_PROTOTYPE_OOP,
        category=PatternCategory.LUA_IDIOMATIC_METATABLE,
        name="Metatable Prototype OOP",
        description="Prototype-based class inheritance via setmetatable(self, { __index = Class }) and constructor methods.",
        recommendation="Use setmetatable with __index to construct lightweight, reusable object prototypes.",
    ),
    PatternType.OPERATOR_OVERLOADING_METAMETHODS: PatternDefinition(
        type=PatternType.OPERATOR_OVERLOADING_METAMETHODS,
        category=PatternCategory.LUA_IDIOMATIC_METATABLE,
        name="Operator Overloading Metamethods",
        description="Overloading arithmetic and structural operators via __add, __sub, __mul, __tostring, __call metamethods.",
        recommendation="Implement __tostring and comparison metamethods for domain value objects.",
    ),
    PatternType.CLOSURE_MODULE_ENCAPSULATION: PatternDefinition(
        type=PatternType.CLOSURE_MODULE_ENCAPSULATION,
        category=PatternCategory.LUA_IDIOMATIC_METATABLE,
        name="Closure Module Encapsulation",
        description="Encapsulating module state in private upvalues (local variables) returned as public API table.",
        recommendation="Prefer local module tables (local M = {}) to avoid polluting the global table _G.",
    ),
    PatternType.COROUTINE_COOPERATIVE_TASK: PatternDefinition(
        type=PatternType.COROUTINE_COOPERATIVE_TASK,
        category=PatternCategory.LUA_IDIOMATIC_METATABLE,
        name="Coroutine Cooperative Task Scheduler",
        description="Cooperative multitasking and frame yield suspension using coroutine.create, resume, and yield.",
        recommendation="Use coroutines for frame-based game loops, cutscenes, and asynchronous promise chains.",
    ),
    PatternType.LUAU_STATIC_TYPE_ANNOTATION: PatternDefinition(
        type=PatternType.LUAU_STATIC_TYPE_ANNOTATION,
        category=PatternCategory.LUA_IDIOMATIC_METATABLE,
        name="Luau Gradual Static Type Annotation",
        description="Gradual static typing using Luau syntax ('type Vector = { x: number, y: number }', 'export type').",
        recommendation="Add Luau type annotations to public API module boundaries for IDE autocompletion and compile-time safety.",
    ),
    PatternType.PCALL_XPCALL_RAILWAY_ERROR: PatternDefinition(
        type=PatternType.PCALL_XPCALL_RAILWAY_ERROR,
        category=PatternCategory.LUA_IDIOMATIC_METATABLE,
        name="Protected Call Railway Error Handling",
        description="Safely capturing runtime errors using pcall(fn, ...) or xpcall(fn, error_handler) without crashing game loops.",
        recommendation="Wrap external I/O, network requests, and user script plugins in pcall/xpcall.",
    ),

    # 2. GameDev, Roblox & Neovim Extension Architectures
    PatternType.ROBLOX_INSTANCE_REPLICATION_BRIDGE: PatternDefinition(
        type=PatternType.ROBLOX_INSTANCE_REPLICATION_BRIDGE,
        category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
        name="Roblox Instance Replication Bridge",
        description="Roblox Client/Server network boundary communication using RemoteEvent, RemoteFunction, and Instance.new.",
        recommendation="Sanitize all incoming RemoteEvent payload parameters on the server side.",
    ),
    PatternType.ECS_COMPONENT_TABLE_LAYOUT: PatternDefinition(
        type=PatternType.ECS_COMPONENT_TABLE_LAYOUT,
        category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
        name="Entity Component System (ECS) Table Layout",
        description="Data-oriented game architecture separating entities (IDs), components (data tables), and systems (iteration loops).",
        recommendation="Use contiguous arrays for component storage to maximize CPU cache locality in game loops.",
    ),
    PatternType.NEOVIM_PLUGIN_API_FACADE: PatternDefinition(
        type=PatternType.NEOVIM_PLUGIN_API_FACADE,
        category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
        name="Neovim Plugin API Facade",
        description="Lua extensions integrating with Neovim C-API via vim.api, vim.keymap, and vim.lsp facades.",
        recommendation="Structure Neovim plugins as clean Lua modules under lua/plugin_name/ with setup() entrypoint.",
    ),
    PatternType.EVENT_SIGNAL_LISTENER_BUS: PatternDefinition(
        type=PatternType.EVENT_SIGNAL_LISTENER_BUS,
        category=PatternCategory.GAMEDEV_ROBLOX_NEOVIM,
        name="Event Signal Listener Bus",
        description="Custom Signal/Event dispatcher pattern implementing :Connect(fn) and :Fire(...).",
        recommendation="Provide disconnect handles to prevent memory leaks in event listeners.",
    ),

    # 3. LuaJIT FFI & Systems Performance
    PatternType.LUAJIT_FFI_C_BINDING: PatternDefinition(
        type=PatternType.LUAJIT_FFI_C_BINDING,
        category=PatternCategory.LUAJIT_FFI_SYSTEMS,
        name="LuaJIT FFI Direct C Binding",
        description="High-performance direct C ABI calling and struct manipulation via ffi.cdef and ffi.load.",
        recommendation="Use LuaJIT FFI for native performance in audio DSP, physics engines, and graphics bindings.",
    ),
    PatternType.TABLE_PREALLOCATION_CACHE: PatternDefinition(
        type=PatternType.TABLE_PREALLOCATION_CACHE,
        category=PatternCategory.LUAJIT_FFI_SYSTEMS,
        name="Table Preallocation & Pooling Cache",
        description="Pre-allocating table capacity (table.create(N)) and object pools to prevent GC churn and hash rehashing.",
        recommendation="Pre-allocate table capacity for large collections to avoid hash resize overhead.",
    ),
    PatternType.PACKED_BITFIELD_MANIPULATION: PatternDefinition(
        type=PatternType.PACKED_BITFIELD_MANIPULATION,
        category=PatternCategory.LUAJIT_FFI_SYSTEMS,
        name="Packed Bitfield Manipulation",
        description="Manipulating bit flags and bitfields using bit/bit32 libraries (bit.band, bit.bor, bit.lshift).",
        recommendation="Use bitwise operations for compact game state flags and network serialization.",
    ),

    # 4. Creational Patterns (5/5)
    PatternType.SINGLETON_MODULE_CACHE: PatternDefinition(
        type=PatternType.SINGLETON_MODULE_CACHE,
        category=PatternCategory.CREATIONAL,
        name="Singleton Module Cache",
        description="Singleton pattern leveraging require() caching in package.loaded table.",
        recommendation="Export a single stateful table from require() modules to enforce singleton lifecycle.",
    ),
    PatternType.FACTORY_CONSTRUCTOR_METHOD: PatternDefinition(
        type=PatternType.FACTORY_CONSTRUCTOR_METHOD,
        category=PatternCategory.CREATIONAL,
        name="Factory Constructor Method",
        description="Factory pattern instantiating configured objects via Class:new(...) or create_object(...).",
        recommendation="Encapsulate metatable initialization inside Class.new() factory constructors.",
    ),
    PatternType.ABSTRACT_FACTORY_THEME_PROVIDER: PatternDefinition(
        type=PatternType.ABSTRACT_FACTORY_THEME_PROVIDER,
        category=PatternCategory.CREATIONAL,
        name="Abstract Factory Theme Provider",
        description="Abstract factory producing families of related UI widgets or game entity models.",
        recommendation="Parameterize UI widget construction with abstract theme provider factories.",
    ),
    PatternType.BUILDER_FLUENT_TABLE_CONFIG: PatternDefinition(
        type=PatternType.BUILDER_FLUENT_TABLE_CONFIG,
        category=PatternCategory.CREATIONAL,
        name="Builder Fluent Table Config",
        description="Fluent method chaining pattern mutating internal configuration and returning self.",
        recommendation="Implement builder chaining for complex game entity or UI tree configuration.",
    ),
    PatternType.PROTOTYPE_DEEP_CLONE_TABLE: PatternDefinition(
        type=PatternType.PROTOTYPE_DEEP_CLONE_TABLE,
        category=PatternCategory.CREATIONAL,
        name="Prototype Deep Clone Table",
        description="Prototype pattern cloning tables and nested metatables for new instances.",
        recommendation="Use recursive table clone functions to instantiate distinct object trees.",
    ),

    # 5. Structural Patterns (7/7)
    PatternType.ADAPTER_METATABLE_WRAPPER: PatternDefinition(
        type=PatternType.ADAPTER_METATABLE_WRAPPER,
        category=PatternCategory.STRUCTURAL,
        name="Adapter Metatable Wrapper",
        description="Adapter pattern wrapping foreign tables and redirecting lookups via __index metamethod.",
        recommendation="Use __index forwarding to adapt legacy table APIs to new interfaces.",
    ),
    PatternType.BRIDGE_DRIVER_RENDERER: PatternDefinition(
        type=PatternType.BRIDGE_DRIVER_RENDERER,
        category=PatternCategory.STRUCTURAL,
        name="Bridge Driver Renderer",
        description="Decoupling game logic from platform graphics/physics drivers (Love2D, Defold, Raylib).",
        recommendation="Abstract rendering behind a driver table interface to support multiple game engines.",
    ),
    PatternType.COMPOSITE_SCENE_GRAPH_NODE: PatternDefinition(
        type=PatternType.COMPOSITE_SCENE_GRAPH_NODE,
        category=PatternCategory.STRUCTURAL,
        name="Composite Scene Graph Node",
        description="Hierarchical tree nodes containing parent and children tables in scene graphs.",
        recommendation="Use composite parent/children table structures for 2D/3D scene graph hierarchies.",
    ),
    PatternType.DECORATOR_FUNCTION_WRAPPER: PatternDefinition(
        type=PatternType.DECORATOR_FUNCTION_WRAPPER,
        category=PatternCategory.STRUCTURAL,
        name="Decorator Function Wrapper",
        description="Higher-order functions wrapping target functions with caching, logging, or profiling.",
        recommendation="Use function decorators for memoization, performance profiling, and error logging.",
    ),
    PatternType.FACADE_INIT_MODULE_API: PatternDefinition(
        type=PatternType.FACADE_INIT_MODULE_API,
        category=PatternCategory.STRUCTURAL,
        name="Facade Init Module API",
        description="Top-level init.lua exposing a unified, cohesive public API over internal submodules.",
        recommendation="Expose clean high-level module functions in init.lua while keeping submodules internal.",
    ),
    PatternType.FLYWEIGHT_SHARED_META_TABLE: PatternDefinition(
        type=PatternType.FLYWEIGHT_SHARED_META_TABLE,
        category=PatternCategory.STRUCTURAL,
        name="Flyweight Shared Metatable",
        description="Sharing a single immutable metatable across millions of lightweight instance tables.",
        recommendation="Share a single __index metatable definition across particle/entity instances to minimize memory.",
    ),
    PatternType.PROXY_LAZY_TABLE_INDEXER: PatternDefinition(
        type=PatternType.PROXY_LAZY_TABLE_INDEXER,
        category=PatternCategory.STRUCTURAL,
        name="Proxy Lazy Table Indexer",
        description="Proxy pattern intercepting property reads and writes using __index and __newindex metamethods.",
        recommendation="Use metatable proxies for lazy module loading and reactive state observation.",
    ),

    # 6. Behavioral Patterns (11/11)
    PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE: PatternDefinition(
        type=PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE,
        category=PatternCategory.BEHAVIORAL,
        name="Chain of Responsibility Middleware",
        description="Chained handler functions passing requests along a pipeline.",
        recommendation="Use chained handler functions for input processing pipelines and HTTP middleware.",
    ),
    PatternType.COMMAND_UNDO_REDO_PAYLOAD: PatternDefinition(
        type=PatternType.COMMAND_UNDO_REDO_PAYLOAD,
        category=PatternCategory.BEHAVIORAL,
        name="Command Action Payload (Undo/Redo)",
        description="Encapsulating actions as tables holding execute() and undo() functions for command history.",
        recommendation="Model level editor actions and player moves as undoable Command tables.",
    ),
    PatternType.INTERPRETER_DSL_EVALUATOR: PatternDefinition(
        type=PatternType.INTERPRETER_DSL_EVALUATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Interpreter Table DSL Evaluator",
        description="Evaluating table-based ASTs or mini-language domain expressions.",
        recommendation="Use table-based DSL interpreters for dialogue trees and quest rule systems.",
    ),
    PatternType.ITERATOR_STATELESS_PAIRS_IPAIRS: PatternDefinition(
        type=PatternType.ITERATOR_STATELESS_PAIRS_IPAIRS,
        category=PatternCategory.BEHAVIORAL,
        name="Custom Stateless / Stateful Iterator",
        description="Custom iterator functions conforming to Lua's generic for-loop protocol (iterator, state, var).",
        recommendation="Implement stateless iterator functions (next_item, state, initial) to eliminate closure allocation overhead.",
    ),
    PatternType.MEDIATOR_GAME_EVENT_COORDINATOR: PatternDefinition(
        type=PatternType.MEDIATOR_GAME_EVENT_COORDINATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Mediator Game Event Coordinator",
        description="Central mediator table coordinating communication between decoupled game subsystems.",
        recommendation="Decouple player state, audio playback, and HUD UI via a central event mediator.",
    ),
    PatternType.MEMENTO_TABLE_SNAPSHOT: PatternDefinition(
        type=PatternType.MEMENTO_TABLE_SNAPSHOT,
        category=PatternCategory.BEHAVIORAL,
        name="Memento State Snapshot",
        description="Capturing and restoring state snapshots for savestates, rollback netcode, and checkpoints.",
        recommendation="Capture immutable state snapshots for deterministic rollback netcode and game saves.",
    ),
    PatternType.OBSERVER_SIGNAL_LISTENER: PatternDefinition(
        type=PatternType.OBSERVER_SIGNAL_LISTENER,
        category=PatternCategory.BEHAVIORAL,
        name="Observer Signal Listener",
        description="Observer pattern dispatching events to a list of registered listener callbacks.",
        recommendation="Use signal broadcaster tables to notify decoupled systems of game state changes.",
    ),
    PatternType.STATE_MACHINE_TABLE_FSM: PatternDefinition(
        type=PatternType.STATE_MACHINE_TABLE_FSM,
        category=PatternCategory.BEHAVIORAL,
        name="State Machine Table FSM",
        description="Finite State Machine managing states via tables of enter(), update(), and exit() hooks.",
        recommendation="Model AI behaviors and game screens using structured state machine tables.",
    ),
    PatternType.STRATEGY_TABLE_FUNCTION_INJECTION: PatternDefinition(
        type=PatternType.STRATEGY_TABLE_FUNCTION_INJECTION,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Table Function Injection",
        description="Injecting interchangeable algorithm closures or strategy tables into components.",
        recommendation="Pass strategy functions for sorting, AI pathfinding, and weapon firing behaviors.",
    ),
    PatternType.TEMPLATE_METHOD_HOOK_LIFECYCLE: PatternDefinition(
        type=PatternType.TEMPLATE_METHOD_HOOK_LIFECYCLE,
        category=PatternCategory.BEHAVIORAL,
        name="Template Method Lifecycle Hooks",
        description="Base class method coordinating execution sequence with optional hook overrides (init, update, draw).",
        recommendation="Define lifecycle template methods coordinating update and draw steps across game entities.",
    ),
    PatternType.VISITOR_SCENE_WALKER: PatternDefinition(
        type=PatternType.VISITOR_SCENE_WALKER,
        category=PatternCategory.BEHAVIORAL,
        name="Visitor Scene Walker",
        description="Visitor pattern traversing nested table hierarchies and executing callbacks per node type.",
        recommendation="Use visitor walkers for scene graph rendering and entity spatial partitioning.",
    ),

    # 7. Hazards & Performance Traps
    PatternType.GLOBAL_VARIABLE_LEAK_HAZARD: PatternDefinition(
        type=PatternType.GLOBAL_VARIABLE_LEAK_HAZARD,
        category=PatternCategory.HAZARDS_MEMORY_LEAK,
        name="Global Variable Leak Hazard",
        description="Unintentional global variable assignment omitting the 'local' keyword, polluting _G.",
        recommendation="Always declare variables with 'local' to prevent global scope contamination and GC leaks.",
    ),
    PatternType.TABLE_REHASH_LOOP_HAZARD: PatternDefinition(
        type=PatternType.TABLE_REHASH_LOOP_HAZARD,
        category=PatternCategory.HAZARDS_MEMORY_LEAK,
        name="Table Rehash Inside Hot Loop Hazard",
        description="Dynamically expanding table size inside tight loops causing repetitive allocation and rehashing.",
        recommendation="Pre-allocate table size (table.create) or reuse object pools inside hot loops.",
    ),
    PatternType.NIL_INDEXING_METATABLE_HAZARD: PatternDefinition(
        type=PatternType.NIL_INDEXING_METATABLE_HAZARD,
        category=PatternCategory.HAZARDS_MEMORY_LEAK,
        name="Nil Indexing Metatable Hazard",
        description="Chained field dereferencing without nil guards, risking 'attempt to index a nil value' crashes.",
        recommendation="Add nil checks or use safe navigation helper functions before deep indexing.",
    ),
    PatternType.COROUTINE_UNHANDLED_DEADLOCK_HAZARD: PatternDefinition(
        type=PatternType.COROUTINE_UNHANDLED_DEADLOCK_HAZARD,
        category=PatternCategory.HAZARDS_MEMORY_LEAK,
        name="Coroutine Unhandled Deadlock Hazard",
        description="Coroutine yielding indefinitely without a resume keeper or timeout mechanism.",
        recommendation="Ensure all yielded coroutines have scheduled resume callbacks or timeout handlers.",
    ),

    # 8. SOLID Principles & Smells
    PatternType.MONOLITHIC_MODULE_SRP: PatternDefinition(
        type=PatternType.MONOLITHIC_MODULE_SRP,
        category=PatternCategory.PRINCIPLE,
        name="Monolithic Module SRP Violation",
        description="Module table declaring excessive functions (>= 15), violating Single Responsibility Principle.",
        recommendation="Decompose large modules into cohesive sub-modules.",
    ),
    PatternType.FAT_METATABLE_INTERFACE_ISP: PatternDefinition(
        type=PatternType.FAT_METATABLE_INTERFACE_ISP,
        category=PatternCategory.PRINCIPLE,
        name="Fat Metatable Interface ISP Violation",
        description="Class metatable defining excessive methods (>= 12), violating Interface Segregation.",
        recommendation="Split fat metatables into focused mixins or component traits.",
    ),
    PatternType.DEEP_TABLE_NESTING_DEMETER: PatternDefinition(
        type=PatternType.DEEP_TABLE_NESTING_DEMETER,
        category=PatternCategory.PRINCIPLE,
        name="Deep Table Nesting Demeter Violation",
        description="Deep chained property indexing (>= 4 levels e.g. a.b.c.d.e), violating Law of Demeter.",
        recommendation="Encapsulate nested access within helper methods on intermediate tables.",
    ),
}
