from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


REQUIRED_FRONT_MATTER_KEYS = (
    "title",
    "chapter",
    "stage",
    "type",
    "difficulty",
    "prerequisites",
    "objectives",
    "study_time",
    "practice_level",
    "keywords",
    "versions",
    "status",
    "last_updated",
)

ALLOWED_TYPES = frozenset(
    {
        "concept",
        "principle",
        "service",
        "platform",
        "tool",
        "language",
        "cloud-service",
        "hardware",
        "methodology",
    }
)

ALLOWED_STATUSES = frozenset({"draft", "reviewed", "verified", "deprecated"})

PLACEHOLDER_DIRECTORIES = (
    "学习路线",
    "技术索引",
    "知识库",
    "实验手册",
    "项目实战",
    "故障案例",
    "面试体系",
    "运维思维训练",
    "企业规范",
)

FENCE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,}).*$")
TOP_LEVEL_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<value>.*)$")
LIST_ITEM_RE = re.compile(r"^  -(?:\s+(?P<value>.*))?$")
MAP_ITEM_RE = re.compile(
    r"^  (?P<key>[A-Za-z_][A-Za-z0-9_.-]*):(?:\s*(?P<value>.*))$"
)
INLINE_LINK_RE = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?P<target><[^>\n]+>|[^)\n]*?)\s*\)"
)
REFERENCE_LINK_RE = re.compile(
    r"(?m)^[ ]{0,3}\[[^\]\n]+\]:[ \t]*(?P<target><[^>\n]+>|\S+)"
)
DRIVE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")
PLACEHOLDER_PATTERNS = (
    ("PH001", "模糊英文占位符", re.compile(r"\b(?:TODO|TBD)\b", re.IGNORECASE)),
    ("PH002", "模糊中文占位符", re.compile(r"待补充|后续完善|稍后完善|这里填写")),
    (
        "PH003",
        "模板必填/可选标记残留",
        re.compile(r"<(?:必填|可选)[：:][^>\n]+>"),
    ),
    ("PH004", "填写/替换标记残留", re.compile(r"<(?:填写|替换)[^>\n]*>")),
)
ACCESS_KEY_RE = re.compile(r"\bAKIA[A-Z0-9]{12,}\b")
PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
)
DIRECT_SECRET_RE = re.compile(
    r"(?im)\b(?:access[_-]?key(?:[_-]?id|[_-]?secret)?|secret[_-]?key|api[_-]?key)\b"
    r"[ \t]*[:=][ \t]*(?P<value>[^\s#]+)"
)


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    line: int
    rule: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.rule} {self.message}"


@dataclass
class _FrontMatterResult:
    values: dict[str, str]
    key_lines: dict[str, int]
    kinds: dict[str, str]
    duplicates: list[tuple[str, int]]
    structure_errors: list[tuple[int, str]]
    has_opening: bool
    has_closing: bool


@dataclass(frozen=True)
class _RepositoryResult:
    errors: tuple[str, ...]
    markdown_count: int
    knowledge_count: int
    local_link_count: int


def _display_path(path: Path) -> str:
    return path.as_posix()


def _parse_scalar(value: str) -> tuple[str, bool]:
    value = value.strip()
    if not value:
        return "", True
    quotes = {'"', "'"}
    if value[0] in quotes:
        quote = value[0]
        if len(value) < 2 or value[-1] != quote:
            return value, False
        inner = value[1:-1]
        if quote in inner:
            return value, False
        return inner, True
    if value[-1] in quotes or any(quote in value for quote in quotes):
        return value, False
    return value, True


def _mask_fenced_code(text: str) -> str:
    lines = text.splitlines(keepends=True)
    active_char: str | None = None
    active_length = 0
    masked: list[str] = []
    for line in lines:
        content = line.rstrip("\r\n")
        match = FENCE_RE.match(content)
        if active_char is None and match:
            fence = match.group("fence")
            active_char, active_length = fence[0], len(fence)
            masked.append("\n" if line.endswith("\n") else "")
            continue
        if active_char is not None:
            closing = content.lstrip()
            if re.fullmatch(re.escape(active_char) + "{" + str(active_length) + ",}\\s*", closing):
                active_char = None
                active_length = 0
            masked.append("\n" if line.endswith("\n") else "")
            continue
        masked.append(line)
    return "".join(masked)


