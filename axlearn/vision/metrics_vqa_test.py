# Copyright © 2023 Apple Inc.

"""Tests VQA metrics."""
# pylint: disable=no-self-use,
from typing import List

from absl.testing import absltest, parameterized

from axlearn.vision.metrics_vqa import _get_normalizer, vqa_accuracy_score


class TestMetricsVQA(parameterized.TestCase):
    """Tests metric utils."""

    @parameterized.named_parameters(
        {"testcase_name": "answer_n/a", "answer": "n/a", "expected": "n"},
        {"testcase_name": "answer_no", "answer": "no", "expected": "no"},
        {"testcase_name": "answer_no_one", "answer": "no one", "expected": "no 1"},
        {"testcase_name": "answer_yes", "answer": "yes", "expected": "yes"},
        {"testcase_name": "digit_0-0", "answer": "0-0", "expected": "0 0"},
        {"testcase_name": "digit_0-9", "answer": "0-9", "expected": "0 9"},
        {"testcase_name": "digit_02/12/2011", "answer": "02/12/2011", "expected": "02 12 2011"},
        {"testcase_name": "digit_07-23-98", "answer": "07-23-98", "expected": "07 23 98"},
        {"testcase_name": "digit_1/4", "answer": "1/4", "expected": "1 4"},
        {"testcase_name": "digit_10-2", "answer": "10-2", "expected": "10 2"},
        {"testcase_name": "digit_11/30/98", "answer": "11/30/98", "expected": "11 30 98"},
        {"testcase_name": "digit_2-1", "answer": "2-1", "expected": "2 1"},
        {"testcase_name": "digit_20+", "answer": "20+", "expected": "20"},
        {"testcase_name": "digit_2008/12/07", "answer": "2008/12/07", "expected": "2008 12 07"},
        {"testcase_name": "digit_333-3333", "answer": "333-3333", "expected": "333 3333"},
        {"testcase_name": "digit_388", "answer": "388", "expected": "388"},
        {"testcase_name": "digit_4", "answer": "4", "expected": "4"},
        {"testcase_name": "digit_4-5", "answer": "4-5", "expected": "4 5"},
        {"testcase_name": "digit_4/5", "answer": "4/5", "expected": "4 5"},
        {"testcase_name": "digit_5", "answer": "5", "expected": "5"},
        {"testcase_name": "digit_658-7245", "answer": "658-7245", "expected": "658 7245"},
        {"testcase_name": "digit_6_fifty-five", "answer": "6 fifty-five", "expected": "6 fifty 5"},
        {"testcase_name": "digit_8", "answer": "8", "expected": "8"},
        {"testcase_name": "digit_8_-_2", "answer": "8 - 2", "expected": "8 2"},
        {"testcase_name": "digit_none", "answer": "none", "expected": "0"},
        {"testcase_name": "empty", "answer": "", "expected": ""},
        {"testcase_name": "letter_a", "answer": "a", "expected": ""},
        {"testcase_name": "multi_1", "answer": "pennette rigate", "expected": "pennette rigate"},
        {"testcase_name": "multi_10", "answer": "crock-pot", "expected": "crock pot"},
        {"testcase_name": "multi_11", "answer": "cs-drz", "expected": "cs drz"},
        {"testcase_name": "multi_12", "answer": "horse, man", "expected": "horse man"},
        {"testcase_name": "multi_13", "answer": "june 29, 2013", "expected": "june 29 2013"},
        {"testcase_name": "multi_14", "answer": "full/0136", "expected": "full 0136"},
        {"testcase_name": "multi_15", "answer": "t-shirt", "expected": "t shirt"},
        {"testcase_name": "multi_16", "answer": "t-shirts", "expected": "t shirts"},
        {
            "testcase_name": "multi_2",
            "answer": "streamers_and_fake_records",
            "expected": "streamers and fake records",
        },
        {"testcase_name": "multi_3", "answer": "stop_sign", "expected": "stop sign"},
        {
            "testcase_name": "multi_4",
            "answer": "1980 harley-davidson",
            "expected": "1980 harley davidson",
        },
        {
            "testcase_name": "multi_5",
            "answer": "6 flowering plants, too many individual flowers to count",
            "expected": "6 flowering plants too many individual flowers to count",
        },
        {"testcase_name": "multi_6", "answer": "black/white", "expected": "black white"},
        {"testcase_name": "multi_7", "answer": "blue, gray", "expected": "blue gray"},
        {
            "testcase_name": "multi_8",
            "answer": "blueberry, strawberry and banana",
            "expected": "blueberry strawberry and banana",
        },
        {
            "testcase_name": "multi_9",
            "answer": "chicken, rice, vegetables",
            "expected": "chicken rice vegetables",
        },
        {"testcase_name": "punct_!", "answer": "hammer time!", "expected": "hammer time"},
        {"testcase_name": "punct_?", "answer": "?", "expected": ""},
        {"testcase_name": "punct_???", "answer": "???", "expected": ""},
        {"testcase_name": "token1", "answer": "someone", "expected": "someone"},
        {"testcase_name": "token2", "answer": "skateboard", "expected": "skateboard"},
    )
    def test_en_normalizer(self, answer: str, expected: str):
        normalizer = _get_normalizer(lang="en")
        assert normalizer(answer) == expected

    @parameterized.named_parameters(
        {
            "testcase_name": "down",
            "answer": "down",
            "gt_answers": [
                "down",
                "down",
                "at table",
                "stakeboard",
                "down",
                "table",
                "down",
                "down",
                "down",
                "down",
            ],
            "expected": 1.0,
        },
        {
            "testcase_name": "none",
            "answer": "none",
            "gt_answers": [
                "panther",
                "none",
                "leather",
                "dog",
                "cat",
                "none",
                "none",
                "none",
                "none",
                "dog",
            ],
            "expected": 1.0,
        },
        {
            "testcase_name": "a",
            "answer": "a",
            "gt_answers": [
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
                "a",
            ],
            "expected": 1.0,
        },
        {
            "testcase_name": "1",
            "answer": "1",
            "gt_answers": ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
            "expected": 1.0,
        },
        {
            "testcase_name": "1_mixed",
            "answer": "1",
            "gt_answers": ["3", "3", "3", "1", "3", "3", "3", "1", "1", "1"],
            "expected": 1.0,
        },
        {
            "testcase_name": "100",
            "answer": "100",
            "gt_answers": [
                "about 100",
                "100",
                "0",
                "0",
                "thousands",
                "1",
                "0",
                "100",
                "many",
                "unknown",
            ],
            "expected": 0.6,
        },
        {
            "testcase_name": "3:18",
            "answer": "3:18",
            "gt_answers": [
                "10:20",
                "10:00",
                "10:20",
                "10 19",
                "10:19",
                "10:20",
                "10 19",
                "3:18",
                "10:20",
                "10:19",
            ],
            "expected": 0.3,
        },
        {
            "testcase_name": "lots",
            "answer": "lots",
            "gt_answers": [
                "50",
                "lots",
                "over 60",
                "several",
                "55",
                "many",
                "78",
                "36",
                "2000",
                "50",
            ],
            "expected": 0.3,
        },
        {
            "testcase_name": "maybe",
            "answer": "maybe",
            "gt_answers": ["no", "yes", "yes", "no", "yes", "maybe", "yes", "yes", "yes", "yes"],
            "expected": 0.3,
        },
        {
            "testcase_name": "russian",
            "answer": "russian",
            "gt_answers": [
                "english",
                "french",
                "german",
                "russian",
                "latin",
                "russian",
                "russian",
                "latin",
                "latin",
                "russian",
            ],
            "expected": 1.0,
        },
        {
            "testcase_name": "shamrock",
            "answer": "shamrock",
            "gt_answers": [
                "logo",
                "shamrock",
                "shamrock",
                "shamrock",
                "shamrock",
                "shamrock",
                "shamrock",
                "clover",
                "clover",
                "shamrock",
            ],
            "expected": 1.0,
        },
        {
            "testcase_name": "yes_2",
            "answer": "yes",
            "gt_answers": ["yes", "yes", "yes", "yes", "yes", "yes", "yes", "yes", "no", "yes"],
            "expected": 1.0,
        },
        {
            "testcase_name": "don't shoot",
            "answer": "don't shoot",
            "gt_answers": [
                "don't shoot",
                "don't shoot",
                "shooting",
                "stop",
                "stop",
                "surrender",
                "i surrender",
                "surrender",
                "hands up",
                "gun",
            ],
            "expected": 0.6,
        },
        {
            "testcase_name": "toilet paper",
            "answer": "toilet paper",
            "gt_answers": [
                "toilet paper",
                "nothing",
                "toilet paper",
                "nothing",
                "paper",
                "handle",
                "toilet bowl cleaner",
                "valve",
                "toilet paper",
                "nothing",
            ],
            "expected": 0.9,
        },
        {
            "testcase_name": "yellow and blue",
            "answer": "yellow and blue",
            "gt_answers": [
                "yellow, blue, purple",
                "yellow, blue, purple, and white",
                "purple, blue, yellow, white, and gray",
                "yellow, blue, purple and white",
                "purple, blue, white, yellow",
                "yellow, purple, blue, white",
                "yellow and blue",
                "purple blue yellow",
                "yellow, blue, purple",
                "purple, blue, and yellow",
            ],
            "expected": 0.3,
        },
    )
    def test_sample_vqa_match_score(self, answer: str, gt_answers: List[str], expected: float):
        assert vqa_accuracy_score(answer=answer, gt_answers=gt_answers) == expected


if __name__ == "__main__":
    absltest.main()