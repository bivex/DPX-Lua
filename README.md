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

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
