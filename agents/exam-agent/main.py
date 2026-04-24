import sys
from core.pipeline import run_exam_research


def main():
    query = "upcoming government exams in India 2026-2027"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

    print(f"🚀 Starting research for: {query}\n")

    result = run_exam_research(query)

    filename = "upcoming_exams_report.md"
    with open(filename, "w") as f:
        f.write(result["final_report"])

    print(f"\n✅ Research Complete! Report saved to '{filename}'")


if __name__ == "__main__":
    main()
