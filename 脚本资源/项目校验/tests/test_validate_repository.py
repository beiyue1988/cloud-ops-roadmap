from __future__ import annotations

import contextlib
import importlib.util
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

    def test_current_repository_passes(self) -> None:
        repository_root = Path(__file__).resolve().parents[3]
        errors = validator.validate_repository(repository_root)
        self.assertEqual(errors, [], "真实仓库诊断：\n" + "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
