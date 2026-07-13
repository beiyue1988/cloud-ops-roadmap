from __future__ import annotations

import argparse
from dataclasses import dataclass, field
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

OUTLINE_GATES = ("partial", "catalogs", "views", "complete")
OUTLINE_STAGE_DIRECTORIES = (
    "00-运维认知与学习准备",
    "01-计算机与服务器基础",
    "02-网络基础",
    "03-实验环境",
    "04-Linux基础",
    "05-Linux系统管理",
    "06-Linux日志体系",
    "07-性能与安全",
    "08-Shell与Python",
    "09-企业基础服务",
    "10-数据服务",
    "11-自动化与协作",
    "12-虚拟化与阿里云",
    "13-Docker容器",
    "14-Kubernetes",
    "15-DevOps与CI-CD",
    "16-企业日志平台",
    "17-监控与可观测性",
    "18-AI-Infra",
    "19-AIOps与MLOps",
    "20-SRE与架构能力",
)
OUTLINE_STAGE_HEADERS = (
    "章节 ID",
    "预定文件",
    "标题",
    "主要目标",
    "type",
    "直接前置",
    "建议投入",
    "就业标签",
    "实践锚点",
)
OUTLINE_STUDY_TIMES = frozenset(
    {"30–60 分钟", "60–90 分钟", "90–120 分钟"}
)
OUTLINE_EMPLOYMENT_LABELS = frozenset({"必须学", "建议学", "就业后补学"})
OUTLINE_ID_RE = re.compile(r"`(?P<value>\d{2}\.\d{2})`")
OUTLINE_STAGE_RE = re.compile(r"`(?P<value>\d{2})`")
OUTLINE_FILENAME_RE = re.compile(
    r"`(?P<value>\d{2}\.\d{2}-[^\s`|/\\]+\.md)`"
)
OUTLINE_TYPE_RE = re.compile(r"`(?P<value>[a-z-]+)`")
OUTLINE_ANCHOR_RE = re.compile(
    r"`(?P<value>CP-(?:0\d|1\d|20)|LAB-L[1-4]|PRJ-0[1-5]-M\d{2})`"
)
OUTLINE_SEPARATOR_RE = re.compile(r":?-{3,}:?")

WAVE_THREE_PLAIN_FILES = (
    "学习路线/README.md",
    "学习路线/00-学习路线导航.md",
    "学习路线/01-完整成长路线.md",
    "学习路线/04-每日每周学习模板.md",
    "技术索引/README.md",
)
WAVE_THREE_TABLES = {
    "学习路线/02-三个月就业路线.md": (
        "周次",
        "主线章节",
        "弹性章节",
        "阶段成果",
        "实践锚点",
    ),
    "学习路线/03-职业发展路线.md": (
        "能力层级",
        "岗位方向",
        "章节 ID",
        "阶段成果",
        "项目锚点",
    ),
    "学习路线/05-知识前置依赖.md": (
        "后学章节",
        "直接前置",
        "关系说明",
    ),
    "技术索引/按技术名称.md": ("技术主词", "别名", "章节 ID"),
    "技术索引/按故障现象.md": (
        "故障现象",
        "机制章节",
        "排查方法章节",
        "未来案例入口",
    ),
    "技术索引/按岗位能力.md": (
        "岗位能力",
        "章节 ID",
        "阶段成果",
        "项目锚点",
    ),
}
PROJECT_VIEW_PATH = "学习路线/06-贯穿项目演进线.md"
PROJECT_VIEW_HEADERS = ("项目", "里程碑", "所需章节", "证据类型")
CHECKPOINT_PATH = "学习路线/阶段检查点/README.md"
CHECKPOINT_HEADERS = ("检查点", "阶段", "所需章节", "实践锚点", "能力结果")
PROJECT_HEADERS = ("里程碑", "能力结果", "所需章节", "证据类型", "未来内容归属")
PROJECT_DIRECTORIES = {
    1: "01-若依传统部署",
    2: "02-Docker容器化改造",
    3: "03-Kubernetes云原生部署",
    4: "04-可观测性建设",
    5: "05-AI推理服务部署",
}
LAB_DIRECTORIES = {
    1: "Level-1-基础实验",
    2: "Level-2-综合实验",
    3: "Level-3-企业实验",
    4: "Level-4-架构实验",
}


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


@dataclass(frozen=True)
class _TableRow:
    cells: tuple[str, ...]
    line: int


@dataclass(frozen=True)
class _ControlledTable:
    path: str
    header_line: int
    rows: tuple[_TableRow, ...]


@dataclass(frozen=True)
class _Chapter:
    chapter_id: str
    stage: int
    filename: str | None
    prerequisites: tuple[str, ...]
    employment: str
    anchors: tuple[str, ...]
    path: str
    line: int


@dataclass
class _OutlineState:
    diagnostics: list[Diagnostic] = field(default_factory=list)
    chapter_entries: list[_Chapter] = field(default_factory=list)
    chapters: dict[str, _Chapter] = field(default_factory=dict)
    catalog_count: int = 0
    dependency_count: int = 0
    view_reference_count: int = 0
    anchor_definitions: dict[str, tuple[str, int]] = field(default_factory=dict)
    anchor_references: list[tuple[str, str, int]] = field(default_factory=list)
    project_mappings: dict[str, set[str]] = field(default_factory=dict)
    project_locations: dict[str, tuple[str, int]] = field(default_factory=dict)
    project_view_records: list[tuple[str, set[str], str, int]] = field(
        default_factory=list
    )


