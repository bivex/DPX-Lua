"""Unit tests for all 23 GoF Creational, Structural, and Behavioral patterns in Lua & Luau."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_lua_parser import NativeLuaParserAdapter
from pattern_detector.domain.rules.behavioral_rules import (
    ChainOfResponsibilityMiddlewareRule,
    CommandUndoRedoPayloadRule,
    InterpreterDslEvaluatorRule,
    IteratorStatelessPairsIpairsRule,
    MediatorGameEventCoordinatorRule,
    MementoTableSnapshotRule,
    ObserverSignalListenerRule,
    StateMachineTableFsmRule,
    StrategyTableFunctionInjectionRule,
    TemplateMethodHookLifecycleRule,
    VisitorSceneWalkerRule,
)
from pattern_detector.domain.rules.creational_rules import (
    AbstractFactoryThemeProviderRule,
    BuilderFluentTableConfigRule,
    FactoryConstructorMethodRule,
    PrototypeDeepCloneTableRule,
    SingletonModuleCacheRule,
)
from pattern_detector.domain.rules.structural_rules import (
    AdapterMetatableWrapperRule,
    BridgeDriverRendererRule,
    CompositeSceneGraphNodeRule,
    DecoratorFunctionWrapperRule,
    FacadeInitModuleApiRule,
    FlyweightSharedMetaTableRule,
    ProxyLazyTableIndexerRule,
)
from pattern_detector.domain.value_objects import PatternType


# --- Creational (5/5) ---

def test_singleton_module_cache() -> None:
    code = """
local ServiceRegistry = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("registry.lua", code)])

    rule = SingletonModuleCacheRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.SINGLETON_MODULE_CACHE


def test_factory_constructor_method() -> None:
    code = """
local function create_enemy(kind)
    return { type = kind, health = 100 }
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("factory.lua", code)])

    rule = FactoryConstructorMethodRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FACTORY_CONSTRUCTOR_METHOD


def test_abstract_factory_theme_provider() -> None:
    code = """
local DarkThemeFactory = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("theme.lua", code)])

    rule = AbstractFactoryThemeProviderRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ABSTRACT_FACTORY_THEME_PROVIDER


def test_builder_fluent_table_config() -> None:
    code = """
local EntityBuilder = {}
EntityBuilder.__index = EntityBuilder

function EntityBuilder:with_position(x, y)
    self.x = x
    self.y = y
    return self
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("builder.lua", code)])

    rule = BuilderFluentTableConfigRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.BUILDER_FLUENT_TABLE_CONFIG


def test_prototype_deep_clone_table() -> None:
    code = """
local function deep_copy(t)
    local clone = {}
    for k, v in pairs(t) do
        clone[k] = type(v) == "table" and deep_copy(v) or v
    end
    return clone
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("clone.lua", code)])

    rule = PrototypeDeepCloneTableRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROTOTYPE_DEEP_CLONE_TABLE


# --- Structural (7/7) ---

def test_adapter_metatable_wrapper() -> None:
    code = """
local LegacyAdapter = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("adapter.lua", code)])

    rule = AdapterMetatableWrapperRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ADAPTER_METATABLE_WRAPPER


def test_bridge_driver_renderer() -> None:
    code = """
local Love2DRenderer = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("renderer.lua", code)])

    rule = BridgeDriverRendererRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.BRIDGE_DRIVER_RENDERER


def test_composite_scene_graph_node() -> None:
    code = """
local SceneNode = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("node.lua", code)])

    rule = CompositeSceneGraphNodeRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMPOSITE_SCENE_GRAPH_NODE


def test_decorator_function_wrapper() -> None:
    code = """
local function memoize(fn)
    local cache = {}
    return function(arg)
        if cache[arg] == nil then cache[arg] = fn(arg) end
        return cache[arg]
    end
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("memo.lua", code)])

    rule = DecoratorFunctionWrapperRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DECORATOR_FUNCTION_WRAPPER


def test_facade_init_module_api() -> None:
    code = """
local M = {}
return M
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("engine/init.lua", code)])

    rule = FacadeInitModuleApiRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FACADE_INIT_MODULE_API


def test_flyweight_shared_meta_table() -> None:
    code = """
