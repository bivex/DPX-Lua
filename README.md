# 🌙 DPX-Lua: Metatables, Coroutines, LuaJIT FFI, GameDev (Roblox/Neovim) & GoF 23 Static Analyzer

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Lua Version](https://img.shields.io/badge/Lua-5.1%20--%205.4%20%7C%20LuaJIT%20%7C%20Luau-000080?logo=lua&logoColor=white)](https://lua.org)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-blueviolet)](https://alistair.cockburn.us/hexagonal-architecture/)
[![CLI: Typer & Rich](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-009688)](https://typer.tiangolo.com)
[![SARIF OASIS v2.1.0](https://img.shields.io/badge/SARIF-OASIS%20v2.1.0-blue)](https://sarifweb.azurewebsites.net)

**DPX-Lua** is an enterprise-grade static analysis engine and architectural pattern detector for Lua, Luau, and LuaJIT codebases. Engineered for **Game Development (Roblox, Love2D, Defold, Solar2D), Neovim Plugins, High-Performance Systems (LuaJIT FFI, OpenResty/Nginx), and Embedded Scripting**, it audits **Metatable Prototype OOP (`__index`), Operator Overloading Metamethods (`__add`, `__tostring`, `__call`), Closure Encapsulation, Coroutine Task Schedulers, Luau Gradual Static Typing, Roblox Remote Networking (`RemoteEvent`), Neovim API Facades (`vim.api`), LuaJIT C-FFI (`ffi.cdef`), all 23 GoF Design Patterns**, and **Lua Memory Hazards (Global Variable Leaks, Unpreallocated Table Rehashing, Nil Index Crashes, Coroutine Deadlocks)**.

[Features](#-key-features) • [Installation](#-installation) • [CLI Usage](#-cli-usage) • [Supported Rules](#-supported-pattern-rules--checks) • [The DPX Suite Family](#-the-dpx-suite-family)

</div>

---

## 🌟 Key Features

- ⚙️ **Metatable Prototype OOP & Metamethods:** Audits class prototyping via `setmetatable(self, Class)` and operator overloading (`__index`, `__newindex`, `__tostring`, `__call`, `__add`).
- 🎮 **GameDev & Engine Architectures:** Recognizes Roblox Client/Server networking (`RemoteEvent`, `Instance.new`), Entity Component Systems (ECS), custom Signal event buses, and Neovim editor plugins (`vim.api`, `vim.keymap`).
- ⚡ **LuaJIT FFI & Systems Performance:** Inspects direct C ABI bindings (`ffi.cdef`), table capacity pre-allocations (`table.create(N)`), and bitwise flags (`bit32`).
- 🔄 **Coroutine Schedulers & Cooperative Multitasking:** Detects game loop frame yields and async promise chains with `coroutine.create`, `coroutine.resume`, `coroutine.yield`.
- 🏛️ **100% Complete Gang of Four (GoF 23/23):** Full coverage of all 23 Creational, Structural, and Behavioral patterns tailored for Lua table prototypes, closures, and metamethods.
- 🚨 **Hazards & Memory Leaks:** Flags unintentional global leaks (omitting `local`), table rehashing inside hot loops, chained nil indexing crashes, and deadlocked coroutines.
- 📊 **Interactive Architecture Observability HUD:** Zero-dependency interactive HTML dashboard with instant search, KPI breakdown, and built-in **`🤖 Copy AI Context Prompt`** generator for LLMs (Claude, GPT-4, Gemini).
- 🔒 **CI/CD & GitHub Security Ready:** Standardized **OASIS SARIF v2.1.0**, JSON, and Markdown reports.

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/bivex/DPX-Lua.git
cd DPX-Lua

# Install dependencies using uv or pip
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

---

## 💻 CLI Usage

### 1. Scan a Lua / Luau Codebase
```bash
# Terminal scan with Rich formatting
dpx-lua scan /path/to/lua/project

# Export Interactive HTML Observability HUD
dpx-lua scan src/ -H reports/lua_hud.html

# Generate AI Context Prompt for LLMs
dpx-lua scan src/ --llm

# Filter for specific Metatable or Coroutine rules
dpx-lua scan src/ -p metatable_prototype_oop -p coroutine_cooperative_task

# Export SARIF for GitHub Code Scanning
dpx-lua scan src/ -S reports/results.sarif
```

### 2. Inspect Supported Architectural Rules
```bash
dpx-lua rules
```

### 3. Query Deep Pattern Documentation
```bash
dpx-lua info metatable_prototype_oop
dpx-lua info roblox_instance_replication_bridge
```

---

## 📋 Supported Pattern Rules & Checks

### 1. ⚙️ Lua & Luau Idiomatic & Metatable OOP
- `metatable_prototype_oop`: Prototype-based class inheritance via `setmetatable(self, { __index = Class })`.
- `operator_overloading_metamethods`: Operator overloading via `__add`, `__sub`, `__mul`, `__tostring`, `__call`.
- `closure_module_encapsulation`: Encapsulating module state in private upvalues returning a public API table (`local M = {}`).
- `coroutine_cooperative_task`: Cooperative multitasking via `coroutine.create`, `coroutine.resume`, and `coroutine.yield`.
- `luau_static_type_annotation`: Gradual static typing using Luau syntax (`type Vector = { x: number, y: number }`).
- `pcall_xpcall_railway_error`: Safe error handling using `pcall(fn, ...)` or `xpcall(fn, err_handler)`.

### 2. 🎮 GameDev, Roblox & Neovim Extension Architectures
- `roblox_instance_replication_bridge`: Roblox Client/Server networking (`RemoteEvent`, `Instance.new`).
- `ecs_component_table_layout`: Entity Component System data-oriented tables (`components[entity_id]`).
- `neovim_plugin_api_facade`: Neovim Lua plugin architecture integrating with `vim.api` and `vim.keymap`.
- `event_signal_listener_bus`: Custom Signal/Event dispatcher implementing `:Connect(fn)` and `:Fire(...)`.

### 3. ⚡ LuaJIT FFI & Systems Performance
- `luajit_ffi_c_binding`: High-performance direct C ABI calling and struct manipulation via `ffi.cdef`.
- `table_preallocation_cache`: Pre-allocating table capacity (`table.create(N)`) to eliminate hash table rehashing.
- `packed_bitfield_manipulation`: Bitwise flag manipulation via `bit`/`bit32` libraries.

### 4. 🏛️ GoF Creational Patterns (5/5)
- `singleton_module_cache`: Singleton pattern leveraging `require()` caching in `package.loaded`.
- `factory_constructor_method`: Factory pattern instantiating objects via `Class:new(...)` or `create_entity(...)`.
- `abstract_factory_theme_provider`: Abstract factory creating families of related UI widgets or game entity models.
- `builder_fluent_table_config`: Fluent method chaining pattern mutating configuration and returning `self`.
- `prototype_deep_clone_table`: Prototype pattern cloning tables and nested metatables for new instances.

### 5. 🧱 GoF Structural Patterns (7/7)
- `adapter_metatable_wrapper`: Adapter pattern wrapping foreign tables via `__index` lookup forwarding.
- `bridge_driver_renderer`: Decoupling game logic from platform graphics/physics drivers (Love2D, Defold, Raylib).
- `composite_scene_graph_node`: Tree hierarchy of parent/children tables in 2D/3D scene graphs.
- `decorator_function_wrapper`: Higher-order functions wrapping target functions with caching, logging, or profiling.
- `facade_init_module_api`: Top-level `init.lua` exposing a unified, cohesive public API over internal submodules.
- `flyweight_shared_meta_table`: Sharing a single immutable metatable across millions of lightweight instance tables.
- `proxy_lazy_table_indexer`: Proxy pattern intercepting reads and writes using `__index` and `__newindex`.

### 6. 🎯 GoF Behavioral Patterns (11/11)
- `chain_of_responsibility_middleware`: Chained handler functions passing requests along a pipeline.
- `command_undo_redo_payload`: Encapsulating actions as tables holding `execute()` and `undo()` functions.
- `interpreter_dsl_evaluator`: Evaluating table-based ASTs or mini-language domain expressions.
- `iterator_stateless_pairs_ipairs`: Custom stateless / stateful iterator functions (generic for-loop protocol).
- `mediator_game_event_coordinator`: Central mediator table coordinating communication across game subsystems.
- `memento_table_snapshot`: Capturing and restoring state snapshots for savestates and checkpoints.
- `observer_signal_listener`: Observer pattern dispatching notifications to subscriber callbacks.
- `state_machine_table_fsm`: Finite State Machine managing states via tables of `enter()`, `update()`, `exit()` hooks.
- `strategy_table_function_injection`: Injecting interchangeable algorithm closures or strategy tables into components.
- `template_method_hook_lifecycle`: Base class lifecycle coordinating execution with optional hook overrides.
- `visitor_scene_walker`: Visitor pattern traversing nested table hierarchies with node callbacks.

### 7. 🛡️ Hazards & Memory Leaks
- `global_variable_leak_hazard`: Unintentional global assignment omitting the `local` keyword, polluting `_G`.
- `table_rehash_loop_hazard`: Dynamically expanding table size inside tight loops causing rehashing.
- `nil_indexing_metatable_hazard`: Chained field dereferencing without nil guards, risking nil index crashes.
- `coroutine_unhandled_deadlock_hazard`: Coroutine yielding indefinitely without a resume keeper.

### 8. 📐 SOLID Principles & Smells
- `monolithic_module_srp`: Module table declaring excessive functions (>= 15), violating Single Responsibility.
- `fat_metatable_interface_isp`: Class metatable defining excessive methods (>= 12), violating Interface Segregation.
- `deep_table_nesting_demeter`: Deep chained property indexing (>= 4 levels), violating Law of Demeter.

---

## 🌐 The DPX Suite Family

Cross-language architectural static analysis across all modern programming languages:

| Repository | Language / Ecosystem | Primary Paradigms & Focus |
|---|---|---|
| **[`DPX-Huff`](https://github.com/bivex/DPX-Huff)** | **Huff / EVM Stack Assembly** (0.3.x+ / Cancun) | **Macros, Stack Layout, Jumpdest Labels, Selector Dispatchers, GoF 23** |
| **[`DPX-Yul`](https://github.com/bivex/DPX-Yul)** | **Yul / EVM Assembly** (0.8.x - 0.8.28+ / Cancun) | **Memory Management, Storage Packing, Transient Storage (EIP-1153), GoF 23** |
| **[`DPX-Cairo`](https://github.com/bivex/DPX-Cairo)** | **Cairo** (Cairo 1.0 - 2.8+ / Starknet) | **Components, Storage Mapping, Syscalls, Account Abstraction, Upgrades, GoF 23** |
| **[`DPX-Move`](https://github.com/bivex/DPX-Move)** | **Move** (Move 2024 / Aptos / Sui) | **Linear Resources, Abilities, Sui Objects, Hot Potato, Prover, GoF 23** |
| **[`DPX-Lua`](https://github.com/bivex/DPX-Lua)** | **Lua / Luau** (5.1 - 5.4 / LuaJIT) | **Metatable OOP, Coroutines, LuaJIT FFI, GameDev (Roblox/Neovim), GoF 23** |
| **[`DPX-Solidity`](https://github.com/bivex/DPX-Solidity)** | **Solidity** (0.8.x - 0.8.28+) | **EVM Gas Optimization, Proxies, CEI Reentrancy, Yul, GoF 23, Security** |
| **[`DPX-Zig`](https://github.com/bivex/DPX-Zig)** | **Zig** (0.11 - 0.14+) | **Comptime Generics, Allocator RAII, Defer Cleanup, SIMD, GoF 23** |
| **[`DPX-Gleam`](https://github.com/bivex/DPX-Gleam)** | **Gleam** (1.0 - 1.8+) | **Type-Safe OTP Actors, Algebraic Data Types, Railway Monads, GoF 23** |
| **[`DPX-Mojo`](https://github.com/bivex/DPX-Mojo)** | **Mojo** (24.x - 25.x+) | **SIMD Vectorization, Ownership, Memory Safety, GoF 23, AI Acceleration** |
| **[`DPX-Julia`](https://github.com/bivex/DPX-Julia)** | **Julia** (1.6 - 1.11+) | **Multiple Dispatch, Holy Traits, Metaprogramming, Tasks, GoF 23** |
| **[`DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin)** | **Kotlin** (1.8 - 2.0+) | **Coroutines, Flow, Jetpack Compose, Multiplatform, GoF 23** |
| **[`DPX-Swift`](https://github.com/bivex/DPX-Swift)** | **Swift** (5.5 - 6.0+) | **Protocol-Oriented, Actor Concurrency, SwiftUI, ARC Safety** |
| **[`DPX-CSharp`](https://github.com/bivex/DPX-CSharp)** | **C#** (10 - 13 / .NET 8-9) | **Clean Architecture, CQRS MediatR, Channel Pipelines** |
| **[`DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript)** | **TypeScript / JavaScript** | **Hexagonal DI, Decorator Meta, Reactive Streams, React/NestJS** |
| **[`DPX-Rust`](https://github.com/bivex/DPX-Rust)** | **Rust** (Edition 2021/2024) | **Zero-Cost Abstractions, RAII Lifetimes, Typestate Pattern** |
| **[`DPX-Go`](https://github.com/bivex/DPX-Go)** | **Go** (1.18 - 1.24+) | **Goroutine Channels, CSP Concurrency, Pipeline Streaming** |
| **[`DPX-Py`](https://github.com/bivex/DPX-Py)** | **Python** (3.8 - 3.13+) | **Multi-Paradigm Hexagonal, Data Flow Engine, AsyncIO** |
| **[`DPX-Php`](https://github.com/bivex/DPX-Php)** | **PHP** (8.1 - 8.4+) | **Attribute-driven DDD, Fiber Concurrency, Laravel/Symfony** |
| **[`DPX-Haskell`](https://github.com/bivex/DPX-Haskell)** | **Haskell** (GHC 9.2 - 9.12+) | **Category Theory, Monad Transformers, Free Monads, Optics** |
| **[`DPX-OCaml`](https://github.com/bivex/DPX-OCaml)** | **OCaml** (4.14 - 5.3+ Multicore) | **Functor Modules, Effect Handlers, GADTs, Railway Monads** |
| **[`DPX-Elixir`](https://github.com/bivex/DPX-Elixir)** | **Elixir** (OTP 25 - 27+) | **GenServer, DynamicSupervisor, Actor Fault Tolerance** |
| **[`DPX-Erlang`](https://github.com/bivex/DPX-Erlang)** | **Erlang/OTP** (24 - 27+) | **OTP Behaviors, Supervision Trees, Message Passing** |
| **[`DPX-C`](https://github.com/bivex/DPX-C)** | **C** (C99 - C23) | **Opaque Structs, VTables, MISRA/CERT Safety, Arena Allocators** |
| **[`DPX-Cpp`](https://github.com/bivex/DPX-Cpp)** | **C++** (C++14 - C++20) | **CRTP, Policy-Based Design, RAII Memory Safety, ANTLR4 AST** |
| **[`DPX-Java`](https://github.com/bivex/DPX-Java)** | **Java** (17 - 23+) | **Virtual Threads, Spring Boot / Jakarta EE, GoF Patterns** |
| **[`DPX`](https://github.com/bivex/DPX)** | **Clojure** / Meta Engine | **Pure Functional, Multimethods, Homoiconic Macro Architecture** |
---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
