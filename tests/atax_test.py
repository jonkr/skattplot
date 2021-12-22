import pytest

from skattplot.atax import ATax


def test_out_of_bounds():
    atax = ATax()
    with pytest.raises(AssertionError):
        atax.get(-1)


@pytest.mark.parametrize('gross_monthly_salary,expected_tax_deduction', [
    (0, 0),
    (1, 0),
    (1600, 0),
    (1601, 117),
    (40000, 9314),
    (40001, 9374),
    (80000, 29150),
    (80001, round(0.36 * 80001, 2)), # NOTE: Behavior changes at this salary level
    (100000, round(0.40 * 100000, 2)),
])
def test_lookup(
        gross_monthly_salary,
        expected_tax_deduction
    ):
    atax = ATax()
    assert atax.get(gross_monthly_salary) == expected_tax_deduction