def _mask_inline_code(text: str) -> str:
    characters = list(text)
    index = 0
    while index < len(text):
        if text[index] != "`":
            index += 1
            continue
        run_end = index
        while run_end < len(text) and text[run_end] == "`":
            run_end += 1
        delimiter = text[index:run_end]
        closing = text.find(delimiter, run_end)
        if closing < 0:
            index = run_end
            continue
        span_end = closing + len(delimiter)
        for position in range(index, span_end):
            if characters[position] not in {"\r", "\n"}:
                characters[position] = " "
        index = span_end
    return "".join(characters)


def _parse_front_matter(text: str) -> _FrontMatterResult:
    lines = text.splitlines()
    result = _FrontMatterResult({}, {}, {}, [], [], False, False)
    if not lines or lines[0] != "---":
        return result
    result.has_opening = True
    closing_index: int | None = None
    for index in range(1, len(lines)):
        if lines[index] == "---":
            closing_index = index
            result.has_closing = True
            break
    if closing_index is None:
        return result

    current_key: str | None = None
    blocks: dict[str, list[str]] = {}
    for index in range(1, closing_index):
        line = lines[index]
        line_number = index + 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t")):
            match = TOP_LEVEL_RE.fullmatch(line)
            if match is None:
                result.structure_errors.append((line_number, "不支持的顶层结构"))
                current_key = None
                continue
            key = match.group("key")
            raw_value = match.group("value").strip()
            if key in result.key_lines:
                result.duplicates.append((key, line_number))
                current_key = key
                continue
            result.key_lines[key] = line_number
            current_key = key
            blocks[key] = []
            if raw_value in {"|", ">", "|-", ">-", "|+", ">+"} or raw_value.startswith(
                ("&", "*", "!!")
            ):
                result.structure_errors.append((line_number, f"键 {key} 使用了不支持的 YAML 语法"))
                result.values[key] = ""
                result.kinds[key] = "unsupported"
            else:
                scalar, scalar_is_valid = _parse_scalar(raw_value)
                result.values[key] = scalar
                result.kinds[key] = (
                    "pending" if not raw_value else "scalar" if scalar_is_valid else "unsupported"
                )
                if not scalar_is_valid:
                    result.structure_errors.append(
                        (line_number, f"键 {key} 包含不受支持的 quoted scalar")
                    )
            continue

        if line.startswith("\t") or len(line) - len(line.lstrip(" ")) != 2:
            result.structure_errors.append((line_number, "只支持两空格的一层缩进"))
            continue
        if current_key is None:
            result.structure_errors.append((line_number, "缩进项没有对应的顶层键"))
            continue
        list_match = LIST_ITEM_RE.fullmatch(line)
        map_match = MAP_ITEM_RE.fullmatch(line)
        if current_key in {"prerequisites", "objectives", "keywords"} and list_match:
            item, item_is_valid = _parse_scalar(list_match.group("value") or "")
            if not item:
                result.structure_errors.append((line_number, f"{current_key} 包含空列表项"))
            if not item_is_valid:
                result.structure_errors.append(
                    (line_number, f"{current_key} 包含不受支持的 quoted scalar")
                )
            blocks[current_key].append(line)
            result.values[current_key] = "\n".join(blocks[current_key])
            result.kinds[current_key] = "list"
        elif current_key == "versions" and map_match:
            item_value, item_is_valid = _parse_scalar(map_match.group("value") or "")
            if not item_value:
                result.structure_errors.append((line_number, "versions 包含空映射值"))
            if not item_is_valid:
                result.structure_errors.append(
                    (line_number, "versions 包含不受支持的 quoted scalar")
                )
            blocks[current_key].append(line)
            result.values[current_key] = "\n".join(blocks[current_key])
            result.kinds[current_key] = "map"
        else:
            result.structure_errors.append((line_number, f"键 {current_key} 的缩进结构不受支持"))
    return result


def extract_front_matter(text: str) -> dict[str, str]:
    return dict(_parse_front_matter(text).values)


