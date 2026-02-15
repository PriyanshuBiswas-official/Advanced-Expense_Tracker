import csv
from datetime import datetime

import pytest

from project import check_balance, print_by_date, print_by_amount, print_by_name


def write_expenses_file(path, rows):
    with open(path / "expenses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "description", "amount"])
        writer.writerows(rows)


def write_ledger_file(path, balance_values):
    with open(path / "ledger.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["balance"])
        for b in balance_values:
            writer.writerow([b])


def test_check_balance_simple(tmp_path, monkeypatch):
    write_ledger_file(tmp_path, ["50"])
    monkeypatch.chdir(tmp_path)
    assert check_balance() == pytest.approx(50.0)


def test_print_by_date_no_results(tmp_path, monkeypatch, capsys):
    rows = [["2024-01-01", "Groceries", "Apples", "5.00"]]
    write_expenses_file(tmp_path, rows)
    monkeypatch.chdir(tmp_path)
    start = datetime.strptime("2025-01-01", "%Y-%m-%d")
    end = datetime.strptime("2025-12-31", "%Y-%m-%d")
    print_by_date(start, end)
    out = capsys.readouterr().out
    assert "No expenses found between" in out


def test_print_by_amount_no_results(tmp_path, monkeypatch, capsys):
    rows = [["2024-01-01", "Groceries", "Apples", "5.00"]]
    write_expenses_file(tmp_path, rows)
    monkeypatch.chdir(tmp_path)
    print_by_amount(1000)
    out = capsys.readouterr().out
    assert "No expenses found above" in out


def test_print_by_name_no_results(tmp_path, monkeypatch, capsys):
    rows = [["2024-01-01", "Groceries", "Apples", "5.00"]]
    write_expenses_file(tmp_path, rows)
    monkeypatch.chdir(tmp_path)
    print_by_name("Banana")
    out = capsys.readouterr().out
    assert "No expenses found with" in out
