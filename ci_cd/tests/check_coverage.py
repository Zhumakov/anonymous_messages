import json
import sys

def check_coverage(json_file_path, min_coverage):
    """Checks if the coverage percentage in the given JSON file
    is greater than or equal to the specified minimum.

    Args:
        json_file_path: Path to the coverage.json file.
        min_coverage: The minimum acceptable coverage percentage.

    Returns:
        True if coverage is sufficient, False otherwise.
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        covered_lines = data['totals']['covered_lines']
        missing_lines = data['totals']['missing_lines']
        total_lines = covered_lines + missing_lines

        if total_lines == 0:
            coverage_percentage = 100.0  # Avoid division by zero
        else:
            coverage_percentage = (covered_lines / total_lines) * 100

        print(f"Coverage: {coverage_percentage:.2f}%")
        return coverage_percentage >= min_coverage

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error processing coverage file: {e}")
        return False

if __name__ == "__main__":
    COVERAGE_FILE = "coverage/coverage.json" # Укажите путь к вашему coverage.json
    MIN_COVERAGE = 80.0

    if len(sys.argv) > 1:
        COVERAGE_FILE = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            MIN_COVERAGE = float(sys.argv[2])
        except ValueError:
            print("Invalid minimum coverage value provided. Using default 80.0")
            MIN_COVERAGE = 80.0

    if check_coverage(COVERAGE_FILE, MIN_COVERAGE):
        print("Coverage check passed!")
        sys.exit(0)  # Exit with success code
    else:
        print("Coverage check failed!")
        sys.exit(1)  # Exit with failure code