def _front_matter_diagnostics(path: Path, text: str) -> tuple[list[Diagnostic], _FrontMatterResult]:
    display = _display_path(path)
    parsed = _parse_front_matter(text)
    diagnostics: list[Diagnostic] = []
    if not parsed.has_opening:
        diagnostics.append(Diagnostic(display, 1, "FM001", "缺少文件首行 Front Matter 分隔符"))
        return diagnostics, parsed
    if not parsed.has_closing:
        diagnostics.append(Diagnostic(display, 1, "FM001", "Front Matter 缺少结束分隔符"))
        return diagnostics, parsed

    for key in REQUIRED_FRONT_MATTER_KEYS:
        if key not in parsed.key_lines:
            diagnostics.append(Diagnostic(display, 1, "FM002", f"缺少必需键 {key}"))
    for key, line in parsed.duplicates:
        diagnostics.append(Diagnostic(display, line, "FM003", f"顶层键 {key} 重复"))

    for key in REQUIRED_FRONT_MATTER_KEYS:
        if key not in parsed.key_lines:
            continue
        value = parsed.values.get(key, "")
        kind = parsed.kinds.get(key, "")
        line = parsed.key_lines[key]
        if key in {"prerequisites", "objectives", "keywords"}:
            if value == "[]" or kind == "pending":
                diagnostics.append(Diagnostic(display, line, "FM004", f"{key} 必须是非空列表"))
            elif kind != "list":
                diagnostics.append(Diagnostic(display, line, "FM008", f"{key} 只支持缩进列表"))
        elif key == "versions":
            if value == "{}":
                pass
            elif kind == "pending":
                diagnostics.append(Diagnostic(display, line, "FM004", "versions 必须为 {} 或非空映射"))
            elif kind != "map":
                diagnostics.append(Diagnostic(display, line, "FM008", "versions 只支持 {} 或一层映射"))
        elif not value:
            diagnostics.append(Diagnostic(display, line, "FM004", f"{key} 不得为空"))

    type_value = parsed.values.get("type")
    if type_value and type_value not in ALLOWED_TYPES:
        diagnostics.append(
            Diagnostic(display, parsed.key_lines["type"], "FM005", f"非法 type：{type_value}")
        )
    status_value = parsed.values.get("status")
    if status_value and status_value not in ALLOWED_STATUSES:
        diagnostics.append(
            Diagnostic(display, parsed.key_lines["status"], "FM006", f"非法 status：{status_value}")
        )
    date_value = parsed.values.get("last_updated")
    if date_value:
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_value):
                raise ValueError
            date.fromisoformat(date_value)
        except ValueError:
            diagnostics.append(
                Diagnostic(
                    display,
                    parsed.key_lines["last_updated"],
                    "FM007",
                    f"last_updated 不是有效 YYYY-MM-DD 日期：{date_value}",
                )
            )
    diagnostics.extend(
        Diagnostic(display, line, "FM008", message)
        for line, message in parsed.structure_errors
    )
    return diagnostics, parsed


def validate_front_matter(path: Path, text: str) -> list[str]:
    diagnostics, _ = _front_matter_diagnostics(path, text)
    return [item.render() for item in sorted(diagnostics)]


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _link_targets(text: str) -> list[tuple[int, str]]:
    masked = _mask_inline_code(_mask_fenced_code(text))
    targets = [
        (_line_number(masked, match.start()), match.group("target").strip())
        for match in INLINE_LINK_RE.finditer(masked)
    ]
    targets.extend(
        (_line_number(masked, match.start()), match.group("target").strip())
        for match in REFERENCE_LINK_RE.finditer(masked)
    )
    return sorted(targets, key=lambda item: (item[0], item[1]))


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _case_status(root: Path, candidate: Path) -> tuple[str, str | None]:
    """Return (status, actual path); status is exact, mismatch, or missing."""
    try:
        parts = candidate.relative_to(root).parts
    except ValueError:
        return "missing", None
    current = root
    mismatch = False
    for part in parts:
        try:
            children = list(current.iterdir())
        except OSError:
            return "missing", None
        exact = next((child for child in children if child.name == part), None)
        if exact is not None:
            current = exact
            continue
        folded = next((child for child in children if child.name.casefold() == part.casefold()), None)
        if folded is None:
            return "missing", None
        mismatch = True
        current = folded
    return ("mismatch" if mismatch else "exact"), current.as_posix()


