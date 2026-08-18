from carrier_guidance.search_client import CarrierGuidanceSearchClient


def main() -> None:
    client = CarrierGuidanceSearchClient()

    for question in (
        "What should happen to lossOccurredWhen?",
        "What date format is required for date of loss?",
    ):
        print(f"\nQuestion: {question}")

        for result in client.hybrid_search(question):
            print(
                f"- {result.source_file} | {result.section} "
                f"| score={result.search_score}"
            )


if __name__ == "__main__":
    main()