from __future__ import annotations

import ast
import contextlib
import hashlib
import importlib.util
import inspect
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载校验模块：{MODULE_PATH}")
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def valid_article(chapter: str = "01.01", **overrides: str) -> str:
    values = {
        "title": "测试章节",
        "chapter": chapter,
        "stage": "01-基础",
        "type": "concept",
        "difficulty": "初级",
        "study_time": "1~2 小时",
        "practice_level": "none",
        "status": "draft",
        "last_updated": "2026-07-11",
    }
    values.update(overrides)
    return f'''---
title: "{values["title"]}"
chapter: "{values["chapter"]}"
stage: "{values["stage"]}"
type: "{values["type"]}"
difficulty: "{values["difficulty"]}"
prerequisites:
  - "无"
objectives:
  - "解释测试目标"
study_time: "{values["study_time"]}"
practice_level: "{values["practice_level"]}"
keywords:
  - "test"
versions: {{}}
status: "{values["status"]}"
last_updated: "{values["last_updated"]}"
---

# 测试章节
'''


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

STAGE_HEADERS = (
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


def controlled_table(headers: tuple[str, ...], rows: list[list[str]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    separator = "|" + "|".join("---" for _ in headers) + "|"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows)
    return f"{header}\n{separator}\n{body}\n"


class RepositoryFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_text(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def assert_has_rule(self, errors: list[str], rule: str) -> None:
        self.assertTrue(
            any(f" {rule} " in error for error in errors),
            f"未发现规则 {rule}，实际诊断：{errors}",
        )


class FrontMatterTests(RepositoryFixture):
    def test_extract_valid_front_matter(self) -> None:
        text = valid_article()
        values = validator.extract_front_matter(text)
        self.assertEqual(values["chapter"], "01.01")
        self.assertEqual(values["status"], "draft")
        self.assertEqual(
            validator.validate_front_matter(Path("知识库/01-基础/01.01-测试.md"), text),
            [],
        )

    def test_front_matter_required_for_knowledge_article(self) -> None:
        errors = validator.validate_front_matter(
            Path("知识库/01-基础/01.01-测试.md"), "# 没有元数据\n"
        )
        self.assert_has_rule(errors, "FM001")
        self.assertIn(":1:", errors[0])

    def test_front_matter_requires_closing_delimiter(self) -> None:
        text = valid_article().rsplit("---", 1)[0]
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assert_has_rule(errors, "FM001")

    def test_front_matter_reports_missing_key(self) -> None:
        text = valid_article().replace('status: "draft"\n', "")
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assert_has_rule(errors, "FM002")
        self.assertTrue(any("status" in error for error in errors))

    def test_front_matter_reports_duplicate_key(self) -> None:
        text = valid_article().replace(
            'title: "测试章节"\n', 'title: "测试章节"\ntitle: "重复标题"\n'
        )
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assert_has_rule(errors, "FM003")
        self.assertTrue(any(":3:" in error for error in errors))

    def test_front_matter_rejects_empty_values(self) -> None:
        text = valid_article().replace('title: "测试章节"', "title:").replace(
            'prerequisites:\n  - "无"', "prerequisites: []"
        )
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assertGreaterEqual(sum(" FM004 " in error for error in errors), 2)

    def test_front_matter_rejects_invalid_type(self) -> None:
        errors = validator.validate_front_matter(
            Path("知识库/文章.md"), valid_article(type="tutorial")
        )
        self.assert_has_rule(errors, "FM005")

    def test_front_matter_rejects_invalid_status(self) -> None:
        errors = validator.validate_front_matter(
            Path("知识库/文章.md"), valid_article(status="done")
        )
        self.assert_has_rule(errors, "FM006")

    def test_front_matter_rejects_invalid_date(self) -> None:
        errors = validator.validate_front_matter(
            Path("知识库/文章.md"), valid_article(last_updated="2026-02-30")
        )
        self.assert_has_rule(errors, "FM007")

    def test_front_matter_accepts_lists_and_versions_map(self) -> None:
        text = valid_article().replace(
            "versions: {}", 'versions:\n  rocky_linux: "9.8"\n  python: "3.11"'
        )
        values = validator.extract_front_matter(text)
        self.assertIn('rocky_linux: "9.8"', values["versions"])
        self.assertEqual(
            validator.validate_front_matter(Path("知识库/文章.md"), text), []
        )

    def test_front_matter_rejects_unsupported_yaml(self) -> None:
        text = valid_article().replace('title: "测试章节"', "title: |\n  多行标题")
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assert_has_rule(errors, "FM008")

    def test_front_matter_rejects_unclosed_double_quoted_scalar(self) -> None:
        text = valid_article().replace('title: "测试章节"', 'title: "未闭合')
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assertTrue(any(error.startswith("知识库/文章.md:2: FM008") for error in errors))

    def test_front_matter_rejects_unclosed_single_quoted_scalar(self) -> None:
        text = valid_article().replace('title: "测试章节"', "title: '未闭合")
        errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
        self.assertTrue(any(error.startswith("知识库/文章.md:2: FM008") for error in errors))

    def test_front_matter_rejects_mismatched_or_trailing_quoted_scalar(self) -> None:
        cases = {
            "mismatched_top_level": (
                valid_article().replace('title: "测试章节"', 'title: "错配\''),
                2,
            ),
            "trailing_top_level": (
                valid_article().replace('title: "测试章节"', 'title: "闭合" trailing'),
                2,
            ),
            "unclosed_list_item": (
                valid_article().replace('  - "无"', '  - "未闭合', 1),
                8,
            ),
            "trailing_versions_value": (
                valid_article().replace(
                    "versions: {}", 'versions:\n  rocky_linux: "9.8" trailing'
                ),
                16,
            ),
        }
        for name, (text, line) in cases.items():
            with self.subTest(name=name):
                errors = validator.validate_front_matter(Path("知识库/文章.md"), text)
                self.assertTrue(
                    any(
                        error.startswith(f"知识库/文章.md:{line}: FM008")
                        for error in errors
                    ),
                    errors,
                )

    def test_front_matter_accepts_controlled_scalar_forms(self) -> None:
        text = (
            valid_article()
            .replace('title: "测试章节"', "title: 测试章节")
            .replace('chapter: "01.01"', "chapter: '01.01'")
            .replace('  - "无"', "  - '无'", 1)
            .replace(
                "versions: {}", 'versions:\n  rocky_linux: "9.8"'
            )
        )
        self.assertEqual(
            validator.validate_front_matter(Path("知识库/文章.md"), text), []
        )

    def test_duplicate_chapter_reports_both_files(self) -> None:
        self.write_text("知识库/01-基础/A.md", valid_article("01.01"))
        self.write_text("知识库/02-网络/B.md", valid_article("01.01"))
        errors = validator.validate_repository(self.root)
        duplicates = [error for error in errors if " CH001 " in error]
        self.assertEqual(len(duplicates), 2)
        self.assertTrue(any(error.startswith("知识库/01-基础/A.md:") for error in duplicates))
        self.assertTrue(any(error.startswith("知识库/02-网络/B.md:") for error in duplicates))


class LinkTests(RepositoryFixture):
    def test_valid_relative_links_and_images(self) -> None:
        source = self.write_text(
            "文档/入口.md", "[目标](目标.md)\n![图片](../图片/示意图.png)\n"
        )
        self.write_text("文档/目标.md", "# 目标\n")
        self.write_text("图片/示意图.png", "not-a-real-image")
        self.assertEqual(validator.validate_local_links(source, source.read_text("utf-8"), self.root), [])

    def test_external_mail_and_anchor_are_ignored(self) -> None:
        source = self.write_text(
            "入口.md",
            "[网页](https://example.com/a) [普通](http://example.com) "
            "[邮件](mailto:test@example.com) [页内](#part)\n",
        )
        self.assertEqual(validator.validate_local_links(source, source.read_text("utf-8"), self.root), [])

    def test_file_anchor_checks_file_only(self) -> None:
        source = self.write_text("入口.md", "[目标](目标.md#不存在的锚点)\n")
        self.write_text("目标.md", "# 目标\n")
        self.assertEqual(validator.validate_local_links(source, source.read_text("utf-8"), self.root), [])

    def test_broken_relative_link(self) -> None:
        source = self.write_text("入口.md", "[缺失](missing.md)\n")
        errors = validator.validate_local_links(source, source.read_text("utf-8"), self.root)
        self.assert_has_rule(errors, "LINK001")
        self.assertIn(":1:", errors[0])

    def test_link_cannot_escape_root(self) -> None:
        source = self.write_text("文档/入口.md", "[越界](../../outside.md)\n")
        errors = validator.validate_local_links(source, source.read_text("utf-8"), self.root)
        self.assert_has_rule(errors, "LINK002")

    def test_absolute_and_drive_links_are_rejected(self) -> None:
        source = self.write_text("入口.md", "[绝对](/etc/passwd)\n[盘符](C:/secret.txt)\n")
        errors = validator.validate_local_links(source, source.read_text("utf-8"), self.root)
        self.assertEqual(sum(" LINK003 " in error for error in errors), 2)

    def test_case_mismatch_is_detected(self) -> None:
        source = self.write_text("文档/入口.md", "[目标](Target.md)\n")
        self.write_text("文档/target.md", "# target\n")
        errors = validator.validate_local_links(source, source.read_text("utf-8"), self.root)
        self.assert_has_rule(errors, "LINK004")

    def test_link_in_fence_is_ignored(self) -> None:
        source = self.write_text(
            "入口.md", "```markdown\n[缺失](missing.md)\n```\n~~~\n[x](also-missing.md)\n~~~\n"
        )
        self.assertEqual(validator.validate_local_links(source, source.read_text("utf-8"), self.root), [])

    def test_link_in_inline_code_is_ignored(self) -> None:
        source = self.write_text(
            "入口.md", "语法示例：`[文本](目标)` 与 ``![图片](目标)``。\n"
        )
        self.assertEqual(
            validator.validate_local_links(source, source.read_text("utf-8"), self.root), []
        )

    def test_reference_and_angle_bracket_links(self) -> None:
        source = self.write_text(
            "入口.md",
            "[行内](<资料/文件 名.md>)\n[引用][guide]\n\n[guide]: <资料/文件 名.md>\n",
        )
        self.write_text("资料/文件 名.md", "# 文件\n")
        self.assertEqual(validator.validate_local_links(source, source.read_text("utf-8"), self.root), [])


class PlaceholderAndSensitiveTests(RepositoryFixture):
    def test_formal_content_placeholder_is_rejected(self) -> None:
        path = Path("学习路线/路线.md")
        errors = validator.validate_placeholders(path, "TODO\n这里需要待补充，后续完善。\n")
        self.assert_has_rule(errors, "PH001")
        self.assert_has_rule(errors, "PH002")

    def test_placeholder_in_fence_is_ignored(self) -> None:
        text = "```text\nTODO\n待补充\n<必填：示例>\n```\n"
        self.assertEqual(validator.validate_placeholders(Path("知识库/文章.md"), text), [])

    def test_placeholder_excluded_directories(self) -> None:
        for path in (Path("模板/README.md"), Path("项目管理/任务包.md"), Path("README.md")):
            with self.subTest(path=path):
                self.assertEqual(validator.validate_placeholders(path, "TODO <必填：说明>\n"), [])

    def test_template_marker_in_formal_content_is_rejected(self) -> None:
        errors = validator.validate_placeholders(
            Path("实验手册/实验.md"), "# 实验\n<必填：填写目标>\n<替换实际值>\n"
        )
        self.assert_has_rule(errors, "PH003")
        self.assert_has_rule(errors, "PH004")

    def test_synthetic_secret_is_rejected_and_redacted(self) -> None:
        synthetic_value = "".join(("AK", "IA", "EXAMPLE", "VALUE1234"))
        text = f"access_key = {synthetic_value}\n"
        errors = validator.validate_sensitive_information(Path("说明.md"), text)
        self.assertTrue(any(" SEC" in error for error in errors))
        self.assertFalse(any(synthetic_value in error for error in errors))


class RepositoryAndCliTests(RepositoryFixture):
    def test_chinese_paths_and_utf8(self) -> None:
        self.write_text("技术索引/入口.md", "[中文目标](../参考资料/中文资料.md)\n")
        self.write_text("参考资料/中文资料.md", "# 中文内容：你好，世界\n")
        self.assertEqual(validator.validate_repository(self.root), [])

    def test_invalid_utf8_reports_io_error(self) -> None:
        path = self.root / "坏文件.md"
        path.write_bytes(b"\xff\xfe\xfa")
        errors = validator.validate_repository(self.root)
        self.assert_has_rule(errors, "IO002")
        self.assertTrue(errors[0].startswith("坏文件.md:0:"))

    def test_errors_are_sorted_deterministically(self) -> None:
        self.write_text("学习路线/A.md", "# A\nTODO\n" + "\n" * 7 + "TODO\n")
        first = validator.validate_repository(self.root)
        second = validator.validate_repository(self.root)
        self.assertEqual(first, second)
        self.assertEqual(
            [error.split(": PH001", 1)[0] for error in first],
            ["学习路线/A.md:2", "学习路线/A.md:10"],
        )

    def test_main_returns_zero_on_success(self) -> None:
        self.write_text("README.md", "# 合法仓库\n")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validator.main([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("校验通过", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_main_returns_one_on_failure(self) -> None:
        self.write_text("README.md", "[缺失](missing.md)\n")
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validator.main([str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("LINK001", stderr.getvalue())
        self.assertIn("校验失败", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_missing_root_returns_one_without_traceback(self) -> None:
        missing = self.root / "不存在"
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validator.main([str(missing)])
        self.assertEqual(code, 1)
        self.assertIn(".:0: IO001", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_main_converts_invalid_root_path_to_io_error(self) -> None:
        invalid_root = chr(0)
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validator.main([invalid_root])
        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn(".:0: IO003", stderr.getvalue())
        self.assertNotIn(invalid_root, stderr.getvalue())
        self.assertNotIn("Traceback", stdout.getvalue() + stderr.getvalue())

    def test_main_converts_root_resolution_os_error_to_io_error(self) -> None:
        sensitive_detail = "".join(("private", "-root-detail"))
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(
            validator.Path, "resolve", side_effect=OSError(sensitive_detail)
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = validator.main([str(self.root)])
        self.assertEqual(code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn(".:0: IO003", stderr.getvalue())
        self.assertNotIn(sensitive_detail, stderr.getvalue())
        self.assertNotIn("Traceback", stdout.getvalue() + stderr.getvalue())

    def test_validate_repository_does_not_swallow_non_path_value_error(self) -> None:
        self.write_text("学习路线/入口.md", "# 合法内容\n")
        marker = "content-value-error-marker"
        with mock.patch.object(
            validator, "validate_placeholders", side_effect=ValueError(marker)
        ), self.assertRaisesRegex(ValueError, marker):
            validator.validate_repository(self.root)

    def test_main_does_not_swallow_non_path_value_error(self) -> None:
        self.write_text("学习路线/入口.md", "# 合法内容\n")
        marker = "main-content-value-error-marker"
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(
            validator, "validate_placeholders", side_effect=ValueError(marker)
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr), self.assertRaisesRegex(
            ValueError, marker
        ):
            validator.main([str(self.root)])
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")

    def test_validate_repository_does_not_swallow_non_path_os_error(self) -> None:
        self.write_text("学习路线/入口.md", "# 合法内容\n")
        marker = "content-os-error-marker"
        with mock.patch.object(
            validator, "validate_placeholders", side_effect=OSError(marker)
        ), self.assertRaisesRegex(OSError, marker):
            validator.validate_repository(self.root)

    def test_main_does_not_swallow_non_path_os_error(self) -> None:
        self.write_text("学习路线/入口.md", "# 合法内容\n")
        marker = "main-content-os-error-marker"
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(
            validator, "validate_placeholders", side_effect=OSError(marker)
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr), self.assertRaisesRegex(
            OSError, marker
        ):
            validator.main([str(self.root)])
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")

    def test_current_repository_passes(self) -> None:
        repository_root = Path(__file__).resolve().parents[3]
        errors = validator.validate_repository(repository_root)
        self.assertEqual(errors, [], "真实仓库诊断：\n" + "\n".join(errors))


class OutlineGateTests(RepositoryFixture):
    project_names = {
        1: "01-若依传统部署",
        2: "02-Docker容器化改造",
        3: "03-Kubernetes云原生部署",
        4: "04-可观测性建设",
        5: "05-AI推理服务部署",
    }
    project_stages = {1: 9, 2: 13, 3: 14, 4: 17, 5: 18}

    def outline(self, gate: str, root: Path | None = None) -> list[str]:
        function = getattr(validator, "validate_outline", None)
        self.assertTrue(callable(function), "缺少 validate_outline 公开入口")
        return function(root or self.root, gate)

    def assert_outline_rule(self, gate: str, rule: str) -> list[str]:
        errors = self.outline(gate)
        self.assert_has_rule(errors, rule)
        return errors

    def chapter_list(self, chapters: list[str]) -> str:
        return ", ".join(f"`{chapter}`" for chapter in chapters) if chapters else "—"

    def stage_row(
        self,
        stage: int,
        chapter: int = 1,
        *,
        chapter_id: str | None = None,
        filename: str | None = None,
        title: str = "测试章节",
        objective: str = "解释一个可检查的目标",
        kind: str = "`concept`",
        prerequisites: str | None = None,
        study_time: str = "30–60 分钟",
        employment: str = "必须学",
        anchors: str | None = None,
    ) -> list[str]:
        actual_id = chapter_id or f"{stage:02d}.{chapter:02d}"
        if prerequisites is None:
            prerequisites = "—" if stage == 0 else f"`{stage - 1:02d}.01`"
        if anchors is None:
            project = next(
                (
                    project
                    for project, project_stage in self.project_stages.items()
                    if project_stage == stage
                ),
                None,
            )
            anchors = f"`PRJ-{project:02d}-M01`" if project is not None else "—"
        return [
            f"`{actual_id}`",
            filename or f"`{actual_id}-测试章节.md`",
            title,
            objective,
            kind,
            prerequisites,
            study_time,
            employment,
            anchors,
        ]

    def write_stage(
        self,
        stage: int,
        rows: list[list[str]] | None = None,
        *,
        headers: tuple[str, ...] = STAGE_HEADERS,
        heading: bool = True,
        duplicate_heading: bool = False,
        separator_override: str | None = None,
    ) -> Path:
        rows = rows if rows is not None else [self.stage_row(stage)]
        table = controlled_table(headers, rows)
        if separator_override is not None:
            table_lines = table.splitlines()
            table_lines[1] = separator_override
            table = "\n".join(table_lines) + "\n"
        content = "# 阶段\n\n"
        if heading:
            content += "## 章节清单\n\n"
        content += table
        if duplicate_heading:
            content += "\n## 章节清单\n"
        return self.write_text(
            f"知识库/{OUTLINE_STAGE_DIRECTORIES[stage]}/README.md", content
        )

    def build_catalogs(self) -> None:
        for stage in range(21):
            self.write_stage(stage)

    def route_rows(self) -> list[list[str]]:
        chapters = [f"{stage:02d}.01" for stage in range(21)]
        sizes = [2] * 9 + [1] * 3
        rows: list[list[str]] = []
        offset = 0
        for week, size in enumerate(sizes, start=1):
            current = chapters[offset : offset + size]
            offset += size
            rows.append(
                [f"第 {week} 周", self.chapter_list(current), "—", f"完成第 {week} 周", "—"]
            )
        return rows

    def write_route(self, rows: list[list[str]] | None = None) -> None:
        self.write_text(
            "学习路线/02-三个月就业路线.md",
            "# 三个月就业路线\n\n"
            + controlled_table(
                ("周次", "主线章节", "弹性章节", "阶段成果", "实践锚点"),
                rows or self.route_rows(),
            ),
        )

    def build_views(self) -> None:
        self.build_catalogs()
        for path in (
            "学习路线/README.md",
            "学习路线/00-学习路线导航.md",
            "学习路线/01-完整成长路线.md",
            "学习路线/04-每日每周学习模板.md",
            "技术索引/README.md",
        ):
            self.write_text(path, "# 导航入口\n")
        self.write_route()
        self.write_text(
            "学习路线/03-职业发展路线.md",
            "# 职业发展路线\n\n"
            + controlled_table(
                ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                [["入门", "Linux 运维", "`00.01`, `01.01`", "理解基础", "—"]],
            ),
        )
        self.write_text(
            "学习路线/05-知识前置依赖.md",
            "# 知识前置依赖\n\n"
            + controlled_table(
                ("后学章节", "直接前置", "关系说明"),
                [["`01.01`", "`00.01`", "先建立运维认知"]],
            ),
        )
        self.write_text(
            "技术索引/按技术名称.md",
            "# 按技术名称\n\n"
            + controlled_table(
                ("技术主词", "别名", "章节 ID"),
                [["Linux", "GNU/Linux", "`00.01`, `01.01`"]],
            ),
        )
        self.write_text(
            "技术索引/按故障现象.md",
            "# 按故障现象\n\n"
            + controlled_table(
                ("故障现象", "机制章节", "排查方法章节", "未来案例入口"),
                [["无法连接", "`00.01`", "`01.01`", "—"]],
            ),
        )
        self.write_text(
            "技术索引/按岗位能力.md",
            "# 按岗位能力\n\n"
            + controlled_table(
                ("岗位能力", "章节 ID", "阶段成果", "项目锚点"),
                [["主机管理", "`00.01`, `01.01`", "能解释基础", "—"]],
            ),
        )

    def write_project(
        self,
        project: int,
        chapters: list[str] | None = None,
        *,
        milestone: str | None = None,
    ) -> None:
        stage = self.project_stages[project]
        chapters = chapters if chapters is not None else [f"{stage:02d}.01"]
        milestone = milestone or f"PRJ-{project:02d}-M01"
        self.write_text(
            f"项目实战/{self.project_names[project]}/README.md",
            f"# 项目 {project:02d}\n\n"
            + controlled_table(
                ("里程碑", "能力结果", "所需章节", "证据类型", "未来内容归属"),
                [[f"`{milestone}`", "完成能力结果", self.chapter_list(chapters), "验证记录", "后续项目任务"]],
            ),
        )

    def build_complete(self) -> None:
        self.build_views()
        project_rows = [
            [
                f"项目 {project:02d}",
                f"`PRJ-{project:02d}-M01`",
                f"`{stage:02d}.01`",
                "验证记录",
            ]
            for project, stage in self.project_stages.items()
        ]
        self.write_text(
            "学习路线/06-贯穿项目演进线.md",
            "# 贯穿项目演进线\n\n"
            + controlled_table(
                ("项目", "里程碑", "所需章节", "证据类型"), project_rows
            ),
        )
        checkpoint_rows = [
            [
                f"`CP-{stage:02d}`",
                f"`{stage:02d}`",
                f"`{stage:02d}.01`",
                "—",
                "完成阶段能力",
            ]
            for stage in range(21)
        ]
        self.write_text(
            "学习路线/阶段检查点/README.md",
            "# 阶段检查点\n\n"
            + controlled_table(
                ("检查点", "阶段", "所需章节", "实践锚点", "能力结果"),
                checkpoint_rows,
            ),
        )
        self.write_text("实验手册/README.md", "# 实验手册\n")
        level_names = {
            1: "Level-1-基础实验",
            2: "Level-2-综合实验",
            3: "Level-3-企业实验",
            4: "Level-4-架构实验",
        }
        for level, name in level_names.items():
            self.write_text(
                f"实验手册/{name}/README.md",
                f"# Level {level}\n\n## 实践锚点\n\n`LAB-L{level}`\n",
            )
        self.write_text("项目实战/README.md", "# 项目实战\n")
        for project in range(1, 6):
            self.write_project(project)

    def test_outline_api_is_available(self) -> None:
        self.assertTrue(callable(getattr(validator, "validate_outline", None)))

    def test_partial_accepts_current_repository_skeleton(self) -> None:
        repository_root = Path(__file__).resolve().parents[3]
        self.assertEqual(self.outline("partial", repository_root), [])

    def test_partial_accepts_valid_existing_catalog(self) -> None:
        self.write_stage(0)
        self.assertEqual(self.outline("partial"), [])

    def test_partial_accepts_multiple_values_and_empty_sets(self) -> None:
        rows = [
            self.stage_row(0),
            self.stage_row(
                0,
                2,
                prerequisites="`00.01`",
                anchors="`CP-00`, `LAB-L1`, `PRJ-01-M01`",
            ),
        ]
        self.write_stage(0, rows)
        self.assertEqual(self.outline("partial"), [])

    def test_partial_requires_heading_when_controlled_table_exists(self) -> None:
        self.write_stage(0, heading=False)
        self.assert_outline_rule("partial", "OL001")

    def test_partial_rejects_duplicate_catalog_heading(self) -> None:
        self.write_stage(0, duplicate_heading=True)
        self.assert_outline_rule("partial", "OL001")

    def test_partial_rejects_wrong_header(self) -> None:
        headers = STAGE_HEADERS[:-1] + ("锚点",)
        self.write_stage(0, headers=headers)
        self.assert_outline_rule("partial", "OL002")

    def test_partial_rejects_invalid_separator(self) -> None:
        self.write_stage(0, separator_override="|---|---|")
        self.assert_outline_rule("partial", "OL002")

    def test_ol003_rejects_invalid_chapter_id(self) -> None:
        self.write_stage(0, [self.stage_row(0, chapter_id="0.1")])
        self.assert_outline_rule("partial", "OL003")

    def test_ol003_rejects_stage_mismatch(self) -> None:
        self.write_stage(0, [self.stage_row(0, chapter_id="01.01")])
        self.assert_outline_rule("partial", "OL003")

    def test_ol003_rejects_non_contiguous_ids(self) -> None:
        self.write_stage(0, [self.stage_row(0, 2)])
        self.assert_outline_rule("partial", "OL003")

    def test_ol003_rejects_duplicate_ids(self) -> None:
        self.write_stage(0)
        self.write_stage(1, [self.stage_row(1, chapter_id="00.01")])
        self.assert_outline_rule("partial", "OL003")

    def test_ol004_rejects_invalid_filename(self) -> None:
        self.write_stage(0, [self.stage_row(0, filename="`00.01 bad.md`")])
        self.assert_outline_rule("partial", "OL004")

    def test_ol004_rejects_filename_id_mismatch(self) -> None:
        self.write_stage(0, [self.stage_row(0, filename="`00.02-测试.md`")])
        self.assert_outline_rule("partial", "OL004")

    def test_ol004_rejects_duplicate_filenames(self) -> None:
        self.write_stage(0)
        self.write_stage(1, [self.stage_row(1, filename="`00.01-测试章节.md`")])
        self.assert_outline_rule("partial", "OL004")

    def test_ol005_rejects_invalid_controlled_fields(self) -> None:
        self.write_stage(
            0,
            [
                self.stage_row(
                    0,
                    title="",
                    objective="<br>",
                    kind="`tutorial`",
                    study_time="45 分钟",
                    employment="核心",
                )
            ],
        )
        errors = self.assert_outline_rule("partial", "OL005")
        self.assertGreaterEqual(sum(" OL005 " in error for error in errors), 4)

    def test_ol006_rejects_missing_prerequisite(self) -> None:
        self.write_stage(0, [self.stage_row(0, prerequisites="`99.01`")])
        self.assert_outline_rule("partial", "OL006")

    def test_ol006_rejects_self_reference(self) -> None:
        self.write_stage(0, [self.stage_row(0, prerequisites="`00.01`")])
        self.assert_outline_rule("partial", "OL006")

    def test_ol006_rejects_forward_reference(self) -> None:
        self.write_stage(
            0,
            [
                self.stage_row(0, 1, prerequisites="`00.02`"),
                self.stage_row(0, 2, prerequisites="—"),
            ],
        )
        self.assert_outline_rule("partial", "OL006")

    def test_ol007_rejects_multi_node_cycle(self) -> None:
        self.write_stage(
            0,
            [
                self.stage_row(0, 1, prerequisites="`00.02`"),
                self.stage_row(0, 2, prerequisites="`00.01`"),
            ],
        )
        self.assert_outline_rule("partial", "OL007")

    def test_catalogs_accepts_all_twenty_one_catalogs(self) -> None:
        self.build_catalogs()
        self.assertEqual(self.outline("catalogs"), [])

    def test_catalogs_requires_all_twenty_one_catalogs(self) -> None:
        self.build_catalogs()
        (self.root / f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md").unlink()
        self.assert_outline_rule("catalogs", "OL001")

    def test_ol009_rejects_required_dependency_on_post_study(self) -> None:
        self.build_catalogs()
        self.write_stage(0, [self.stage_row(0, employment="就业后补学")])
        self.assert_outline_rule("catalogs", "OL009")

    def test_views_accepts_catalogs_routes_and_indexes(self) -> None:
        self.build_views()
        self.assertEqual(self.outline("views"), [])

    def test_views_requires_wave_three_route_file(self) -> None:
        self.build_views()
        (self.root / "技术索引/按岗位能力.md").unlink()
        self.assert_outline_rule("views", "OL001")

    def test_ol008_rejects_unknown_view_chapter(self) -> None:
        self.build_views()
        self.write_text(
            "技术索引/按技术名称.md",
            controlled_table(
                ("技术主词", "别名", "章节 ID"),
                [["Linux", "GNU/Linux", "`99.01`"]],
            ),
        )
        self.assert_outline_rule("views", "OL008")

    def test_ol008_rejects_route_prerequisite_order(self) -> None:
        self.build_views()
        rows = self.route_rows()
        rows[0][1] = "`01.01`, `00.01`"
        self.write_route(rows)
        self.assert_outline_rule("views", "OL008")

    def test_ol009_rejects_incomplete_twelve_week_closure(self) -> None:
        self.build_views()
        rows = self.route_rows()
        rows[-1][1] = "—"
        self.write_route(rows)
        self.assert_outline_rule("views", "OL009")

    def test_ol009_rejects_extra_mainline_chapter(self) -> None:
        self.build_views()
        self.write_stage(20, [self.stage_row(20, employment="建议学")])
        self.assert_outline_rule("views", "OL009")

    def test_ol009_rejects_out_of_order_week_rows(self) -> None:
        self.build_views()
        rows = self.route_rows()
        rows[0][0], rows[1][0] = rows[1][0], rows[0][0]
        self.write_route(rows)
        self.assert_outline_rule("views", "OL009")

    def test_ol012_rejects_duplicate_mainline_id(self) -> None:
        self.build_views()
        rows = self.route_rows()
        rows[-1][1] += ", `00.01`"
        self.write_route(rows)
        self.assert_outline_rule("views", "OL012")

    def test_ol012_rejects_non_suggested_flexible_chapter(self) -> None:
        self.build_views()
        rows = self.route_rows()
        rows[0][2] = "`00.01`"
        self.write_route(rows)
        self.assert_outline_rule("views", "OL012")

    def test_complete_accepts_closed_anchors_and_projects(self) -> None:
        self.build_complete()
        self.assertEqual(self.outline("complete"), [])

    def test_partial_malformed_stage_table_preserves_direct_row_diagnostics(
        self,
    ) -> None:
        rows = [
            self.stage_row(0),
            self.stage_row(0, 2, prerequisites="`00.01`", title="<br>"),
        ]
        path = self.write_stage(0, rows)
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        bad_index = next(
            index for index, line in enumerate(lines) if "`00.01`" in line
        )
        lines[bad_index] = lines[bad_index][1:]
        path.write_text("".join(lines), encoding="utf-8")

        errors = self.outline("partial")

        self.assertTrue(
            any(" OL002 " in error and "数据行列数或边界非法" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(" OL005 " in error and "标题" in error for error in errors), errors
        )
        self.assertFalse(
            any(" OL003 " in error and "00.01" in error for error in errors), errors
        )

    def test_views_malformed_table_preserves_direct_row_diagnostics(self) -> None:
        self.build_views()
        path = self.write_text(
            "技术索引/按技术名称.md",
            "# 按技术名称\n\n"
            + controlled_table(
                ("技术主词", "别名", "章节 ID"),
                [["Linux", "GNU/Linux", "`00.01`"], ["", "空主词", "`01.01`"]],
            ),
        )
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        bad_index = next(
            index for index, line in enumerate(lines) if "GNU/Linux" in line
        )
        lines[bad_index] = lines[bad_index][1:]
        path.write_text("".join(lines), encoding="utf-8")

        errors = self.outline("views")

        self.assertTrue(
            any(" OL002 " in error and "数据行列数或边界非法" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(" OL002 " in error and "技术主词" in error for error in errors), errors
        )

    def test_complete_malformed_project_view_preserves_other_direct_diagnostics(
        self,
    ) -> None:
        self.build_complete()
        path = self.root / "学习路线/06-贯穿项目演进线.md"
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        bad_index = next(
            index for index, line in enumerate(lines) if "`PRJ-01-M01`" in line
        )
        lines[bad_index] = lines[bad_index][1:]
        other_index = next(
            index for index, line in enumerate(lines) if "`PRJ-02-M01`" in line
        )
        lines[other_index] = lines[other_index].replace("| 项目 02 |", "|  |", 1)
        path.write_text("".join(lines), encoding="utf-8")

        errors = self.outline("complete")

        self.assertTrue(
            any(" OL002 " in error and "数据行列数或边界非法" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(
                " OL002 " in error
                and "项目" in error
                and "单行非空文本" in error
                for error in errors
            ),
            errors,
        )

    def test_complete_malformed_project_table_preserves_other_direct_diagnostics(
        self,
    ) -> None:
        self.build_complete()
        path = self.root / "项目实战/01-若依传统部署/README.md"
        path.write_text(
            "# 项目 01\n\n"
            + controlled_table(
                ("里程碑", "能力结果", "所需章节", "证据类型", "未来内容归属"),
                [
                    ["`PRJ-01-M01`", "完成能力结果", "`09.01`", "验证记录", "后续项目任务"],
                    ["`PRJ-01-M02`", "", "`08.01`", "验证记录", "后续项目任务"],
                ],
            ),
            encoding="utf-8",
        )
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        bad_index = next(
            index for index, line in enumerate(lines) if "`PRJ-01-M01`" in line
        )
        lines[bad_index] = lines[bad_index][1:]
        path.write_text("".join(lines), encoding="utf-8")

        errors = self.outline("complete")

        self.assertTrue(
            any(" OL002 " in error and "数据行列数或边界非法" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(" OL002 " in error and "能力结果" in error for error in errors), errors
        )
        self.assertFalse(
            any(" OL010 " in error and "预期 PRJ-01-M01" in error for error in errors),
            errors,
        )

    def test_complete_malformed_checkpoint_does_not_derive_anchor_errors(
        self,
    ) -> None:
        self.build_complete()
        self.write_stage(0, [self.stage_row(0, anchors="`CP-00`")])
        path = self.write_text(
            "学习路线/阶段检查点/README.md",
            "# 阶段检查点\n\n"
            + controlled_table(
                ("检查点", "阶段", "所需章节", "实践锚点", "能力结果"),
                [
                    ["`CP-00`", "`00`", "`00.01`", "—", "完成阶段能力"],
                    ["`CP-01`", "`01`", "`01.01`", "—", ""],
                ],
            ),
        )
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        bad_index = next(
            index for index, line in enumerate(lines) if "`CP-00`" in line
        )
        lines[bad_index] = lines[bad_index][1:]
        path.write_text("".join(lines), encoding="utf-8")

        errors = self.outline("complete")

        self.assertTrue(
            any(" OL002 " in error and "数据行列数或边界非法" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(" OL002 " in error and "能力结果" in error for error in errors), errors
        )
        self.assertFalse(
            any(" OL010 " in error and "CP-00 不存在" in error for error in errors),
            errors,
        )
        self.assertFalse(
            any(" OL010 " in error and "应按 CP-00" in error for error in errors),
            errors,
        )

    def test_complete_invalid_view_record_preserves_unrelated_missing_milestone(
        self,
    ) -> None:
        self.build_complete()
        path = self.root / "学习路线/06-贯穿项目演进线.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("`09.01`", "09.01", 1)
        text = text.replace(
            "| 项目 05 | `PRJ-05-M01` | `18.01` | 验证记录 |\n", "", 1
        )
        path.write_text(text, encoding="utf-8")

        errors = self.outline("complete")

        self.assertTrue(any(" OL002 " in error for error in errors), errors)
        self.assertTrue(
            any(" OL011 " in error and "PRJ-05-M01" in error for error in errors),
            errors,
        )

    def test_complete_invalid_project_record_preserves_unrelated_missing_milestone(
        self,
    ) -> None:
        self.build_complete()
        project_path = self.root / "项目实战/01-若依传统部署/README.md"
        project_path.write_text(
            project_path.read_text(encoding="utf-8").replace("`09.01`", "09.01", 1),
            encoding="utf-8",
        )
        view_path = self.root / "学习路线/06-贯穿项目演进线.md"
        view_path.write_text(
            view_path.read_text(encoding="utf-8").replace(
                "| 项目 05 | `PRJ-05-M01` | `18.01` | 验证记录 |\n", "", 1
            ),
            encoding="utf-8",
        )

        errors = self.outline("complete")

        self.assertTrue(any(" OL002 " in error for error in errors), errors)
        self.assertTrue(
            any(" OL011 " in error and "PRJ-05-M01" in error for error in errors),
            errors,
        )

    def test_complete_invalid_view_milestone_preserves_unrelated_missing_milestone(
        self,
    ) -> None:
        self.build_complete()
        path = self.root / "学习路线/06-贯穿项目演进线.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("`PRJ-01-M01`", "`PRJ-99-M01`", 1)
        text = text.replace(
            "| 项目 05 | `PRJ-05-M01` | `18.01` | 验证记录 |\n", "", 1
        )
        path.write_text(text, encoding="utf-8")

        errors = self.outline("complete")

        self.assertTrue(any(" OL010 " in error for error in errors), errors)
        self.assertTrue(
            any(" OL011 " in error and "PRJ-05-M01" in error for error in errors),
            errors,
        )

    def test_complete_wrong_project_milestone_emits_only_direct_error(self) -> None:
        cases = ("without-legal-same-name", "with-legal-same-name")
        observed: dict[str, list[str]] = {}
        for case in cases:
            with self.subTest(case=case):
                self.build_complete()
                self.write_text(
                    "项目实战/01-若依传统部署/README.md",
                    "# 项目 01\n\n"
                    + controlled_table(
                        ("里程碑", "能力结果", "所需章节", "证据类型", "未来内容归属"),
                        [
                            ["`PRJ-01-M01`", "完成能力结果", "`09.01`", "验证记录", "后续项目任务"],
                            ["`PRJ-02-M02`", "错误归属", "`08.01`", "验证记录", "后续项目任务"],
                        ],
                    ),
                )
                if case == "without-legal-same-name":
                    self.write_stage(8, [self.stage_row(8, anchors="`PRJ-02-M02`")])
                else:
                    self.write_text(
                        "项目实战/02-Docker容器化改造/README.md",
                        "# 项目 02\n\n"
                        + controlled_table(
                            ("里程碑", "能力结果", "所需章节", "证据类型", "未来内容归属"),
                            [
                                ["`PRJ-02-M01`", "完成能力结果", "`13.01`", "验证记录", "后续项目任务"],
                                ["`PRJ-02-M02`", "合法定义", "`08.01`", "验证记录", "后续项目任务"],
                            ],
                        ),
                    )
                    view_path = self.root / "学习路线/06-贯穿项目演进线.md"
                    row = "| 项目 02 | `PRJ-02-M01` | `13.01` | 验证记录 |\n"
                    view_path.write_text(
                        view_path.read_text(encoding="utf-8").replace(
                            row,
                            row
                            + "| 项目 02 | `PRJ-02-M02` | `08.01` | 验证记录 |\n",
                            1,
                        ),
                        encoding="utf-8",
                    )

                errors = self.outline("complete")
                observed[case] = errors

        violations: list[str] = []
        without_legal = observed["without-legal-same-name"]
        with_legal = observed["with-legal-same-name"]
        for case, errors in observed.items():
            direct = [
                error
                for error in errors
                if " OL010 " in error and "预期 PRJ-01-M02" in error
            ]
            if len(direct) != 1:
                violations.append(f"{case}: direct={direct!r}")
            if any("重复定义" in error for error in errors):
                violations.append(f"{case}: duplicate={errors!r}")
        if len(without_legal) != 1:
            violations.append(f"without-legal-same-name: errors={without_legal!r}")
        legal_gaps = [
            error
            for error in with_legal
            if " OL011 " in error and "PRJ-02-M02" in error
        ]
        if len(legal_gaps) != 1 or len(with_legal) != 2:
            violations.append(f"with-legal-same-name: errors={with_legal!r}")
        self.assertEqual(violations, [])

    def test_complete_invalid_sibling_milestone_preserves_valid_mapping_error(
        self,
    ) -> None:
        self.build_complete()
        self.write_stage(8, [self.stage_row(8, anchors="`PRJ-01-M01`")])
        self.write_text(
            "项目实战/01-若依传统部署/README.md",
            "# 项目 01\n\n"
            + controlled_table(
                ("里程碑", "能力结果", "所需章节", "证据类型", "未来内容归属"),
                [
                    ["`PRJ-01-M01`", "完成能力结果", "`08.01`", "验证记录", "后续项目任务"],
                    ["`PRJ-01-M03`", "非法兄弟", "`08.01`", "验证记录", "后续项目任务"],
                ],
            ),
        )
        view_path = self.root / "学习路线/06-贯穿项目演进线.md"
        view_path.write_text(
            view_path.read_text(encoding="utf-8").replace(
                "| 项目 01 | `PRJ-01-M01` | `09.01` |",
                "| 项目 01 | `PRJ-01-M01` | `08.01` |",
                1,
            ),
            encoding="utf-8",
        )

        errors = self.outline("complete")

        self.assertTrue(
            any(" OL010 " in error and "预期 PRJ-01-M02" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any(
                " OL011 " in error
                and "PRJ-01-M01" in error
                and "09.01" in error
                for error in errors
            ),
            errors,
        )

    def test_partial_missing_separator_preserves_first_data_row_diagnostics(
        self,
    ) -> None:
        violations: list[str] = []
        cases = ("missing-separator", "malformed-separator-shape")
        for case in cases:
            with self.subTest(case=case):
                with tempfile.TemporaryDirectory() as directory:
                    fixture = type(self)("runTest")
                    fixture.root = Path(directory)
                    rows = [
                        fixture.stage_row(0, title="<br>"),
                        fixture.stage_row(0, 2, prerequisites="`00.01`"),
                    ]
                    path = fixture.write_stage(0, rows)
                    lines = path.read_text(encoding="utf-8").splitlines()
                    separator_index = next(
                        index for index, line in enumerate(lines) if line.startswith("|---")
                    )
                    if case == "missing-separator":
                        del lines[separator_index]
                    else:
                        lines[separator_index] = (
                            "|:-:|--:|:--|:-|--|:-:|--|:--:|:-|"
                        )
                    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

                    errors = fixture.outline("partial")
                    separator_errors = [
                        error
                        for error in errors
                        if " OL002 " in error and "分隔行非法" in error
                    ]
                    if len(separator_errors) != 1:
                        violations.append(f"{case}: separator={separator_errors!r}")
                    if case == "missing-separator":
                        title_errors = [
                            error
                            for error in errors
                            if " OL005 " in error and "标题" in error
                        ]
                        if len(title_errors) != 1:
                            violations.append(
                                f"missing-separator: title={title_errors!r}; errors={errors!r}"
                            )
                        if any(
                            " OL003 " in error and "应连续为 00.01" in error
                            for error in errors
                        ):
                            violations.append(
                                f"missing-separator: compressed-position={errors!r}"
                            )
                    else:
                        separator_line = separator_index + 1
                        direct_from_separator = [
                            error
                            for error in errors
                            if f":{separator_line}:" in error
                            and any(
                                f" {rule} " in error
                                for rule in ("OL003", "OL004", "OL005", "OL010")
                            )
                        ]
                        if direct_from_separator:
                            violations.append(
                                "malformed-separator-shape: "
                                f"data-diagnostics={direct_from_separator!r}"
                            )
                    temporary_root = Path(directory)
                if temporary_root.exists():
                    violations.append(f"{case}: temporary directory not cleaned")
        self.assertEqual(violations, [])

    def test_complete_invalid_view_key_does_not_suppress_foreign_project_gap(
        self,
    ) -> None:
        self.build_complete()
        path = self.root / "学习路线/06-贯穿项目演进线.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("`PRJ-01-M01`", "`PRJ-02-M01`", 1)
        text = text.replace(
            "| 项目 02 | `PRJ-02-M01` | `13.01` | 验证记录 |\n", "", 1
        )
        path.write_text(text, encoding="utf-8")

        errors = self.outline("complete")

        direct = [
            error
            for error in errors
            if error.startswith("学习路线/06-贯穿项目演进线.md:")
            and " OL010 " in error
            and "项目演进视图里程碑应属于项目 01" in error
        ]
        foreign_gap = [
            error
            for error in errors
            if error.startswith("项目实战/02-Docker容器化改造/README.md:")
            and " OL011 " in error
            and "PRJ-02-M01 未出现在贯穿项目视图" in error
        ]
        self.assertEqual(len(direct), 1, errors)
        self.assertEqual(len(foreign_gap), 1, errors)

    def test_complete_invalid_project_key_scopes_chapter_reference_by_relation(
        self,
    ) -> None:
        violations: list[str] = []
        for case in ("different-chapter", "same-chapter-different-source"):
            with self.subTest(case=case):
                with tempfile.TemporaryDirectory() as directory:
                    fixture = type(self)("runTest")
                    fixture.root = Path(directory)
                    fixture.build_complete()
                    fixture.write_text(
                        "项目实战/01-若依传统部署/README.md",
                        "# 项目 01\n\n"
                        + controlled_table(
                            (
                                "里程碑",
                                "能力结果",
                                "所需章节",
                                "证据类型",
                                "未来内容归属",
                            ),
                            [
                                [
                                    "`PRJ-01-M01`",
                                    "完成能力结果",
                                    "`09.01`",
                                    "验证记录",
                                    "后续项目任务",
                                ],
                                [
                                    "`PRJ-02-M02`",
                                    "错误归属",
                                    "`08.01`",
                                    "验证记录",
                                    "后续项目任务",
                                ],
                            ],
                        ),
                    )
                    fixture.write_stage(
                        8, [fixture.stage_row(8, anchors="`PRJ-02-M02`")]
                    )
                    related_chapter = "13.01" if case == "different-chapter" else "08.01"
                    if case == "different-chapter":
                        fixture.write_stage(
                            13,
                            [
                                fixture.stage_row(
                                    13,
                                    anchors="`PRJ-02-M01`, `PRJ-02-M02`",
                                )
                            ],
                        )
                    view_path = fixture.root / "学习路线/06-贯穿项目演进线.md"
                    row = "| 项目 02 | `PRJ-02-M01` | `13.01` | 验证记录 |\n"
                    view_path.write_text(
                        view_path.read_text(encoding="utf-8").replace(
                            row,
                            row
                            + "| 项目 02 | `PRJ-02-M02` | "
                            + f"`{related_chapter}` | 验证记录 |\n",
                            1,
                        ),
                        encoding="utf-8",
                    )

                    errors = fixture.outline("complete")
                    direct = [
                        error
                        for error in errors
                        if error.startswith(
                            "项目实战/01-若依传统部署/README.md:"
                        )
                        and " OL010 " in error
                        and "预期 PRJ-01-M02" in error
                    ]
                    if len(direct) != 1:
                        violations.append(f"{case}: direct={direct!r}")
                    stage_eight_cascade = [
                        error
                        for error in errors
                        if error.startswith(
                            "知识库/08-Shell与Python/README.md:"
                        )
                        and "PRJ-02-M02" in error
                        and (" OL010 " in error or " OL011 " in error)
                    ]
                    if stage_eight_cascade:
                        violations.append(
                            f"{case}: stage-eight-cascade={stage_eight_cascade!r}"
                        )
                    if case == "different-chapter":
                        stage_thirteen_missing = [
                            error
                            for error in errors
                            if error.startswith(
                                "知识库/13-Docker容器/README.md:"
                            )
                            and " OL010 " in error
                            and "PRJ-02-M02 不存在" in error
                        ]
                        stage_thirteen_unlisted = [
                            error
                            for error in errors
                            if error.startswith(
                                "知识库/13-Docker容器/README.md:"
                            )
                            and " OL011 " in error
                            and "PRJ-02-M02" in error
                            and "13.01" in error
                        ]
                        if len(stage_thirteen_missing) != 1:
                            violations.append(
                                f"different-chapter: missing={stage_thirteen_missing!r}; errors={errors!r}"
                            )
                        if len(stage_thirteen_unlisted) != 1:
                            violations.append(
                                "different-chapter: "
                                f"unlisted={stage_thirteen_unlisted!r}; errors={errors!r}"
                            )
                    else:
                        view_missing = [
                            error
                            for error in errors
                            if error.startswith(
                                "学习路线/06-贯穿项目演进线.md:"
                            )
                            and " OL010 " in error
                            and "PRJ-02-M02 不存在" in error
                        ]
                        if len(view_missing) != 1:
                            violations.append(
                                "same-chapter-different-source: "
                                f"view-missing={view_missing!r}; errors={errors!r}"
                            )
                    temporary_root = Path(directory)
                if temporary_root.exists():
                    violations.append(f"{case}: temporary directory not cleaned")
        self.assertEqual(violations, [])

    def test_complete_unstable_view_identity_stops_only_view_comparison(
        self,
    ) -> None:
        self.build_complete()
        view_path = self.root / "学习路线/06-贯穿项目演进线.md"
        view_path.write_text(
            view_path.read_text(encoding="utf-8").replace(
                "`PRJ-01-M01`", "`BROKEN`", 1
            ),
            encoding="utf-8",
        )
        self.write_stage(13, [self.stage_row(13, anchors="—")])

        errors = self.outline("complete")

        direct = [
            error
            for error in errors
            if error.startswith("学习路线/06-贯穿项目演进线.md:")
            and " OL010 " in error
            and "项目演进视图的里程碑" in error
        ]
        unstable_view_gap = [
            error
            for error in errors
            if " OL011 " in error
            and "PRJ-01-M01 未出现在贯穿项目视图" in error
        ]
        independent_gap = [
            error
            for error in errors
            if error.startswith("项目实战/02-Docker容器化改造/README.md:")
            and " OL011 " in error
            and "PRJ-02-M01" in error
            and "13.01" in error
            and "章节未反向引用" in error
        ]
        self.assertEqual(len(direct), 1, errors)
        self.assertEqual(unstable_view_gap, [], errors)
        self.assertEqual(len(independent_gap), 1, errors)

    def test_catalog_cycles_has_no_post_normalization_comparison_sort(self) -> None:
        class ComparableId(str):
            comparisons = 0

            def __lt__(self, other: object) -> bool:
                type(self).comparisons += 1
                return str.__lt__(self, other)

        nodes = [ComparableId(f"N-{index:03d}") for index in range(256)]
        graph = {
            node: (nodes[(int(node[-3:]) + 1) % len(nodes)],)
            for node in reversed(nodes)
        }

        ComparableId.comparisons = 0
        first = validator._catalog_cycles(graph)
        first_comparisons = ComparableId.comparisons
        ComparableId.comparisons = 0
        second = validator._catalog_cycles(graph)
        second_comparisons = ComparableId.comparisons

        self.assertEqual(first, second)
        self.assertEqual(len(first), 1)
        self.assertEqual(len(first[0]), 256)
        self.assertEqual(len(set(first[0])), 256)
        self.assertEqual(first[0][0], "N-000")
        self.assertEqual(first_comparisons, 255)
        self.assertEqual(second_comparisons, 255)

        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        function_node = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "_catalog_cycles"
        )
        function_dump = ast.dump(function_node, include_attributes=False)
        self.assertEqual(
            hashlib.sha256(function_dump.encode("utf-8")).hexdigest(),
            "705deb57eb4a09333016b64c8d451d2df363fb74daa073fdafc000033d98d604",
        )
        reverse_assignment = next(
            node
            for node in ast.walk(function_node)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "reverse"
                for target in node.targets
            )
        )
        post_normalization_forbidden_calls = [
            (node.lineno, ast.unparse(node.func))
            for node in ast.walk(function_node)
            if isinstance(node, ast.Call)
            and node.lineno > reverse_assignment.lineno
            and (
                isinstance(node.func, ast.Name)
                and node.func.id in {"sorted", "min", "max"}
                or isinstance(node.func, ast.Attribute)
                and (
                    node.func.attr == "sort"
                    or isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "heapq"
                )
            )
        ]
        self.assertEqual(post_normalization_forbidden_calls, [])

    def test_complete_rejects_all_controlled_tables_inside_fences(self) -> None:
        self.build_complete()
        for path in sorted(self.root.rglob("*.md")):
            original = path.read_text(encoding="utf-8")
            path.write_text(
                f"```markdown\n{original.rstrip()}\n```\n",
                encoding="utf-8",
            )

        errors = self.outline("complete")

        self.assert_has_rule(errors, "OL001")
        self.assertNotIn("Traceback", "\n".join(errors))

    def test_partial_skips_fenced_example_before_real_stage_table(self) -> None:
        fenced_example = (
            "```markdown\n"
            + controlled_table(("示例列",), [["不是正式章节表"]])
            + "```\n"
        )
        self.write_text(
            f"知识库/{OUTLINE_STAGE_DIRECTORIES[0]}/README.md",
            "# 阶段\n\n## 章节清单\n\n"
            + fenced_example
            + "\n"
            + controlled_table(STAGE_HEADERS, [self.stage_row(0)]),
        )

        self.assertEqual(self.outline("partial"), [])

    def test_catalogs_ignores_indented_code_table(self) -> None:
        self.build_catalogs()
        real_table = controlled_table(STAGE_HEADERS, [self.stage_row(20)])
        for indent in ("    ", "\t"):
            with self.subTest(indent=repr(indent)):
                indented_table = "\n".join(
                    indent + line for line in real_table.splitlines()
                )
                self.write_text(
                    f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md",
                    "# 阶段\n\n## 章节清单\n\n" + indented_table + "\n",
                )

                errors = self.outline("catalogs")

                self.assertEqual(sum(" OL001 " in error for error in errors), 1, errors)
                self.assertFalse(any(" OL002 " in error for error in errors), errors)
                self.assertNotIn("Traceback", "\n".join(errors))

    def test_catalogs_ignores_mixed_space_tab_indented_code_table(self) -> None:
        self.build_catalogs()
        real_table = controlled_table(STAGE_HEADERS, [self.stage_row(20)])
        for prefix in (" \t", "  \t", "   \t"):
            with self.subTest(prefix=repr(prefix)):
                indented_table = "\n".join(
                    prefix + line for line in real_table.splitlines()
                )
                self.write_text(
                    f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md",
                    "# 阶段\n\n## 章节清单\n\n" + indented_table + "\n",
                )

                errors = self.outline("catalogs")

                self.assertEqual(sum(" OL001 " in error for error in errors), 1, errors)
                self.assertFalse(any(" OL002 " in error for error in errors), errors)
                self.assertNotIn("Traceback", "\n".join(errors))

    def test_catalogs_accepts_real_table_with_up_to_three_spaces(self) -> None:
        self.build_catalogs()
        real_table = controlled_table(STAGE_HEADERS, [self.stage_row(20)])
        for prefix in ("", " ", "  ", "   "):
            with self.subTest(prefix=repr(prefix)):
                table = "\n".join(prefix + line for line in real_table.splitlines())
                self.write_text(
                    f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md",
                    "# 阶段\n\n## 章节清单\n\n" + table + "\n",
                )

                self.assertEqual(self.outline("catalogs"), [])

    def test_catalogs_keeps_table_masked_after_indented_pseudo_closing_fence(
        self,
    ) -> None:
        self.build_catalogs()
        real_table = controlled_table(STAGE_HEADERS, [self.stage_row(20)])
        relative = f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md"
        for prefix in ("    ", "\t", " \t"):
            with self.subTest(prefix=repr(prefix)):
                self.write_text(
                    relative,
                    "# 阶段\n\n## 章节清单\n\n```markdown\n"
                    + prefix
                    + "```\n"
                    + real_table
                    + "```\n",
                )

                errors = self.outline("catalogs")

                self.assertEqual(sum(" OL001 " in error for error in errors), 1, errors)
                self.assertFalse(any(" OL002 " in error for error in errors), errors)
                self.assertNotIn("Traceback", "\n".join(errors))

    def test_catalogs_accepts_table_after_valid_closing_fence_indent(self) -> None:
        self.build_catalogs()
        real_table = controlled_table(STAGE_HEADERS, [self.stage_row(20)])
        relative = f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md"
        for prefix in ("", " ", "  ", "   "):
            with self.subTest(prefix=repr(prefix)):
                self.write_text(
                    relative,
                    "# 阶段\n\n## 章节清单\n\n```markdown\n示例\n"
                    + prefix
                    + "```\n"
                    + real_table,
                )

                self.assertEqual(self.outline("catalogs"), [])

    def test_catalogs_does_not_open_backtick_fence_with_backtick_info(self) -> None:
        self.build_catalogs()
        real_table = controlled_table(STAGE_HEADERS, [self.stage_row(20)])
        self.write_text(
            f"知识库/{OUTLINE_STAGE_DIRECTORIES[20]}/README.md",
            "# 阶段\n\n## 章节清单\n\n```bad`info\n" + real_table,
        )

        self.assertEqual(self.outline("catalogs"), [])

    def test_complete_malformed_project_view_rows_emit_only_direct_errors(
        self,
    ) -> None:
        def mutate(text: str, kind: str) -> str:
            lines = text.splitlines(keepends=True)
            for index, line in enumerate(lines):
                if "`PRJ-02-M01`" not in line:
                    continue
                body = line.rstrip("\r\n")
                ending = line[len(body) :]
                if kind == "missing-leading":
                    body = body[1:]
                elif kind == "missing-trailing":
                    body = body[:-1]
                else:
                    body = body[:-1] + "| 多余 |"
                lines[index] = body + ending
                break
            return "".join(lines)

        for kind in ("missing-leading", "missing-trailing", "extra-column"):
            with self.subTest(kind=kind):
                self.build_complete()
                path = self.root / "学习路线/06-贯穿项目演进线.md"
                path.write_text(mutate(path.read_text("utf-8"), kind), encoding="utf-8")

                errors = self.outline("complete")

                self.assertTrue(errors, "结构错误必须产生直接 OL002")
                self.assertTrue(all(" OL002 " in error for error in errors), errors)

    def test_complete_malformed_project_mapping_rows_emit_only_direct_errors(
        self,
    ) -> None:
        def mutate(text: str, kind: str) -> str:
            lines = text.splitlines(keepends=True)
            for index, line in enumerate(lines):
                if "`PRJ-01-M01`" not in line:
                    continue
                body = line.rstrip("\r\n")
                ending = line[len(body) :]
                if kind == "missing-leading":
                    body = body[1:]
                elif kind == "missing-trailing":
                    body = body[:-1]
                else:
                    body = body[:-1] + "| 多余 |"
                lines[index] = body + ending
                break
            return "".join(lines)

        for kind in ("missing-leading", "missing-trailing", "extra-column"):
            with self.subTest(kind=kind):
                self.build_complete()
                path = self.root / "项目实战/01-若依传统部署/README.md"
                path.write_text(mutate(path.read_text("utf-8"), kind), encoding="utf-8")

                errors = self.outline("complete")

                self.assertTrue(errors, "结构错误必须产生直接 OL002")
                self.assertTrue(all(" OL002 " in error for error in errors), errors)

    def test_complete_blank_line_terminates_controlled_table_before_prose(self) -> None:
        self.build_complete()
        path = self.root / "学习路线/06-贯穿项目演进线.md"
        path.write_text(
            path.read_text("utf-8") + "\n说明文字 | 可以包含 | 竖线\n",
            encoding="utf-8",
        )

        self.assertEqual(self.outline("complete"), [])

    def test_complete_invalid_project_view_chapters_do_not_emit_ol011(self) -> None:
        self.build_complete()
        path = self.root / "学习路线/06-贯穿项目演进线.md"
        path.write_text(
            path.read_text("utf-8").replace("`09.01`", "09.01", 1),
            encoding="utf-8",
        )

        errors = self.outline("complete")

        self.assertEqual(sum(" OL002 " in error for error in errors), 1, errors)
        self.assertFalse(any(" OL011 " in error for error in errors), errors)

    def test_complete_invalid_project_mapping_chapters_do_not_emit_ol011(self) -> None:
        self.build_complete()
        path = self.root / "项目实战/01-若依传统部署/README.md"
        path.write_text(
            path.read_text("utf-8").replace("`09.01`", "09.01", 1),
            encoding="utf-8",
        )

        errors = self.outline("complete")

        self.assertEqual(sum(" OL002 " in error for error in errors), 1, errors)
        self.assertFalse(any(" OL011 " in error for error in errors), errors)

    def test_complete_allows_html_break_literal_in_inline_code(self) -> None:
        for delimiter in ("`", "``", "```"):
            with self.subTest(delimiter=delimiter):
                self.build_complete()
                self.write_stage(
                    0,
                    [
                        self.stage_row(
                            0, title=f"测试 {delimiter}<br>{delimiter} 章节"
                        )
                    ],
                )
                self.write_text(
                    "学习路线/03-职业发展路线.md",
                    "# 职业发展路线\n\n"
                    + controlled_table(
                        ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                        [
                            [
                                "入门",
                                "Linux 运维",
                                "`00.01`, `01.01`",
                                f"完成 {delimiter}<br>{delimiter} 结果",
                                "—",
                            ]
                        ],
                    ),
                )

                self.assertEqual(self.outline("complete"), [])

    def test_complete_allows_odd_escaped_html_break_literal(self) -> None:
        self.build_complete()
        self.write_stage(0, [self.stage_row(0, title=r"测试 \<br> 章节")])
        self.write_text(
            "学习路线/03-职业发展路线.md",
            "# 职业发展路线\n\n"
            + controlled_table(
                ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                [["入门", "Linux 运维", "`00.01`, `01.01`", r"完成 \<br> 结果", "—"]],
            ),
        )

        self.assertEqual(self.outline("complete"), [])

    def test_complete_rejects_raw_and_even_escaped_html_break(self) -> None:
        for label, title, result in (
            ("raw", "测试 <br> 章节", "完成 <br> 结果"),
            ("even-escaped", r"测试 \\<br> 章节", r"完成 \\<br> 结果"),
            (
                "escaped-code-opener",
                r"测试 \`<br>` 章节",
                r"完成 \`<br>` 结果",
            ),
        ):
            with self.subTest(label=label):
                self.build_complete()
                self.write_stage(0, [self.stage_row(0, title=title)])
                self.write_text(
                    "学习路线/03-职业发展路线.md",
                    "# 职业发展路线\n\n"
                    + controlled_table(
                        ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                        [["入门", "Linux 运维", "`00.01`, `01.01`", result, "—"]],
                    ),
                )

                errors = self.outline("complete")

                self.assert_has_rule(errors, "OL005")
                self.assert_has_rule(errors, "OL002")

    def test_catalog_cycles_collapses_dense_strong_component(self) -> None:
        nodes = tuple(f"N{index:03d}" for index in range(100))
        graph = {
            node: tuple(other for other in nodes if other != node) for node in nodes
        }

        first = validator._catalog_cycles(graph)
        second = validator._catalog_cycles(graph)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 1, first)
        self.assertEqual(len(first[0]), 100)
        self.assertEqual(set(first[0]), set(nodes))

    def test_catalogs_reports_cycle_component_without_fabricated_path(self) -> None:
        self.write_stage(
            0,
            [
                self.stage_row(0, 1, prerequisites="`00.03`"),
                self.stage_row(0, 2, prerequisites="`00.01`"),
                self.stage_row(0, 3, prerequisites="`00.02`"),
            ],
        )

        errors = self.outline("partial")
        cycles = [error for error in errors if " OL007 " in error]

        self.assertEqual(len(cycles), 1, errors)
        self.assertIn("循环分量", cycles[0])
        self.assertNotIn(" -> ", cycles[0])
        for chapter_id in ("00.01", "00.02", "00.03"):
            self.assertIn(chapter_id, cycles[0])

    def test_complete_rejects_attribute_bearing_html_break(self) -> None:
        self.build_complete()
        self.write_stage(
            0,
            [self.stage_row(0, title='测试<br class="x">章节')],
        )

        errors = self.outline("complete")

        self.assert_has_rule(errors, "OL005")
        self.assertTrue(any("标题" in error for error in errors), errors)
        self.assertNotIn("Traceback", "\n".join(errors))

    def test_complete_rejects_case_and_whitespace_html_break_variants(
        self,
    ) -> None:
        self.build_complete()
        variants = ('完成<BR data-x="1" />结果', '完成<br data-x = "1"    >结果')
        for value in variants:
            with self.subTest(value=value):
                self.write_text(
                    "学习路线/03-职业发展路线.md",
                    "# 职业发展路线\n\n"
                    + controlled_table(
                        ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                        [["入门", "Linux 运维", "`00.01`, `01.01`", value, "—"]],
                    ),
                )

                errors = self.outline("complete")

                self.assert_has_rule(errors, "OL002")
                self.assertTrue(any("阶段成果" in error for error in errors), errors)
                self.assertNotIn("Traceback", "\n".join(errors))

        self.write_text(
            "学习路线/03-职业发展路线.md",
            "# 职业发展路线\n\n"
            + controlled_table(
                ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                [["入门", "Linux 运维", "`00.01`, `01.01`", "普通 br 与 <bracket> 文本", "—"]],
            ),
        )
        self.assertEqual(self.outline("complete"), [])

    def test_complete_rejects_html_break_with_angle_brackets_in_attributes(
        self,
    ) -> None:
        self.build_complete()

        def write_stage_result(value: str) -> None:
            self.write_text(
                "学习路线/03-职业发展路线.md",
                "# 职业发展路线\n\n"
                + controlled_table(
                    ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                    [
                        [
                            "入门",
                            "Linux 运维",
                            "`00.01`, `01.01`",
                            value,
                            "—",
                        ]
                    ],
                ),
            )

        variants = (
            '<br title="<x>">',
            '<BR title="<x>" />',
            '<br data-note="a > b < c">',
            "<br title='<x>'>",
        )
        for variant in variants:
            write_stage_result("完成阶段成果")
            with self.subTest(field="title", variant=variant):
                self.write_stage(
                    0,
                    [self.stage_row(0, title=f"测试{variant}章节")],
                )

                errors = self.outline("complete")

                self.assert_has_rule(errors, "OL005")
                self.assertTrue(any("标题" in error for error in errors), errors)
                self.assertNotIn("Traceback", "\n".join(errors))

            self.write_stage(0)
            with self.subTest(field="stage_result", variant=variant):
                write_stage_result(f"完成{variant}结果")

                errors = self.outline("complete")

                self.assert_has_rule(errors, "OL002")
                self.assertTrue(any("阶段成果" in error for error in errors), errors)
                self.assertNotIn("Traceback", "\n".join(errors))

    def test_complete_allows_plain_br_and_non_break_tag_names(self) -> None:
        self.build_complete()
        controls = (
            "普通 br 文本",
            "<bracket>",
            "<br-description>",
            "<br:custom>",
            "<brx>",
        )
        for control in controls:
            with self.subTest(control=control):
                self.write_stage(
                    0,
                    [self.stage_row(0, title=f"测试{control}章节")],
                )
                self.write_text(
                    "学习路线/03-职业发展路线.md",
                    "# 职业发展路线\n\n"
                    + controlled_table(
                        ("能力层级", "岗位方向", "章节 ID", "阶段成果", "项目锚点"),
                        [
                            [
                                "入门",
                                "Linux 运维",
                                "`00.01`, `01.01`",
                                f"完成{control}结果",
                                "—",
                            ]
                        ],
                    ),
                )

                self.assertEqual(self.outline("complete"), [])

    def test_catalogs_handles_graph_deeper_than_recursion_limit(self) -> None:
        identifiers = [
            f"{stage:02d}.{chapter:02d}"
            for stage in range(11)
            for chapter in range(1, 100)
        ]
        for stage in range(11):
            rows: list[list[str]] = []
            for chapter in range(1, 100):
                index = stage * 99 + chapter - 1
                prerequisite = identifiers[(index + 1) % len(identifiers)]
                rows.append(
                    self.stage_row(
                        stage,
                        chapter,
                        prerequisites=f"`{prerequisite}`",
                        anchors="—",
                    )
                )
            self.write_stage(stage, rows)
        for stage in range(11, 21):
            self.write_stage(stage)

        first = self.outline("catalogs")
        second = self.outline("catalogs")

        self.assertEqual(first, second)
        self.assert_has_rule(first, "OL007")
        self.assertNotIn("RecursionError", "\n".join(first))
        self.assertNotIn("Traceback", "\n".join(first))

    def test_complete_missing_project_view_does_not_emit_ol011(self) -> None:
        self.build_complete()
        (self.root / "学习路线/06-贯穿项目演进线.md").unlink()

        errors = self.outline("complete")

        self.assertEqual(len(errors), 1, errors)
        self.assert_has_rule(errors, "OL001")
        self.assertFalse(any(" OL011 " in error for error in errors), errors)
        self.assertNotIn("Traceback", "\n".join(errors))

    def test_complete_malformed_project_view_does_not_emit_ol011(self) -> None:
        self.build_complete()
        self.write_text(
            "学习路线/06-贯穿项目演进线.md",
            "# 贯穿项目演进线\n\n"
            + controlled_table(
                ("错误项目列", "里程碑", "所需章节", "证据类型"),
                [["项目 01", "`PRJ-01-M01`", "`09.01`", "验证记录"]],
            ),
        )

        errors = self.outline("complete")

        self.assertEqual(len(errors), 1, errors)
        self.assert_has_rule(errors, "OL002")
        self.assertFalse(any(" OL011 " in error for error in errors), errors)
        self.assertNotIn("Traceback", "\n".join(errors))

    def test_complete_invalid_project_view_milestone_does_not_emit_closure_ol011(
        self,
    ) -> None:
        self.build_complete()
        view_path = self.root / "学习路线/06-贯穿项目演进线.md"
        view_text = view_path.read_text(encoding="utf-8")
        view_path.write_text(
            view_text.replace("`PRJ-01-M01`", "`PRJ-99-M01`", 1),
            encoding="utf-8",
        )

        errors = self.outline("complete")

        self.assertEqual(len(errors), 1, errors)
        self.assert_has_rule(errors, "OL010")
        self.assertFalse(any(" OL011 " in error for error in errors), errors)
        self.assertNotIn("Traceback", "\n".join(errors))

    def test_complete_rejects_project_milestone_missing_from_evolution_view(
        self,
    ) -> None:
        self.build_complete()
        missing_milestone = "PRJ-05-M01"
        view_path = self.root / "学习路线/06-贯穿项目演进线.md"
        view_text = view_path.read_text(encoding="utf-8")
        missing_row = (
            f"| 项目 05 | `{missing_milestone}` | `18.01` | 验证记录 |\n"
        )
        self.assertIn(missing_row, view_text)
        view_path.write_text(view_text.replace(missing_row, ""), encoding="utf-8")

        errors = self.outline("complete")

        self.assertEqual(len(errors), 1, errors)
        self.assertIn(" OL011 ", errors[0])
        self.assertIn(missing_milestone, errors[0])

    def test_complete_requires_level_anchor_file(self) -> None:
        self.build_complete()
        (self.root / "实验手册/Level-4-架构实验/README.md").unlink()
        self.assert_outline_rule("complete", "OL001")

    def test_ol010_rejects_invalid_anchor_syntax(self) -> None:
        self.write_stage(0, [self.stage_row(0, anchors="`LAB-L5`")])
        self.assert_outline_rule("partial", "OL010")

    def test_ol010_rejects_undefined_anchor(self) -> None:
        self.build_complete()
        self.write_stage(0, [self.stage_row(0, anchors="`PRJ-01-M02`")])
        self.assert_outline_rule("complete", "OL010")

    def test_ol010_rejects_non_contiguous_project_milestones(self) -> None:
        self.build_complete()
        self.write_project(1, milestone="PRJ-01-M02")
        self.assert_outline_rule("complete", "OL010")

    def test_ol010_rejects_missing_checkpoint_definition(self) -> None:
        self.build_complete()
        rows = [
            [f"`CP-{stage:02d}`", f"`{stage:02d}`", f"`{stage:02d}.01`", "—", "完成阶段能力"]
            for stage in range(20)
        ]
        self.write_text(
            "学习路线/阶段检查点/README.md",
            controlled_table(
                ("检查点", "阶段", "所需章节", "实践锚点", "能力结果"), rows
            ),
        )
        self.assert_outline_rule("complete", "OL010")

    def test_ol010_rejects_out_of_order_checkpoint_definitions(self) -> None:
        self.build_complete()
        rows = [
            [f"`CP-{stage:02d}`", f"`{stage:02d}`", f"`{stage:02d}.01`", "—", "完成阶段能力"]
            for stage in range(21)
        ]
        rows[0], rows[1] = rows[1], rows[0]
        self.write_text(
            "学习路线/阶段检查点/README.md",
            controlled_table(
                ("检查点", "阶段", "所需章节", "实践锚点", "能力结果"), rows
            ),
        )
        self.assert_outline_rule("complete", "OL010")

    def test_ol010_rejects_lab_definition_in_wrong_level(self) -> None:
        self.build_complete()
        self.write_text(
            "实验手册/Level-2-综合实验/README.md", "# Level 2\n\n`LAB-L3`\n"
        )
        self.assert_outline_rule("complete", "OL010")

    def test_ol011_rejects_project_to_chapter_mapping_gap(self) -> None:
        self.build_complete()
        self.write_stage(9, [self.stage_row(9, anchors="—")])
        self.assert_outline_rule("complete", "OL011")

    def test_ol011_rejects_chapter_to_project_mapping_gap(self) -> None:
        self.build_complete()
        self.write_project(1, chapters=["08.01"])
        self.assert_outline_rule("complete", "OL011")

    def test_outline_diagnostics_are_deterministic(self) -> None:
        self.write_stage(0, [self.stage_row(0, prerequisites="`99.01`")])
        first = self.outline("partial")
        second = self.outline("partial")
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first, key=validator._error_sort_key))

    def test_cli_help_lists_four_outline_gates(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as caught:
            validator.main(["--help"])
        self.assertEqual(caught.exception.code, 0)
        for gate in ("partial", "catalogs", "views", "complete"):
            self.assertIn(gate, stdout.getvalue())

    def test_cli_partial_returns_zero_and_reports_outline_counts(self) -> None:
        stdout, stderr = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = validator.main([str(self.root), "--outline-gate", "partial"])
        except SystemExit as error:
            self.fail(f"partial CLI 不应由 argparse 提前退出：{error}")
        self.assertEqual(code, 0)
        self.assertIn("大纲门禁通过", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_cli_catalogs_returns_one_with_ol001_without_traceback(self) -> None:
        stdout, stderr = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = validator.main([str(self.root), "--outline-gate", "catalogs"])
        except SystemExit as error:
            self.fail(f"catalogs CLI 不应由 argparse 提前退出：{error}")
        self.assertEqual(code, 1)
        self.assertIn("OL001", stderr.getvalue())
        self.assertNotIn("Traceback", stdout.getvalue() + stderr.getvalue())

    def test_cli_rejects_unknown_outline_gate(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as caught:
            validator.main([str(self.root), "--outline-gate", "unknown"])
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("invalid choice", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
