from logic_utils import validate_guess, build_investigation_report

TEST_CASES = [
    {"guess": 50, "secret": 50, "low": 1, "high": 100, "expected_status": "Win"},
    {"guess": 40, "secret": 50, "low": 1, "high": 100, "expected_status": "Too Low"},
    {"guess": 60, "secret": 50, "low": 1, "high": 100, "expected_status": "Too High"},
    {"guess": 0, "secret": 50, "low": 1, "high": 100, "expected_status": "invalid"},
    {"guess": 101, "secret": 50, "low": 1, "high": 100, "expected_status": "invalid"},
]

def run_evaluation():
    passed = 0

    for i, case in enumerate(TEST_CASES, start=1):
        guess = case["guess"]
        secret = case["secret"]
        low = case["low"]
        high = case["high"]
        expected = case["expected_status"]

        valid, _ = validate_guess(guess, low, high)

        if not valid:
            actual = "invalid"
        else:
            report = build_investigation_report(guess, secret, "Normal")
            actual = report["status"]

        if actual == expected:
            print(f"PASS test {i}: expected {expected}, got {actual}")
            passed += 1
        else:
            print(f"FAIL test {i}: expected {expected}, got {actual}")

    print(f"\nSummary: {passed}/{len(TEST_CASES)} tests passed")


if __name__ == "__main__":
    run_evaluation()