import requests
import time

# ==========================
# Test Dataset
# ==========================

test_cases = [

    {
        "claim": "Lionel Messi won the 2022 FIFA World Cup.",
        "expected": "Supported"
    },

    {
        "claim": "Earth is flat.",
        "expected": "Refuted"
    },

    {
        "claim": "Water boils at 100 degrees Celsius.",
        "expected": "Supported"
    },

    {
        "claim": "Python is the best programming language.",
        "expected": "Opinion Analysis"
    },

    {
        "claim": "The Moon is made of cheese.",
        "expected": "Refuted"
    },

    {
        "claim": "Narendra Modi is the Prime Minister of India.",
        "expected": "Supported"
    },

    {
        "claim": "The Sun revolves around the Earth.",
        "expected": "Refuted"
    },

    {
        "claim": "Mount Everest is the tallest mountain in the world.",
        "expected": "Supported"
    },

    {
        "claim": "COVID-19 vaccines contain microchips.",
        "expected": "Refuted"
    },

    {
        "claim": "Lionel Messi is the greatest footballer.",
        "expected": "Opinion Analysis"
    }

]

# ==========================
# Statistics
# ==========================

correct = 0
total = len(test_cases)

total_time = 0
total_articles = 0
total_confidence = 0
confidence_count = 0

print("=" * 80)
print("FACTCHECK AI EVALUATION")
print("=" * 80)

# ==========================
# Run Tests
# ==========================

for i, case in enumerate(test_cases, start=1):

    claim = case["claim"]
    expected = case["expected"]

    start = time.time()

    response = requests.post(
        "https://factcheck-ai-62fu.onrender.com/check",
        json={
            "text": claim
        }
    )

    elapsed = time.time() - start

    total_time += elapsed

    if response.status_code != 200:

        print(f"\nTest {i}")
        print("Server Error")
        print(response.text)
        continue

    result = response.json()

    verdict = result.get("verdict", "Unknown")
    confidence = result.get("confidence", 0)
    articles = result.get("articles", [])

    if isinstance(confidence, int):
        total_confidence += confidence
        confidence_count += 1

    total_articles += len(articles)

    if verdict == expected:
        correct += 1
        status = "PASS"
    else:
        status = "FAIL"

    print("\n---------------------------------------------")

    print(f"Test {i}")

    print(f"Claim        : {claim}")

    print(f"Expected     : {expected}")

    print(f"Predicted    : {verdict}")

    print(f"Confidence   : {confidence}")

    print(f"Articles     : {len(articles)}")

    print(f"Response Time: {elapsed:.2f} sec")

    print(f"Result       : {status}")

# ==========================
# Final Statistics
# ==========================

accuracy = (correct / total) * 100

average_time = total_time / total

average_articles = total_articles / total

if confidence_count > 0:
    average_confidence = total_confidence / confidence_count
else:
    average_confidence = 0

print("\n")
print("=" * 80)

print("FINAL REPORT")

print("=" * 80)

print(f"Total Test Cases        : {total}")

print(f"Correct Predictions     : {correct}")

print(f"Accuracy                : {accuracy:.2f}%")

print(f"Average Response Time   : {average_time:.2f} sec")

print(f"Average Articles Found  : {average_articles:.2f}")

print(f"Average Confidence      : {average_confidence:.2f}%")

print("=" * 80)