def _requested_candidate(root: Path, source: Path, decoded: str) -> Path:
    parts = list(source.parent.relative_to(root).parts)
    for part in Path(decoded).parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return root.joinpath(*parts)


def validate_local_links(path: Path, text: str, root: Path) -> list[str]:
    root = root.resolve(strict=False)
    source = path.resolve(strict=False) if path.is_absolute() else (root / path).resolve(strict=False)
    display = _relative_path(source, root)
    diagnostics: list[Diagnostic] = []
    for line, raw_target in _link_targets(text):
        target = raw_target
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        if not target:
            diagnostics.append(Diagnostic(display, line, "LINK005", "本地链接目标为空"))
            continue
        lowered = target.lower()
        if lowered.startswith(("http://", "https://", "mailto:")) or target.startswith("#"):
            continue
        if DRIVE_PATH_RE.match(target) or target.startswith(("/", "\\")):
            diagnostics.append(
                Diagnostic(display, line, "LINK003", "绝对本地路径或 Windows 盘符链接不受支持")
            )
            continue
        try:
            split = urlsplit(target)
        except ValueError:
            diagnostics.append(Diagnostic(display, line, "LINK005", "无法解析本地链接目标"))
            continue
        if split.scheme:
            diagnostics.append(
                Diagnostic(display, line, "LINK005", f"不支持的链接 scheme：{split.scheme}")
            )
            continue
        decoded = unquote(split.path).replace("\\", "/")
        if not decoded:
            continue
        resolved_candidate = (source.parent / Path(decoded)).resolve(strict=False)
        if resolved_candidate != root and root not in resolved_candidate.parents:
            diagnostics.append(Diagnostic(display, line, "LINK002", "本地链接目标越出仓库根目录"))
            continue
        requested_candidate = _requested_candidate(root, source, decoded)
        status, actual = _case_status(root, requested_candidate)
        if status == "mismatch":
            actual_display = _relative_path(Path(actual), root) if actual else "未知"
            diagnostics.append(
                Diagnostic(
                    display,
                    line,
                    "LINK004",
                    f"链接大小写与实际路径不一致；实际路径为 {actual_display}",
                )
            )
        elif status == "missing":
            diagnostics.append(
                Diagnostic(display, line, "LINK001", f"本地链接目标不存在：{decoded}")
            )
    return [item.render() for item in sorted(diagnostics)]


def validate_placeholders(path: Path, text: str) -> list[str]:
    if not path.parts or path.parts[0] not in PLACEHOLDER_DIRECTORIES:
        return []
    masked = _mask_fenced_code(text)
    display = _display_path(path)
    diagnostics: list[Diagnostic] = []
    for rule, message, pattern in PLACEHOLDER_PATTERNS:
        diagnostics.extend(
            Diagnostic(display, _line_number(masked, match.start()), rule, message)
            for match in pattern.finditer(masked)
        )
    return [item.render() for item in sorted(diagnostics)]


def validate_sensitive_information(path: Path, text: str) -> list[str]:
    display = _display_path(path)
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(
        Diagnostic(display, _line_number(text, match.start()), "SEC001", "检测到云 AccessKey 格式")
        for match in ACCESS_KEY_RE.finditer(text)
    )
    diagnostics.extend(
        Diagnostic(display, _line_number(text, match.start()), "SEC002", "检测到私钥头")
        for match in PRIVATE_KEY_RE.finditer(text)
    )
    for match in DIRECT_SECRET_RE.finditer(text):
        raw_value = match.group("value").strip().strip('"\'')
        if (
            not raw_value
            or raw_value.startswith("<")
            or raw_value.startswith(("$", "${", "%"))
            or raw_value in {"''", '""', "null", "None"}
        ):
            continue
        diagnostics.append(
            Diagnostic(
                display,
                _line_number(text, match.start()),
                "SEC003",
                "检测到敏感字段直接赋非占位值",
            )
        )
    unique = sorted(set(diagnostics))
    return [item.render() for item in unique]


