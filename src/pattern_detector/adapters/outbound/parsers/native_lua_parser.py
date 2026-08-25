"""High-speed native parser adapter for Lua & Luau source code (.lua, .luau)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import (
    CodeModel,
    LuaClassTable,
    LuaFile,
    LuaFunction,
    LuaRequire,
    LuaTypeAlias,
    LuaVariable,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


def _split_top_level_commas(s: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in s:
        if char in "([{<":
            depth += 1
            current.append(char)
        elif char in ")]}>":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [p for p in parts if p]


class NativeLuaParserAdapter(ParserPort):
    """Single-pass robust parser extracting Lua/Luau tables, metatables, functions, and Luau types."""

    REQUIRE_PATTERN = re.compile(
        r"^(?:local\s+(?P<alias>[a-zA-Z0-9_]+)\s*=\s*)?require\s*\(\s*[\"'](?P<path>[^\"']+)[\"']\s*\)"
    )
    TABLE_DECL_PATTERN = re.compile(
        r"^\s*(?P<local>local\s+)?(?P<name>[a-zA-Z0-9_]+)\s*=\s*(?:\{|setmetatable\s*\()"
    )
    FN_HEADER_PATTERN = re.compile(
        r"^\s*(?P<local>local\s+)?function\s+(?:(?P<receiver>[a-zA-Z0-9_]+)(?P<sep>[:.]))?(?P<name>[a-zA-Z0-9_]+)\s*\("
    )
    TYPE_ALIAS_PATTERN = re.compile(
        r"^\s*(?P<export>export\s+)?type\s+(?P<name>[a-zA-Z0-9_]+)\s*=\s*(?P<def>[^;]+)"
    )
    METAMETHOD_ASSIGN_PATTERN = re.compile(
        r"^\s*(?P<target>[a-zA-Z0-9_]+)\.(?P<meta>__[a-zA-Z0-9_]+)\s*="
    )
    GLOBAL_ASSIGN_PATTERN = re.compile(
        r"^\s*(?P<name>[a-zA-Z0-9_]+)\s*=\s*[^=]"
    )

    KNOWN_GLOBALS = {"_G", "math", "table", "string", "coroutine", "os", "io", "debug", "package", "utf8", "bit32", "bit", "ffi", "vim", "game", "workspace", "script"}

    def parse_file(self, file_path: str, content: str) -> LuaFile:
        lines = content.splitlines()
        file_obj = LuaFile(file_path=file_path, raw_content=content, lines=lines)

        current_function: LuaFunction | None = None
        current_func_body: list[str] = []
        block_depth = 0

        # Map to collect tables/classes by name
        tables_by_name: dict[str, LuaClassTable] = {}

        for line_idx, raw_line in enumerate(lines, 1):
            trimmed = raw_line.strip()

            # Skip comments and empty lines
            if trimmed.startswith("--") or not trimmed:
                continue

            # Requires
            req_m = self.REQUIRE_PATTERN.match(trimmed)
            if req_m:
                alias = req_m.group("alias") or ""
                path = req_m.group("path")
                is_ffi = path == "ffi"
                is_roblox = "ReplicatedStorage" in path or "ServerScriptService" in path
                file_obj.requires.append(
                    LuaRequire(
                        module_path=path,
                        alias=alias,
                        is_ffi=is_ffi,
                        is_roblox=is_roblox,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    )
                )

            # Luau Type Alias
            type_m = self.TYPE_ALIAS_PATTERN.match(trimmed)
            if type_m:
                t_name = type_m.group("name")
                t_export = bool(type_m.group("export"))
                t_def = type_m.group("def").strip()
                file_obj.type_aliases.append(
                    LuaTypeAlias(
                        name=t_name,
                        is_exported=t_export,
                        type_def=t_def,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    )
                )

            # Metamethod assignment (e.g. Class.__index = Class)
            meta_m = self.METAMETHOD_ASSIGN_PATTERN.match(trimmed)
            if meta_m:
                tgt = meta_m.group("target")
                meta = meta_m.group("meta")
                if tgt in tables_by_name:
                    tables_by_name[tgt].metamethods.append(meta)

            # Table Declaration
            tbl_m = self.TABLE_DECL_PATTERN.match(trimmed)
            if tbl_m and not current_function:
                is_loc = bool(tbl_m.group("local"))
                t_name = tbl_m.group("name")
                if t_name not in self.KNOWN_GLOBALS:
                    cls_obj = LuaClassTable(
                        name=t_name,
                        is_local=is_loc,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                        raw_text=raw_line,
                    )
                    if "setmetatable" in trimmed:
                        cls_obj.has_setmetatable = True
                    tables_by_name[t_name] = cls_obj

            # Function Start (using balanced parenthesis parsing)
            if not current_function:
                fn_match = self.FN_HEADER_PATTERN.match(trimmed)
                if fn_match:
                    is_loc = bool(fn_match.group("local"))
                    recv = fn_match.group("receiver") or ""
                    sep = fn_match.group("sep") or ""
                    fn_name = fn_match.group("name")
                    is_meth = sep == ":"

                    if recv and recv not in tables_by_name and recv not in self.KNOWN_GLOBALS:
                        tables_by_name[recv] = LuaClassTable(
                            name=recv,
                            is_local=False,
                            location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                            raw_text=raw_line,
                        )

                    rest = trimmed[fn_match.end():]
                    depth = 1
                    i = 0
                    while i < len(rest) and depth > 0:
                        if rest[i] == "(":
                            depth += 1
                        elif rest[i] == ")":
                            depth -= 1
                        i += 1

                    params_str = rest[:i-1] if i > 0 else ""
                    params = [p.strip() for p in _split_top_level_commas(params_str) if p.strip()]

                    current_function = LuaFunction(
                        name=fn_name,
                        is_local=is_loc,
                        is_method=is_meth,
                        receiver=recv,
                        parameters=params,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                        raw_text=raw_line,
                    )
                    current_func_body = [raw_line]

                    # Single line function (e.g. function() return 1 end)
                    if trimmed.endswith("end") and "end" in raw_line[fn_match.end():]:
                        current_function.body = "\n".join(current_func_body)
                        file_obj.functions.append(current_function)
                        if recv and recv in tables_by_name:
                            tables_by_name[recv].methods.append(current_function)
                        current_function = None
                        current_func_body = []
                        block_depth = 0
                    else:
                        block_depth = 1
                    continue

            # Inside Function: Accumulate body
            if current_function:
                current_func_body.append(raw_line)

                # Track block nesting: function, then, do, repeat
                opening_words = len(re.findall(r"\b(function|then|do|repeat)\b", raw_line))
                closing_words = len(re.findall(r"\b(end|until)\b", raw_line))
                block_depth += opening_words - closing_words

                if "coroutine." in raw_line:
                    current_function.has_coroutine = True
                if "pcall(" in raw_line or "xpcall(" in raw_line:
                    current_function.has_pcall = True
                if "setmetatable(" in raw_line:
                    current_function.has_setmetatable = True
                if "ffi." in raw_line:
                    current_function.has_ffi = True
                if "game:" in raw_line or "Instance.new" in raw_line:
                    current_function.has_roblox = True
                if "vim." in raw_line:
                    current_function.has_neovim = True

                if block_depth <= 0:
                    current_function.body = "\n".join(current_func_body)
                    file_obj.functions.append(current_function)
                    if current_function.receiver and current_function.receiver in tables_by_name:
                        tables_by_name[current_function.receiver].methods.append(current_function)
                    current_function = None
                    current_func_body = []
                    block_depth = 0
                continue

            # Global Assignment Detection outside function
            if not current_function:
                glob_m = self.GLOBAL_ASSIGN_PATTERN.match(trimmed)
                if glob_m and not trimmed.startswith("local ") and not trimmed.startswith("return "):
                    g_name = glob_m.group("name")
                    if g_name not in self.KNOWN_GLOBALS and not g_name.startswith("_") and "." not in g_name and ":" not in g_name:
                        file_obj.global_assignments.append(
                            LuaVariable(
                                name=g_name,
                                is_local=False,
                                location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                            )
                        )

        # Flush tables to file
        file_obj.classes = list(tables_by_name.values())
        return file_obj

    def parse_codebase(self, files: list[tuple[str, str]], target_path: str = "") -> CodeModel:
        model = CodeModel(target_path=target_path)
        for fpath, content in files:
            lua_file = self.parse_file(fpath, content)
            model.files.append(lua_file)
        return model
