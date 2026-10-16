"""Statement хуваагч — MySQL шаардахгүй."""

import pytest

from sqlrunner.splitter import SplitError, Statement, split_statements


def texts(source: str) -> list[str]:
    return [statement.text for statement in split_statements(source)]


def test_splits_on_semicolon_and_reports_lines() -> None:
    source = "USE delguur;\n\nSELECT *\nFROM baraa;\n"

    assert split_statements(source) == [
        Statement("USE delguur", 1),
        Statement("SELECT *\nFROM baraa", 3),
    ]


def test_trailing_statement_without_delimiter() -> None:
    assert texts("SELECT 1;\nSELECT 2") == ["SELECT 1", "SELECT 2"]


def test_empty_and_comment_only_input() -> None:
    assert split_statements("") == []
    assert split_statements("-- зөвхөн тайлбар\n/* бас */\n# энэ ч\n;;") == []


def test_leading_comment_is_not_part_of_statement_line() -> None:
    source = "-- 1. Бараа\n-- тайлбар\nSELECT ner FROM baraa;"

    assert split_statements(source) == [Statement("SELECT ner FROM baraa", 3)]


@pytest.mark.parametrize(
    "literal",
    [
        "'a;b'",
        "'it''s; ok'",
        "'it\\'s; ok'",
        '"a;b"',
        "`col;umn`",
        "'-- биш тайлбар'",
        "'/* биш */'",
    ],
)
def test_delimiter_inside_quotes_is_ignored(literal: str) -> None:
    assert texts(f"SELECT {literal};SELECT 2;") == [f"SELECT {literal}", "SELECT 2"]


def test_comments_hide_semicolons() -> None:
    source = "SELECT 1 -- ; энд биш\n, 2; /* ; */ SELECT 3 # ;\n;"

    assert texts(source) == ["SELECT 1 -- ; энд биш\n, 2", "SELECT 3 # ;"]


def test_double_dash_without_space_is_an_operator() -> None:
    assert texts("SELECT 5--2;") == ["SELECT 5--2"]


def test_executable_comment_starts_a_statement() -> None:
    assert texts("/*!40101 SET NAMES utf8mb4 */;") == ["/*!40101 SET NAMES utf8mb4 */"]


def test_delimiter_command_for_procedure_body() -> None:
    source = """\
USE delguur;

DELIMITER $$
CREATE PROCEDURE p(IN p_id INT)
BEGIN
    SELECT 1;
    SELECT 'а;б';
END$$
DELIMITER ;

CALL p(1);
"""
    statements = split_statements(source)

    assert [statement.line for statement in statements] == [1, 4, 11]
    assert statements[1].text == (
        "CREATE PROCEDURE p(IN p_id INT)\nBEGIN\n    SELECT 1;\n    SELECT 'а;б';\nEND"
    )
    assert statements[2].text == "CALL p(1)"


def test_delimiter_command_is_case_insensitive_and_any_token() -> None:
    source = "delimiter //\nCREATE TRIGGER t BEFORE INSERT ON x FOR EACH ROW BEGIN SET @a=1; END//"

    assert texts(source) == [
        "CREATE TRIGGER t BEFORE INSERT ON x FOR EACH ROW BEGIN SET @a=1; END",
    ]


def test_delimiter_word_inside_statement_is_not_a_command() -> None:
    assert texts("SELECT 'x' AS\ndelimiter ;") == ["SELECT 'x' AS\ndelimiter"]


def test_delimiter_without_token_is_an_error() -> None:
    with pytest.raises(SplitError) as error:
        split_statements("SELECT 1;\nDELIMITER \n")

    assert error.value.line == 2


def test_crlf_line_endings() -> None:
    assert split_statements("SELECT 1;\r\nSELECT 2;\r\n") == [
        Statement("SELECT 1", 1),
        Statement("SELECT 2", 2),
    ]


def test_unterminated_quote_is_left_for_the_server() -> None:
    assert texts("SELECT 'дуусаагүй; SELECT 2;") == ["SELECT 'дуусаагүй; SELECT 2;"]
