"""Domain CodeModel entities representing Lua & Luau modules, tables, metatables, and functions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class LuaVariable:
    """Variable or field assignment in Lua."""

    name: str
    is_local: bool = True
    location: SourceLocation | None = None


@dataclass
class LuaFunction:
    """Function or method definition in Lua / Luau."""

    name: str
    is_local: bool = True
    is_method: bool = False  # e.g. function Class:method()
    receiver: str = ""  # e.g. "Class" in Class:method()
    parameters: list[str] = field(default_factory=list)
    body: str = ""
    has_coroutine: bool = False
    has_pcall: bool = False
    has_setmetatable: bool = False
    has_ffi: bool = False
    has_roblox: bool = False
    has_neovim: bool = False
    branch_count: int = 1
    location: SourceLocation | None = None
    raw_text: str = ""


@dataclass
class LuaClassTable:
    """Table representing a class prototype, module, or metatable in Lua."""

    name: str
    is_local: bool = True
    methods: list[LuaFunction] = field(default_factory=list)
    metamethods: list[str] = field(default_factory=list)  # e.g. "__index", "__tostring", "__add"
    fields_count: int = 0
    has_setmetatable: bool = False
    location: SourceLocation | None = None
    raw_text: str = ""

    @property
    def total_methods_count(self) -> int:
        return len(self.methods)


@dataclass
class LuaRequire:
    """Module import statement (require("..."))."""

    module_path: str
    alias: str = ""
    is_ffi: bool = False
    is_roblox: bool = False
    location: SourceLocation | None = None


@dataclass
class LuaTypeAlias:
    """Luau static type annotation ('type Vector3 = { x: number, y: number, z: number }')."""

    name: str
    is_exported: bool = False
    type_def: str = ""
    location: SourceLocation | None = None


@dataclass
class LuaFile:
    """Parsed single Lua source file (.lua, .luau)."""

    file_path: str
    raw_content: str
    lines: list[str] = field(default_factory=list)
    requires: list[LuaRequire] = field(default_factory=list)
    classes: list[LuaClassTable] = field(default_factory=list)
    functions: list[LuaFunction] = field(default_factory=list)
    type_aliases: list[LuaTypeAlias] = field(default_factory=list)
    global_assignments: list[LuaVariable] = field(default_factory=list)


@dataclass
class CodeModel:
    """Aggregated structural model of a scanned Lua / Luau codebase."""

    target_path: str = ""
    files: list[LuaFile] = field(default_factory=list)

    @property
    def all_classes(self) -> list[LuaClassTable]:
        return [c for f in self.files for c in f.classes]

    @property
    def all_functions(self) -> list[LuaFunction]:
        return [fn for f in self.files for fn in f.functions]

    @property
    def all_requires(self) -> list[LuaRequire]:
        return [req for f in self.files for req in f.requires]

    @property
    def all_type_aliases(self) -> list[LuaTypeAlias]:
        return [t for f in self.files for t in f.type_aliases]

    @property
    def all_global_assignments(self) -> list[LuaVariable]:
        return [g for f in self.files for g in f.global_assignments]
