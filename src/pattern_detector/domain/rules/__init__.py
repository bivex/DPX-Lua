"""Rules registry and aggregation factory for Lua & Luau pattern detector."""

from __future__ import annotations

from pattern_detector.domain.rules.base import BaseRule
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
from pattern_detector.domain.rules.gamedev_rules import (
    EcsComponentTableLayoutRule,
    EventSignalListenerBusRule,
    NeovimPluginApiFacadeRule,
    RobloxInstanceReplicationBridgeRule,
)
from pattern_detector.domain.rules.hazards_rules import (
    CoroutineUnhandledDeadlockHazardRule,
    GlobalVariableLeakHazardRule,
    NilIndexingMetatableHazardRule,
    TableRehashLoopHazardRule,
)
from pattern_detector.domain.rules.idiomatic_rules import (
    ClosureModuleEncapsulationRule,
    CoroutineCooperativeTaskRule,
    LuauStaticTypeAnnotationRule,
    MetatablePrototypeOopRule,
    OperatorOverloadingMetamethodsRule,
    PcallXpcallRailwayErrorRule,
)
from pattern_detector.domain.rules.luajit_systems_rules import (
    LuajitFfiCBindingRule,
    PackedBitfieldManipulationRule,
    TablePreallocationCacheRule,
)
from pattern_detector.domain.rules.solid_principles_rules import (
    DeepTableNestingDemeterRule,
    FatMetatableInterfaceIspRule,
    MonolithicModuleSrpRule,
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

DEFAULT_RULES: list[type[BaseRule]] = [
    # 1. Lua & Luau Idiomatic & Metatable OOP (6)
    MetatablePrototypeOopRule,
    OperatorOverloadingMetamethodsRule,
    ClosureModuleEncapsulationRule,
    CoroutineCooperativeTaskRule,
    LuauStaticTypeAnnotationRule,
    PcallXpcallRailwayErrorRule,

    # 2. GameDev, Roblox & Neovim Extension (4)
    RobloxInstanceReplicationBridgeRule,
    EcsComponentTableLayoutRule,
    NeovimPluginApiFacadeRule,
    EventSignalListenerBusRule,

    # 3. LuaJIT FFI & Systems Performance (3)
    LuajitFfiCBindingRule,
    TablePreallocationCacheRule,
    PackedBitfieldManipulationRule,

    # 4. Creational Patterns (5/5)
    SingletonModuleCacheRule,
    FactoryConstructorMethodRule,
    AbstractFactoryThemeProviderRule,
    BuilderFluentTableConfigRule,
    PrototypeDeepCloneTableRule,

    # 5. Structural Patterns (7/7)
    AdapterMetatableWrapperRule,
    BridgeDriverRendererRule,
    CompositeSceneGraphNodeRule,
    DecoratorFunctionWrapperRule,
    FacadeInitModuleApiRule,
    FlyweightSharedMetaTableRule,
    ProxyLazyTableIndexerRule,

    # 6. Behavioral Patterns (11/11)
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

    # 7. Hazards & Performance Traps (4)
    GlobalVariableLeakHazardRule,
    TableRehashLoopHazardRule,
    NilIndexingMetatableHazardRule,
    CoroutineUnhandledDeadlockHazardRule,

    # 8. SOLID Principles & Smells (3)
    MonolithicModuleSrpRule,
    FatMetatableInterfaceIspRule,
    DeepTableNestingDemeterRule,
]


def get_default_rules() -> list[BaseRule]:
    """Instantiate and return full suite of default Lua & Luau rules."""
    return [rule_cls() for rule_cls in DEFAULT_RULES]