@dataclass(frozen=True)
class _OutlineResult:
    errors: tuple[str, ...]
    catalog_count: int
    chapter_count: int
    dependency_count: int
    view_reference_count: int
    anchor_count: int


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


def _add_outline_error(
    state: _OutlineState, path: str, line: int, rule: str, message: str
) -> None:
    state.diagnostics.append(Diagnostic(path, line, rule, message))


def _read_outline_file(
    root: Path,
    relative: str,
    state: _OutlineState,
    *,
    required: bool,
) -> str | None:
    path = root / relative
    if not path.is_file():
        if required:
            _add_outline_error(state, relative, 0, "OL001", "当前门禁缺少规定文件")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        _add_outline_error(state, relative, 0, "OL001", "规定文件无法以 UTF-8 读取")
        return None


def _split_table_cells(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return tuple(cell.strip() for cell in stripped[1:-1].split("|"))


def _parse_controlled_table(
    lines: list[str],
    relative: str,
    expected_headers: tuple[str, ...],
    state: _OutlineState,
    *,
    start: int = 0,
    end: int | None = None,
    required: bool,
) -> _ControlledTable | None:
    stop = len(lines) if end is None else min(end, len(lines))
    header_index = next(
        (index for index in range(start, stop) if lines[index].lstrip().startswith("|")),
        None,
    )
    if header_index is None:
        if required:
            _add_outline_error(state, relative, 0, "OL001", "当前门禁缺少规定表格")
        return None

    header = _split_table_cells(lines[header_index])
    if header != expected_headers:
        _add_outline_error(
            state,
            relative,
            header_index + 1,
            "OL002",
            "受控表格表头与批准合同不一致",
        )
        return None
    separator_index = header_index + 1
    separator = (
        _split_table_cells(lines[separator_index]) if separator_index < stop else None
    )
    if (
        separator is None
        or len(separator) != len(expected_headers)
        or any(OUTLINE_SEPARATOR_RE.fullmatch(cell) is None for cell in separator)
    ):
        _add_outline_error(
            state,
            relative,
            min(separator_index + 1, len(lines) or 1),
            "OL002",
            "受控表格分隔行非法",
        )
        return None

    rows: list[_TableRow] = []
    index = separator_index + 1
    while index < stop and lines[index].lstrip().startswith("|"):
        cells = _split_table_cells(lines[index])
        if cells is None or len(cells) != len(expected_headers):
            _add_outline_error(
                state,
                relative,
                index + 1,
                "OL002",
                "受控表格数据行列数或边界非法",
            )
        else:
            rows.append(_TableRow(cells, index + 1))
        index += 1
    if not rows:
        _add_outline_error(
            state,
            relative,
            header_index + 1,
            "OL002",
            "受控表格至少需要一行数据",
        )
        return None
    return _ControlledTable(relative, header_index + 1, tuple(rows))


def _load_controlled_table(
    root: Path,
    relative: str,
    expected_headers: tuple[str, ...],
    state: _OutlineState,
    *,
    required: bool,
) -> _ControlledTable | None:
    text = _read_outline_file(root, relative, state, required=required)
    if text is None:
        return None
    lines = text.splitlines()
    return _parse_controlled_table(
        lines, relative, expected_headers, state, required=required
    )


def _parse_controlled_list(
    value: str, pattern: re.Pattern[str]
) -> tuple[str, ...] | None:
    if value == "—":
        return ()
    parts = value.split(", ")
    if not parts or ", ".join(parts) != value:
        return None
    parsed: list[str] = []
    for part in parts:
        match = pattern.fullmatch(part)
        if match is None:
            return None
        parsed.append(match.group("value"))
    return tuple(parsed)


def _chapter_order(chapter_id: str) -> tuple[int, int]:
    stage, chapter = chapter_id.split(".", 1)
    return int(stage), int(chapter)


def _parse_stage_table(
    table: _ControlledTable, stage: int, state: _OutlineState
) -> None:
    state.catalog_count += 1
    for position, row in enumerate(table.rows, start=1):
        cells = row.cells
        identifier_match = OUTLINE_ID_RE.fullmatch(cells[0])
        chapter_id = identifier_match.group("value") if identifier_match else None
        if chapter_id is None:
            _add_outline_error(
                state, table.path, row.line, "OL003", "章节 ID 必须为反引号包裹的 NN.CC"
            )
        else:
            identifier_stage, identifier_chapter = _chapter_order(chapter_id)
            if identifier_stage != stage:
                _add_outline_error(
                    state,
                    table.path,
                    row.line,
                    "OL003",
                    f"章节 ID {chapter_id} 与阶段 {stage:02d} 不一致",
                )
            if identifier_chapter != position:
                _add_outline_error(
                    state,
                    table.path,
                    row.line,
                    "OL003",
                    f"阶段内章节序号应连续为 {stage:02d}.{position:02d}",
                )

        filename_match = OUTLINE_FILENAME_RE.fullmatch(cells[1])
        filename = filename_match.group("value") if filename_match else None
        if filename is None:
            _add_outline_error(
                state,
                table.path,
                row.line,
                "OL004",
                "预定文件必须为无空格的反引号 NN.CC-名称.md",
            )
        elif chapter_id is not None and not filename.startswith(chapter_id + "-"):
            _add_outline_error(
                state,
                table.path,
                row.line,
                "OL004",
                f"预定文件与章节 ID {chapter_id} 不对齐",
            )

        if not cells[2] or re.search(r"<br\s*/?>", cells[2], re.IGNORECASE):
            _add_outline_error(state, table.path, row.line, "OL005", "标题必须为单行非空文本")
        if not cells[3] or re.search(r"<br\s*/?>", cells[3], re.IGNORECASE):
            _add_outline_error(
                state, table.path, row.line, "OL005", "主要目标必须为单行非空文本"
            )
        type_match = OUTLINE_TYPE_RE.fullmatch(cells[4])
        if type_match is None or type_match.group("value") not in ALLOWED_TYPES:
            _add_outline_error(state, table.path, row.line, "OL005", "type 不在批准枚举中")
        if cells[6] not in OUTLINE_STUDY_TIMES:
            _add_outline_error(state, table.path, row.line, "OL005", "建议投入不在批准枚举中")
        if cells[7] not in OUTLINE_EMPLOYMENT_LABELS:
            _add_outline_error(state, table.path, row.line, "OL005", "就业标签不在批准枚举中")

        prerequisites = _parse_controlled_list(cells[5], OUTLINE_ID_RE)
        if prerequisites is None:
            _add_outline_error(
                state,
                table.path,
                row.line,
                "OL002",
                "直接前置必须为 — 或逗号加空格分隔的反引号章节 ID",
            )
            prerequisites = ()
        elif len(set(prerequisites)) != len(prerequisites):
            _add_outline_error(state, table.path, row.line, "OL006", "直接前置包含重复章节 ID")

        anchors = _parse_controlled_list(cells[8], OUTLINE_ANCHOR_RE)
        if anchors is None:
            _add_outline_error(
                state,
                table.path,
                row.line,
                "OL010",
                "实践锚点格式不符合 CP、LAB 或 PRJ 合同",
            )
            anchors = ()
        elif len(set(anchors)) != len(anchors):
            _add_outline_error(state, table.path, row.line, "OL010", "实践锚点重复")

        if chapter_id is not None:
            chapter = _Chapter(
                chapter_id,
                stage,
                filename,
                prerequisites,
                cells[7],
                anchors,
                table.path,
                row.line,
            )
            state.chapter_entries.append(chapter)
            state.dependency_count += len(prerequisites)
            state.anchor_references.extend(
                (anchor, table.path, row.line) for anchor in anchors
            )


def _load_stage_catalog(
    root: Path, stage: int, state: _OutlineState, *, required: bool
) -> None:
    relative = f"知识库/{OUTLINE_STAGE_DIRECTORIES[stage]}/README.md"
    text = _read_outline_file(root, relative, state, required=required)
    if text is None:
        return
    lines = text.splitlines()
    headings = [index for index, line in enumerate(lines) if line == "## 章节清单"]
    table_like = any(
        (cells := _split_table_cells(line)) is not None
        and bool(cells)
        and cells[0] == "章节 ID"
        for line in lines
    )
    if not headings:
        if required or table_like:
            _add_outline_error(
                state, relative, 0, "OL001", "缺少唯一的 ## 章节清单 标题"
            )
        return
    for duplicate in headings[1:]:
        _add_outline_error(
            state, relative, duplicate + 1, "OL001", "## 章节清单 标题重复"
        )
    heading = headings[0]
    end = next(
        (
            index
            for index in range(heading + 1, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    table = _parse_controlled_table(
        lines,
        relative,
        OUTLINE_STAGE_HEADERS,
        state,
        start=heading + 1,
        end=end,
        required=True,
    )
    if table is not None:
        _parse_stage_table(table, stage, state)


def _catalog_cycles(graph: dict[str, tuple[str, ...]]) -> list[tuple[str, ...]]:
    colors: dict[str, int] = {}
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def visit(chapter_id: str) -> None:
        colors[chapter_id] = 1
        stack.append(chapter_id)
        for prerequisite in sorted(graph.get(chapter_id, ())):
            if prerequisite not in graph:
                continue
            color = colors.get(prerequisite, 0)
            if color == 0:
                visit(prerequisite)
            elif color == 1:
                start = stack.index(prerequisite)
                cycles.add(tuple(sorted(set(stack[start:]))))
        stack.pop()
        colors[chapter_id] = 2

    for chapter_id in sorted(graph):
        if colors.get(chapter_id, 0) == 0:
            visit(chapter_id)
    return sorted(cycles)


def _finalize_catalogs(state: _OutlineState) -> None:
    by_identifier: dict[str, list[_Chapter]] = {}
    by_filename: dict[str, list[_Chapter]] = {}
    for chapter in state.chapter_entries:
        by_identifier.setdefault(chapter.chapter_id, []).append(chapter)
        if chapter.filename is not None:
            by_filename.setdefault(chapter.filename, []).append(chapter)
    for chapter_id, entries in sorted(by_identifier.items()):
        if len(entries) > 1:
            for entry in entries:
                _add_outline_error(
                    state,
                    entry.path,
                    entry.line,
                    "OL003",
                    f"章节 ID {chapter_id} 全局重复",
                )
        state.chapters[chapter_id] = sorted(
            entries, key=lambda item: (item.path, item.line)
        )[0]
    for filename, entries in sorted(by_filename.items()):
        if len(entries) > 1:
            for entry in entries:
                _add_outline_error(
                    state,
                    entry.path,
                    entry.line,
                    "OL004",
                    f"预定文件 {filename} 全局重复",
                )

    graph = {
        chapter_id: chapter.prerequisites
        for chapter_id, chapter in state.chapters.items()
    }
    for chapter in state.chapter_entries:
        for prerequisite in chapter.prerequisites:
            if prerequisite not in state.chapters:
                _add_outline_error(
                    state,
                    chapter.path,
                    chapter.line,
                    "OL006",
                    f"直接前置 {prerequisite} 不存在",
                )
            elif prerequisite == chapter.chapter_id:
                _add_outline_error(
                    state, chapter.path, chapter.line, "OL006", "章节不得依赖自身"
                )
            elif _chapter_order(prerequisite) >= _chapter_order(chapter.chapter_id):
                _add_outline_error(
                    state,
                    chapter.path,
                    chapter.line,
                    "OL006",
                    f"直接前置 {prerequisite} 不是排序更早的章节",
                )

    for cycle in _catalog_cycles(graph):
        location = state.chapters[cycle[0]]
        _add_outline_error(
            state,
            location.path,
            location.line,
            "OL007",
            "章节依赖存在循环：" + " -> ".join(cycle + (cycle[0],)),
        )

    for chapter in sorted(state.chapters.values(), key=lambda item: item.chapter_id):
        if chapter.employment != "必须学":
            continue
        pending = list(chapter.prerequisites)
        seen: set[str] = set()
        while pending:
            prerequisite = pending.pop()
            if prerequisite in seen or prerequisite not in state.chapters:
                continue
            seen.add(prerequisite)
            dependency = state.chapters[prerequisite]
            if dependency.employment == "就业后补学":
                _add_outline_error(
                    state,
                    chapter.path,
                    chapter.line,
                    "OL009",
                    f"必须学章节依赖就业后补学章节 {prerequisite}",
                )
            pending.extend(dependency.prerequisites)


def _require_plain_files(root: Path, paths: tuple[str, ...], state: _OutlineState) -> None:
    for relative in paths:
        _read_outline_file(root, relative, state, required=True)


def _parse_view_chapters(
    value: str,
    path: str,
    line: int,
    state: _OutlineState,
    *,
    allow_empty: bool = True,
) -> tuple[str, ...]:
    chapters = _parse_controlled_list(value, OUTLINE_ID_RE)
    if chapters is None or (not allow_empty and not chapters):
        _add_outline_error(
            state,
            path,
            line,
            "OL002",
            "章节引用必须为 — 或逗号加空格分隔的反引号章节 ID",
        )
        return ()
    state.view_reference_count += len(chapters)
    if len(set(chapters)) != len(chapters):
        _add_outline_error(state, path, line, "OL012", "同一单元格包含重复章节 ID")
    for chapter_id in chapters:
        if chapter_id not in state.chapters:
            _add_outline_error(
                state, path, line, "OL008", f"派生视图引用不存在章节 {chapter_id}"
            )
    return chapters


def _parse_view_anchors(
    value: str, path: str, line: int, state: _OutlineState
) -> tuple[str, ...]:
    anchors = _parse_controlled_list(value, OUTLINE_ANCHOR_RE)
    if anchors is None:
        _add_outline_error(
            state, path, line, "OL010", "派生视图锚点语法不符合批准合同"
        )
        return ()
    state.view_reference_count += len(anchors)
    if len(set(anchors)) != len(anchors):
        _add_outline_error(state, path, line, "OL012", "同一单元格包含重复锚点")
    state.anchor_references.extend((anchor, path, line) for anchor in anchors)
    return anchors


def _require_text(
    value: str, path: str, line: int, state: _OutlineState, field_name: str
) -> None:
    if not value or re.search(r"<br\s*/?>", value, re.IGNORECASE):
        _add_outline_error(
            state, path, line, "OL002", f"{field_name} 必须为单行非空文本"
        )


def _expected_required_closure(state: _OutlineState) -> set[str]:
    closure = {
        chapter_id
        for chapter_id, chapter in state.chapters.items()
        if chapter.employment == "必须学"
    }
    pending = list(closure)
    while pending:
        chapter_id = pending.pop()
        chapter = state.chapters.get(chapter_id)
        if chapter is None:
            continue
        for prerequisite in chapter.prerequisites:
            if prerequisite in state.chapters and prerequisite not in closure:
                closure.add(prerequisite)
                pending.append(prerequisite)
    return closure


def _validate_route_table(
    table: _ControlledTable, state: _OutlineState, *, strict: bool
) -> None:
    weeks: list[int] = []
    mainline: list[tuple[str, int]] = []
    flexible: list[tuple[str, int]] = []
    for position, row in enumerate(table.rows, start=1):
        week_match = re.fullmatch(r"第 ([1-9]|1[0-2]) 周", row.cells[0])
        if week_match is None:
            _add_outline_error(
                state, table.path, row.line, "OL009", "周次必须为第 1 周至第 12 周"
            )
        else:
            week = int(week_match.group(1))
            if week in weeks:
                _add_outline_error(state, table.path, row.line, "OL012", "周次重复")
            weeks.append(week)
            if week != position:
                _add_outline_error(
                    state,
                    table.path,
                    row.line,
                    "OL009",
                    f"周次行顺序应为第 {position} 周",
                )
        main = _parse_view_chapters(row.cells[1], table.path, row.line, state)
        optional = _parse_view_chapters(row.cells[2], table.path, row.line, state)
        mainline.extend((chapter_id, row.line) for chapter_id in main)
        flexible.extend((chapter_id, row.line) for chapter_id in optional)
        _require_text(row.cells[3], table.path, row.line, state, "阶段成果")
        _parse_view_anchors(row.cells[4], table.path, row.line, state)

    main_ids = [chapter_id for chapter_id, _ in mainline]
    flexible_ids = [chapter_id for chapter_id, _ in flexible]
    for chapter_id in sorted(set(main_ids)):
        if main_ids.count(chapter_id) > 1:
            line = next(line for item, line in mainline if item == chapter_id)
            _add_outline_error(
                state, table.path, line, "OL012", f"主线章节 {chapter_id} 重复"
            )
    for chapter_id in sorted(set(flexible_ids)):
        if flexible_ids.count(chapter_id) > 1:
            line = next(line for item, line in flexible if item == chapter_id)
            _add_outline_error(
                state, table.path, line, "OL012", f"弹性章节 {chapter_id} 重复"
            )
    for chapter_id in sorted(set(main_ids) & set(flexible_ids)):
        line = next(line for item, line in flexible if item == chapter_id)
        _add_outline_error(
            state, table.path, line, "OL012", f"章节 {chapter_id} 同时位于主线和弹性集合"
        )
    for chapter_id, line in flexible:
        chapter = state.chapters.get(chapter_id)
        if chapter is not None and chapter.employment != "建议学":
            _add_outline_error(
                state,
                table.path,
                line,
                "OL012",
                f"弹性章节 {chapter_id} 不是建议学",
            )
    for chapter_id, line in mainline:
        chapter = state.chapters.get(chapter_id)
        if chapter is not None and chapter.employment == "就业后补学":
            _add_outline_error(
                state,
                table.path,
                line,
                "OL009",
                f"就业后补学章节 {chapter_id} 不得进入主线",
            )

    positions: dict[str, int] = {}
    for index, (chapter_id, _) in enumerate(mainline):
        positions.setdefault(chapter_id, index)
    for chapter_id, line in mainline:
        chapter = state.chapters.get(chapter_id)
        if chapter is None:
            continue
        for prerequisite in chapter.prerequisites:
            if prerequisite not in positions or positions[prerequisite] >= positions[chapter_id]:
                _add_outline_error(
                    state,
                    table.path,
                    line,
                    "OL008",
                    f"主线章节 {chapter_id} 未在前置 {prerequisite} 之后出现",
                )

    if strict:
        expected_weeks = set(range(1, 13))
        if set(weeks) != expected_weeks or len(weeks) != 12:
            _add_outline_error(
                state,
                table.path,
                table.header_line,
                "OL009",
                "三个月路线必须恰好包含第 1 周至第 12 周",
            )
        expected_main = _expected_required_closure(state)
        actual_main = set(main_ids)
        if actual_main != expected_main:
            missing = ", ".join(sorted(expected_main - actual_main)) or "无"
            extra = ", ".join(sorted(actual_main - expected_main)) or "无"
            _add_outline_error(
                state,
                table.path,
                table.header_line,
                "OL009",
                f"十二周主线与必须学前置闭包不一致；缺少：{missing}；越界：{extra}",
            )


def _validate_career_table(table: _ControlledTable, state: _OutlineState) -> None:
    keys: set[tuple[str, str]] = set()
    for row in table.rows:
        _require_text(row.cells[0], table.path, row.line, state, "能力层级")
        _require_text(row.cells[1], table.path, row.line, state, "岗位方向")
        key = (row.cells[0], row.cells[1])
        if key in keys:
            _add_outline_error(state, table.path, row.line, "OL012", "职业路线能力项重复")
        keys.add(key)
        _parse_view_chapters(row.cells[2], table.path, row.line, state, allow_empty=False)
        _require_text(row.cells[3], table.path, row.line, state, "阶段成果")
        _parse_view_anchors(row.cells[4], table.path, row.line, state)


def _validate_dependency_table(table: _ControlledTable, state: _OutlineState) -> None:
    seen: set[str] = set()
    for row in table.rows:
        later = _parse_view_chapters(
            row.cells[0], table.path, row.line, state, allow_empty=False
        )
        prerequisites = _parse_view_chapters(
            row.cells[1], table.path, row.line, state, allow_empty=False
        )
        _require_text(row.cells[2], table.path, row.line, state, "关系说明")
        if len(later) != 1:
            _add_outline_error(
                state, table.path, row.line, "OL002", "后学章节单元格只能包含一个章节 ID"
            )
            continue
        chapter_id = later[0]
        if chapter_id in seen:
            _add_outline_error(state, table.path, row.line, "OL012", "后学章节重复")
        seen.add(chapter_id)
        chapter = state.chapters.get(chapter_id)
        if chapter is None:
            continue
        for prerequisite in prerequisites:
            if prerequisite not in chapter.prerequisites:
                _add_outline_error(
                    state,
                    table.path,
                    row.line,
                    "OL008",
                    f"依赖视图中的 {prerequisite} 不是 {chapter_id} 的直接前置",
                )


def _validate_technology_table(table: _ControlledTable, state: _OutlineState) -> None:
    keys: set[str] = set()
    for row in table.rows:
        _require_text(row.cells[0], table.path, row.line, state, "技术主词")
        if row.cells[0] in keys:
            _add_outline_error(state, table.path, row.line, "OL012", "技术主词重复")
        keys.add(row.cells[0])
        if not row.cells[1]:
            _add_outline_error(state, table.path, row.line, "OL002", "别名不得为空")
        _parse_view_chapters(row.cells[2], table.path, row.line, state, allow_empty=False)


def _validate_incident_table(table: _ControlledTable, state: _OutlineState) -> None:
    keys: set[str] = set()
    for row in table.rows:
        _require_text(row.cells[0], table.path, row.line, state, "故障现象")
        if row.cells[0] in keys:
            _add_outline_error(state, table.path, row.line, "OL012", "故障现象重复")
        keys.add(row.cells[0])
        _parse_view_chapters(row.cells[1], table.path, row.line, state, allow_empty=False)
        _parse_view_chapters(row.cells[2], table.path, row.line, state, allow_empty=False)
        if not row.cells[3]:
            _add_outline_error(state, table.path, row.line, "OL002", "未来案例入口不得为空")


def _validate_role_table(table: _ControlledTable, state: _OutlineState) -> None:
    keys: set[str] = set()
    for row in table.rows:
        _require_text(row.cells[0], table.path, row.line, state, "岗位能力")
        if row.cells[0] in keys:
            _add_outline_error(state, table.path, row.line, "OL012", "岗位能力重复")
        keys.add(row.cells[0])
        _parse_view_chapters(row.cells[1], table.path, row.line, state, allow_empty=False)
        _require_text(row.cells[2], table.path, row.line, state, "阶段成果")
        _parse_view_anchors(row.cells[3], table.path, row.line, state)


def _validate_wave_three_views(
    root: Path, state: _OutlineState, *, required: bool, strict: bool
) -> None:
    if required:
        _require_plain_files(root, WAVE_THREE_PLAIN_FILES, state)
    for relative, headers in WAVE_THREE_TABLES.items():
        table = _load_controlled_table(
            root, relative, headers, state, required=required
        )
        if table is None:
            continue
        if relative == "学习路线/02-三个月就业路线.md":
            _validate_route_table(table, state, strict=strict)
        elif relative == "学习路线/03-职业发展路线.md":
            _validate_career_table(table, state)
        elif relative == "学习路线/05-知识前置依赖.md":
            _validate_dependency_table(table, state)
        elif relative == "技术索引/按技术名称.md":
            _validate_technology_table(table, state)
        elif relative == "技术索引/按故障现象.md":
            _validate_incident_table(table, state)
        elif relative == "技术索引/按岗位能力.md":
            _validate_role_table(table, state)


def _record_anchor_definition(
    anchor: str, path: str, line: int, state: _OutlineState
) -> None:
    if anchor in state.anchor_definitions:
        _add_outline_error(state, path, line, "OL010", f"锚点 {anchor} 重复定义")
        return
    state.anchor_definitions[anchor] = (path, line)


def _validate_project_view(table: _ControlledTable, state: _OutlineState) -> None:
    seen: set[str] = set()
    for row in table.rows:
        _require_text(row.cells[0], table.path, row.line, state, "项目")
        anchors = _parse_controlled_list(row.cells[1], OUTLINE_ANCHOR_RE)
        if anchors is None or len(anchors) != 1 or not anchors[0].startswith("PRJ-"):
            _add_outline_error(
                state,
                table.path,
                row.line,
                "OL010",
                "项目演进视图的里程碑必须是单个 PRJ-NN-MCC",
            )
            milestone = None
        else:
            milestone = anchors[0]
            state.view_reference_count += 1
            state.anchor_references.append((milestone, table.path, row.line))
            if milestone in seen:
                _add_outline_error(
                    state, table.path, row.line, "OL012", "项目演进视图里程碑重复"
                )
            seen.add(milestone)
        chapters = set(
            _parse_view_chapters(
                row.cells[2], table.path, row.line, state, allow_empty=False
            )
        )
        _require_text(row.cells[3], table.path, row.line, state, "证据类型")
        if milestone is not None:
            state.project_view_records.append(
                (milestone, chapters, table.path, row.line)
            )


def _validate_checkpoint_table(
    table: _ControlledTable, state: _OutlineState, *, require_all: bool
) -> None:
    for position, row in enumerate(table.rows):
        anchor_match = OUTLINE_ANCHOR_RE.fullmatch(row.cells[0])
        checkpoint = (
            anchor_match.group("value")
            if anchor_match is not None
            and anchor_match.group("value").startswith("CP-")
            else None
        )
        if checkpoint is None:
            _add_outline_error(
                state, table.path, row.line, "OL010", "检查点必须为反引号 CP-NN"
            )
        stage_match = OUTLINE_STAGE_RE.fullmatch(row.cells[1])
        stage_value = stage_match.group("value") if stage_match else None
        if stage_value is None or not 0 <= int(stage_value) <= 20:
            _add_outline_error(
                state, table.path, row.line, "OL010", "检查点阶段必须为反引号 00 至 20"
            )
        if checkpoint is not None and stage_value is not None:
            if checkpoint != f"CP-{stage_value}":
                _add_outline_error(
                    state, table.path, row.line, "OL010", "检查点 ID 与阶段不对齐"
                )
            expected = f"{position:02d}"
            if checkpoint != f"CP-{expected}" or stage_value != expected:
                _add_outline_error(
                    state,
                    table.path,
                    row.line,
                    "OL010",
                    f"检查点定义应按 CP-{expected} 连续排序",
                )
        _parse_view_chapters(
            row.cells[2], table.path, row.line, state, allow_empty=False
        )
        _parse_view_anchors(row.cells[3], table.path, row.line, state)
        _require_text(row.cells[4], table.path, row.line, state, "能力结果")
        if checkpoint is not None:
            _record_anchor_definition(checkpoint, table.path, row.line, state)
    if require_all:
        actual = {
            anchor
            for anchor in state.anchor_definitions
            if anchor.startswith("CP-")
        }
        for missing in sorted({f"CP-{stage:02d}" for stage in range(21)} - actual):
            _add_outline_error(
                state, table.path, 0, "OL010", f"缺少检查点定义 {missing}"
            )


def _validate_labs(root: Path, state: _OutlineState) -> None:
    _read_outline_file(root, "实验手册/README.md", state, required=True)
    for level, directory in LAB_DIRECTORIES.items():
        relative = f"实验手册/{directory}/README.md"
        text = _read_outline_file(root, relative, state, required=True)
        if text is None:
            continue
        occurrences = [
            (match.group(1), _line_number(text, match.start()))
            for match in re.finditer(r"`(LAB-L[1-4])`", text)
        ]
        expected = f"LAB-L{level}"
        expected_lines = [line for anchor, line in occurrences if anchor == expected]
        if not expected_lines:
            _add_outline_error(
                state, relative, 0, "OL010", f"对应 Level README 缺少定义 {expected}"
            )
        else:
            _record_anchor_definition(expected, relative, expected_lines[0], state)
            for line in expected_lines[1:]:
                _add_outline_error(
                    state, relative, line, "OL010", f"锚点 {expected} 重复定义"
                )
        for anchor, line in occurrences:
            if anchor != expected:
                _add_outline_error(
                    state,
                    relative,
                    line,
                    "OL010",
                    f"锚点 {anchor} 定义在错误的 Level README",
                )


def _validate_project_table(
    table: _ControlledTable, project: int, state: _OutlineState
) -> None:
    for position, row in enumerate(table.rows, start=1):
        anchor_match = OUTLINE_ANCHOR_RE.fullmatch(row.cells[0])
        milestone = (
            anchor_match.group("value")
            if anchor_match is not None
            and anchor_match.group("value").startswith("PRJ-")
            else None
        )
        expected = f"PRJ-{project:02d}-M{position:02d}"
        if milestone is None:
            _add_outline_error(
                state, table.path, row.line, "OL010", "项目里程碑必须为反引号 PRJ-NN-MCC"
            )
        else:
            if milestone != expected:
                _add_outline_error(
                    state,
                    table.path,
                    row.line,
                    "OL010",
                    f"项目里程碑应连续且属于当前项目；预期 {expected}",
                )
            _record_anchor_definition(milestone, table.path, row.line, state)
        _require_text(row.cells[1], table.path, row.line, state, "能力结果")
        chapters = set(
            _parse_view_chapters(
                row.cells[2], table.path, row.line, state, allow_empty=False
            )
        )
        _require_text(row.cells[3], table.path, row.line, state, "证据类型")
        _require_text(row.cells[4], table.path, row.line, state, "未来内容归属")
        if milestone is not None:
            state.project_mappings[milestone] = chapters
            state.project_locations[milestone] = (table.path, row.line)


def _validate_projects(root: Path, state: _OutlineState, *, required: bool) -> None:
    if required:
        _read_outline_file(root, "项目实战/README.md", state, required=True)
    for project, directory in PROJECT_DIRECTORIES.items():
        relative = f"项目实战/{directory}/README.md"
        table = _load_controlled_table(
            root, relative, PROJECT_HEADERS, state, required=required
        )
        if table is not None:
            _validate_project_table(table, project, state)


def _validate_anchor_and_project_closure(state: _OutlineState) -> None:
    for anchor, path, line in state.anchor_references:
        if anchor not in state.anchor_definitions:
            _add_outline_error(
                state, path, line, "OL010", f"引用的实践锚点 {anchor} 不存在"
            )

    for milestone, chapters in sorted(state.project_mappings.items()):
        path, line = state.project_locations[milestone]
        for chapter_id in sorted(chapters):
            chapter = state.chapters.get(chapter_id)
            if chapter is not None and milestone not in chapter.anchors:
                _add_outline_error(
                    state,
                    path,
                    line,
                    "OL011",
                    f"项目里程碑 {milestone} 列出章节 {chapter_id}，但章节未反向引用",
                )
    for chapter in sorted(state.chapters.values(), key=lambda item: item.chapter_id):
        for milestone in sorted(
            anchor for anchor in chapter.anchors if anchor.startswith("PRJ-")
        ):
            if chapter.chapter_id not in state.project_mappings.get(milestone, set()):
                _add_outline_error(
                    state,
                    chapter.path,
                    chapter.line,
                    "OL011",
                    f"章节引用 {milestone}，但项目未列回章节 {chapter.chapter_id}",
                )
    view_milestones = {
        milestone for milestone, _, _, _ in state.project_view_records
    }
    for milestone in sorted(state.project_mappings.keys() - view_milestones):
        path, line = state.project_locations[milestone]
        _add_outline_error(
            state,
            path,
            line,
            "OL011",
            f"项目里程碑 {milestone} 未出现在贯穿项目视图",
        )
    for milestone, chapters, path, line in state.project_view_records:
        mapping = state.project_mappings.get(milestone)
        if mapping is not None and chapters != mapping:
            _add_outline_error(
                state,
                path,
                line,
                "OL011",
                f"贯穿项目视图与里程碑 {milestone} 的章节集合不一致",
            )


def _validate_partial_auxiliary_tables(root: Path, state: _OutlineState) -> None:
    project_view = _load_controlled_table(
        root,
        PROJECT_VIEW_PATH,
        PROJECT_VIEW_HEADERS,
        state,
        required=False,
    )
    if project_view is not None:
        _validate_project_view(project_view, state)
    checkpoint = _load_controlled_table(
        root, CHECKPOINT_PATH, CHECKPOINT_HEADERS, state, required=False
    )
    if checkpoint is not None:
        _validate_checkpoint_table(checkpoint, state, require_all=False)
    _validate_projects(root, state, required=False)


def _validate_complete(root: Path, state: _OutlineState) -> None:
    project_view = _load_controlled_table(
        root,
        PROJECT_VIEW_PATH,
        PROJECT_VIEW_HEADERS,
        state,
        required=True,
    )
    if project_view is not None:
        _validate_project_view(project_view, state)
    checkpoint = _load_controlled_table(
        root, CHECKPOINT_PATH, CHECKPOINT_HEADERS, state, required=True
    )
    if checkpoint is not None:
        _validate_checkpoint_table(checkpoint, state, require_all=True)
    _validate_labs(root, state)
    _validate_projects(root, state, required=True)
    _validate_anchor_and_project_closure(state)


def _aggregate_outline(root: Path, gate: str) -> _OutlineResult:
    if gate not in OUTLINE_GATES:
        raise ValueError(f"不支持的大纲门禁：{gate}")
    state = _OutlineState()
    try:
        root = root.resolve(strict=False)
        if not root.exists() or not root.is_dir():
            _add_outline_error(state, ".", 0, "OL001", "仓库根目录不存在或不是目录")
            ordered = tuple(item.render() for item in sorted(set(state.diagnostics)))
            return _OutlineResult(ordered, 0, 0, 0, 0, 0)
    except (OSError, ValueError):
        _add_outline_error(state, ".", 0, "OL001", "仓库根路径解析失败")
        ordered = tuple(item.render() for item in sorted(set(state.diagnostics)))
        return _OutlineResult(ordered, 0, 0, 0, 0, 0)

    catalogs_required = gate != "partial"
    for stage in range(21):
        _load_stage_catalog(root, stage, state, required=catalogs_required)
    _finalize_catalogs(state)

    if gate == "partial":
        _validate_wave_three_views(root, state, required=False, strict=False)
        _validate_partial_auxiliary_tables(root, state)
    elif gate in {"views", "complete"}:
        _validate_wave_three_views(root, state, required=True, strict=True)
        if gate == "complete":
            _validate_complete(root, state)

    ordered = tuple(
        item.render() for item in sorted(set(state.diagnostics))
    )
    return _OutlineResult(
        ordered,
        state.catalog_count,
        len(state.chapters),
        state.dependency_count,
        state.view_reference_count,
        len(state.anchor_definitions),
    )


def validate_outline(root: Path, gate: str) -> list[str]:
    return list(_aggregate_outline(root, gate).errors)


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
    parser.add_argument(
        "--outline-gate",
        choices=OUTLINE_GATES,
        help=(
            "启用分级大纲门禁：partial 校验已存在受控表格；catalogs 要求 00–20 "
            "阶段清单；views 增加路线与索引；complete 增加检查点、实验和项目闭合"
        ),
    )
    args = parser.parse_args(argv)
    result = _aggregate_repository(Path(args.root))
    outline_result = (
        _aggregate_outline(Path(args.root), args.outline_gate)
        if args.outline_gate is not None
        else None
    )
    errors = list(result.errors)
    if outline_result is not None:
        errors.extend(outline_result.errors)
    errors = sorted(set(errors), key=_error_sort_key)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"校验失败：{len(errors)} 个错误", file=sys.stderr)
        return 1
    print(
        f"校验通过：Markdown {result.markdown_count}，知识章节 {result.knowledge_count}，"
        f"本地链接 {result.local_link_count}；错误 0"
    )
    if outline_result is not None:
        print(
            f"大纲门禁通过：级别 {args.outline_gate}，阶段清单 {outline_result.catalog_count}，"
            f"章节 {outline_result.chapter_count}，依赖 {outline_result.dependency_count}，"
            f"视图引用 {outline_result.view_reference_count}，锚点 {outline_result.anchor_count}；错误 0"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