local ParticleFlyweight = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("particle.lua", code)])

    rule = FlyweightSharedMetaTableRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FLYWEIGHT_SHARED_META_TABLE


def test_proxy_lazy_table_indexer() -> None:
    code = """
local LazyTable = {}
LazyTable.__newindex = function(t, k, v)
    rawset(t, k, v)
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("proxy.lua", code)])

    rule = ProxyLazyTableIndexerRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROXY_LAZY_TABLE_INDEXER


# --- Behavioral (11/11) ---

def test_chain_of_responsibility_middleware() -> None:
    code = """
local function auth_middleware(req, res, next)
    if req.token then
        return next(req, res)
    end
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("mw.lua", code)])

    rule = ChainOfResponsibilityMiddlewareRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CHAIN_OF_RESPONSIBILITY_MIDDLEWARE


def test_command_undo_redo_payload() -> None:
    code = """
local MoveCommand = {}
MoveCommand.__index = MoveCommand

function MoveCommand:execute()
    self.entity.x = self.to_x
end

function MoveCommand:undo()
    self.entity.x = self.from_x
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("cmd.lua", code)])

    rule = CommandUndoRedoPayloadRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.COMMAND_UNDO_REDO_PAYLOAD


def test_interpreter_dsl_evaluator() -> None:
    code = """
local function eval_expr(ast)
    if ast.type == "add" then
        return eval_expr(ast.left) + eval_expr(ast.right)
    end
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("eval.lua", code)])

    rule = InterpreterDslEvaluatorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.INTERPRETER_DSL_EVALUATOR


def test_iterator_stateless_pairs_ipairs() -> None:
    code = """
local function iter_range(from, to)
    local i = from - 1
    return function()
        i = i + 1
        if i <= to then return i end
    end
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("iter.lua", code)])

    rule = IteratorStatelessPairsIpairsRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.ITERATOR_STATELESS_PAIRS_IPAIRS


def test_mediator_game_event_coordinator() -> None:
    code = """
local GameEventManager = {}
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("manager.lua", code)])

    rule = MediatorGameEventCoordinatorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MEDIATOR_GAME_EVENT_COORDINATOR


def test_memento_table_snapshot() -> None:
    code = """
local function save_state(game)
    return { level = game.level, score = game.score }
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("save.lua", code)])

    rule = MementoTableSnapshotRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MEMENTO_TABLE_SNAPSHOT


def test_observer_signal_listener() -> None:
    code = """
local Broadcaster = {}
Broadcaster.__index = Broadcaster

function Broadcaster:subscribe(fn)
    table.insert(self.subs, fn)
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("obs.lua", code)])

    rule = ObserverSignalListenerRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.OBSERVER_SIGNAL_LISTENER


def test_state_machine_table_fsm() -> None:
    code = """
local PlayerFSM = {}
PlayerFSM.__index = PlayerFSM

function PlayerFSM:transition_to(state)
    self.current = state
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("fsm.lua", code)])

    rule = StateMachineTableFsmRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.STATE_MACHINE_TABLE_FSM


def test_strategy_table_function_injection() -> None:
    code = """
local function sort_entities(entities, comparator)
    table.sort(entities, comparator)
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("sort.lua", code)])

    rule = StrategyTableFunctionInjectionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.STRATEGY_TABLE_FUNCTION_INJECTION


def test_template_method_hook_lifecycle() -> None:
    code = """
local BaseEntity = {}
BaseEntity.__index = BaseEntity

function BaseEntity:update(dt)
    self:on_before_update(dt)
    self.x = self.x + 1
end

function BaseEntity:on_before_update(dt)
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("entity.lua", code)])

    rule = TemplateMethodHookLifecycleRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TEMPLATE_METHOD_HOOK_LIFECYCLE


def test_visitor_scene_walker() -> None:
    code = """
local function walk_scene(node, callback)
    callback(node)
    for _, child in ipairs(node.children) do
        walk_scene(child, callback)
    end
end
"""
    parser = NativeLuaParserAdapter()
    model = parser.parse_codebase([("walker.lua", code)])

    rule = VisitorSceneWalkerRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.VISITOR_SCENE_WALKER