def _error_sort_key(error: str) -> tuple[str, int, str, str]:
    match = re.match(r"^(.*):(\d+):\s+([A-Z]+\d+)\s+(.*)$", error)
    if match is None:
        return error, 0, "", ""
    return match.group(1), int(match.group(2)), match.group(3), match.group(4)


def _is_knowledge_article(path: Path) -> bool:
    return bool(path.parts) and path.parts[0] == "知识库" and path.name.casefold() != "readme.md"


def _is_local_link_target(raw_target: str) -> bool:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    lowered = target.lower()
    return bool(target) and not lowered.startswith(("http://", "https://", "mailto:")) and not target.startswith("#")


def _aggregate_repository_checked(
    root: Path, markdown_files: list[Path]
) -> _RepositoryResult:
    errors: list[str] = []
    chapters: dict[str, list[tuple[str, int]]] = {}
    knowledge_count = 0
    local_link_count = 0

    for path in markdown_files:
        relative = path.relative_to(root)
        display = relative.as_posix()
        if _is_knowledge_article(relative):
            knowledge_count += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(Diagnostic(display, 0, "IO002", "无法以 UTF-8 读取 Markdown").render())
            continue

        targets = _link_targets(text)
        local_link_count += sum(_is_local_link_target(target) for _, target in targets)
        errors.extend(validate_local_links(path, text, root))
        errors.extend(validate_sensitive_information(relative, text))
        errors.extend(validate_placeholders(relative, text))

        if _is_knowledge_article(relative):
            front_errors, parsed = _front_matter_diagnostics(relative, text)
            errors.extend(item.render() for item in front_errors)
            chapter = parsed.values.get("chapter", "")
            if (
                parsed.has_opening
                and parsed.has_closing
                and not parsed.structure_errors
                and not any(key == "chapter" for key, _ in parsed.duplicates)
                and chapter
            ):
                chapters.setdefault(chapter, []).append(
                    (display, parsed.key_lines.get("chapter", 1))
                )

    for chapter, locations in sorted(chapters.items()):
        if len(locations) < 2:
            continue
        for display, line in locations:
            others = ", ".join(path for path, _ in locations if path != display)
            errors.append(
                Diagnostic(
                    display,
                    line,
                    "CH001",
                    f"chapter {chapter} 重复；其他文件：{others}",
                ).render()
            )

    ordered = tuple(sorted(set(errors), key=_error_sort_key))
    return _RepositoryResult(ordered, len(markdown_files), knowledge_count, local_link_count)


def _root_path_error_result() -> _RepositoryResult:
    error = Diagnostic(".", 0, "IO003", "根路径解析或遍历失败").render()
    return _RepositoryResult((error,), 0, 0, 0)


def _aggregate_repository(root: Path) -> _RepositoryResult:
    try:
        root = root.resolve(strict=False)
        if not root.exists() or not root.is_dir():
            error = Diagnostic(".", 0, "IO001", "仓库根目录不存在或不是目录").render()
            return _RepositoryResult((error,), 0, 0, 0)
        markdown_files = sorted(
            (
                path
                for path in root.rglob("*.md")
                if path.is_file() and ".git" not in path.relative_to(root).parts
            ),
            key=lambda path: path.relative_to(root).as_posix(),
        )
    except (OSError, ValueError):
        return _root_path_error_result()
    return _aggregate_repository_checked(root, markdown_files)


def validate_repository(root: Path) -> list[str]:
    return list(_aggregate_repository(root).errors)


def _success_summary(root: Path) -> str:
    result = _aggregate_repository(root)
    return (
        f"校验通过：Markdown {result.markdown_count}，知识章节 {result.knowledge_count}，"
        f"本地链接 {result.local_link_count}；错误 0"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校验 cloud-ops-roadmap Markdown 基础门禁")
    parser.add_argument("root", nargs="?", default=".", help="仓库根目录，默认当前目录")
    args = parser.parse_args(argv)
    result = _aggregate_repository(Path(args.root))
    if result.errors:
        for error in result.errors:
            print(error, file=sys.stderr)
        print(f"校验失败：{len(result.errors)} 个错误", file=sys.stderr)
        return 1
    print(
        f"校验通过：Markdown {result.markdown_count}，知识章节 {result.knowledge_count}，"
        f"本地链接 {result.local_link_count}；错误 0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
