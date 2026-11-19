import pytest
from hypothesis import given, strategies as st
from mobile_data_plan import parse_plan, usage_average, payable_bill


# TEST 1: parse_plan()

@given(
    plan=st.text(
        alphabet=st.characters(whitelist_categories=("Ll", "Lu")),
        min_size=1,
        max_size=12
    ),
    gb=st.floats(min_value=0.01, max_value=1000,
                 allow_nan=False, allow_infinity=False)
)
def test_parse_plan_valid_input(plan, gb):
    result = parse_plan(f"{plan}:{gb}")
    assert result == (plan.title(), gb)


@given(st.text().filter(lambda s: s.count(":") != 1))
def test_parse_plan_invalid_separator(s):
    with pytest.raises(ValueError):
        parse_plan(s)


@given(st.sampled_from([
    "", ":5", "standard:", "standard:abc",
    "standard:-5", "standard:nan", "standard:inf"
]))
def test_parse_plan_invalid_values(s):
    with pytest.raises(ValueError):
        parse_plan(s)


# TEST 2: usage_average()

@given(
    st.lists(st.integers(min_value=0, max_value=10000),
             min_size=1, max_size=20)
)
def test_usage_average_valid_input(values):
    csv = ",".join(str(value) for value in values)
    expected = sum(values) // len(values)
    assert usage_average(csv) == expected


@given(
    st.lists(
        st.one_of(
            st.integers(min_value=0, max_value=10000).map(str),
            st.just("")
        ),
        min_size=1,
        max_size=8
    ).filter(lambda parts: "" in parts).map(",".join)
)
def test_usage_average_empty_values(s):
    with pytest.raises(ValueError):
        usage_average(s)


@given(st.integers(min_value=-10000, max_value=-1))
def test_usage_average_negative_values(value):
    with pytest.raises(ValueError):
        usage_average(f"{value},100")


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1))
def test_usage_average_non_numeric_values(s):
    with pytest.raises(ValueError):
        usage_average(s + ",100")


# TEST 3: payable_bill()

@given(
    bill=st.floats(min_value=0.01, max_value=100000,
                   allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0, max_value=100000,
                       allow_nan=False, allow_infinity=False)
)
def test_payable_bill_valid_input(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result == pytest.approx(max(bill * 1.18 - discount, 0))


@given(st.text().filter(lambda s: s.count("|") != 1))
def test_payable_bill_invalid_separator(s):
    with pytest.raises(ValueError):
        payable_bill(s)


@given(st.sampled_from([
    "", "abc|50", "399|abc", "-100|20",
    "399|-50", "nan|10", "inf|10"
]))
def test_payable_bill_invalid_values(s):
    with pytest.raises(ValueError):
        payable_bill(s)
