import pytest

from atax import ATax


@pytest.mark.parametrize(
    "tax_table_number,gross_monthly_salary,expected_tax_deduction",
    [
        (29, 0, 0),
        (29, 1, 0),
        (29, 1600, 0),
        (29, 1601, 117),
        (29, 40000, 9006),
        (29, 40001, 9064),
        (29, 80000, 28442),
        (29, 80001, round(0.36 * 80001)),  # NOTE: Behavior changes at this salary level
        (29, 100000, round(0.39 * 100000)),
        (29, 200000, round(0.44 * 200000)),
        (30, 0, 0),
        (30, 1, 0),
        (30, 1600, 0),
        (30, 1601, 117),
        (30, 40000, 9314),
        (30, 40001, 9374),
        (30, 80000, 29150),
        (30, 80001, round(0.36 * 80001)),  # NOTE: Behavior changes at this salary level
        (30, 100000, round(0.40 * 100000)),
        (30, 200000, round(0.45 * 200000)),
    ],
)
def test_lookup_default_tax_table(
    tax_table_number, gross_monthly_salary, expected_tax_deduction
):
    atax = ATax(tax_table_number)
    assert atax.get(gross_monthly_salary) == expected_tax_deduction


@pytest.mark.parametrize(
    "age,gross_monthly_salary,expected_tax_deduction",
    [
        (64, 35001, 7874),
        (65, 35001, 5280),
    ],
)
def test_lookup_tax_table_varying_age(
    age, gross_monthly_salary, expected_tax_deduction
):
    atax = ATax(table_number=30, age=age)
    assert atax.get(gross_monthly_salary) == expected_tax_deduction



@pytest.mark.parametrize(
    "age,gross_monthly_salary,expected_tax_deduction",
    [
        (64, 35001, 7874),
        (65, 35001, 5280),
    ],
)
def test_lookup_tax_table_varying_age(
    age, gross_monthly_salary, expected_tax_deduction
):
    atax = ATax(table_number=30, age=age)
    assert atax.get(gross_monthly_salary) == expected_tax_deduction


@pytest.mark.parametrize(
    "income_year,gross_monthly_salary,expected_tax_deduction",
    [
        (2021, 35001, 7874),
        (2022, 35001, 7708),
    ],
)
def test_lookup_tax_table_varying_income_year(
    income_year, gross_monthly_salary, expected_tax_deduction
):
    atax = ATax(table_number=30, age=64, income_year=income_year)
    assert atax.get(gross_monthly_salary) == expected_tax_deduction
