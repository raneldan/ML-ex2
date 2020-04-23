from typing import List


def check_classification(classified_digits: List[int], test_labels: List[int]) -> int:
    correct_counter: int = 0
    assert len(classified_digits) == len(test_labels)
    total_lines = len(classified_digits)
    for index, value in enumerate(classified_digits):
        if test_labels[index] == value:
            correct_counter += 1
    precent = correct_counter / total_lines
    print("Percentage is="+str(precent))
    return correct_counter / total_lines


# returns line to digit
def classify_digits(binary_classification_results: List[List[bool]]) -> List[int]:
    classified_digits: List[int] = []
    number_of_two_or_more = 0
    number_of_zero = 0
    number_of_lines = len(binary_classification_results[0])
    number_of_digits = len(binary_classification_results)
    for line_number in range(number_of_lines):
        found_digit: bool = False
        for digit in range(number_of_digits):
            digit_binary_classification_for_line = binary_classification_results[digit][line_number]
            if digit_binary_classification_for_line:
                if found_digit:
                    number_of_two_or_more += 1
                    print("Two classifications for line: " + str(line_number) + "with digit" + str(digit))
                else:
                    classified_digits.append(digit)
                    found_digit = True
        if not found_digit:
            print("No classification for line: " + str(line_number) + "classified to default to 8")
            number_of_zero += 1
            classified_digits.append(8)

    print("Number of lines is: " + str(number_of_lines))
    print("number of two or more classifications (BAD):" + str(number_of_two_or_more))
    print("number of two or more classifications (BAD):" + str(number_of_zero))
    return classified_digits


###TESTS:
good_binary_classification_results: List[bool] = [[0, 0, 0],  # 0
                                                  [0, 0, 1],  # 1
                                                  [0, 1, 0],  # 2
                                                  [0, 0, 0],  # 3
                                                  [0, 0, 0],  # 4
                                                  [0, 0, 0],  # 5
                                                  [0, 0, 0],  # 6
                                                  [1, 0, 0],  # 7
                                                  [0, 0, 0],  # 8
                                                  [0, 0, 0]]  # 9

no_classifications: List[bool] = [[0, 0, 0],  # 0
                                  [0, 0, 0],  # 1
                                  [0, 0, 0],  # 2
                                  [0, 0, 0],  # 3
                                  [0, 0, 0],  # 4
                                  [0, 0, 0],  # 5
                                  [0, 0, 0],  # 6
                                  [0, 0, 0],  # 7
                                  [0, 0, 0],  # 8
                                  [0, 0, 0]]  # 9
good_test_labels = [7, 2, 1]
bad_test_labels = [6, 5, 3]


def __classify_digits_test(binary_classification_results: List[List[bool]], test_labels1: List[int]) -> bool:
    classification = classify_digits(binary_classification_results)
    for index, value in enumerate(classification):
        if test_labels1[index] != value:
            return False
    return True



if __name__ == '__main__':
    print("*****************TRUE TEST*****************")
    assert __classify_digits_test(good_binary_classification_results, good_test_labels)
    classifications = classify_digits(good_binary_classification_results)
    assert 1 == check_classification(classifications, good_test_labels)
    print("*****************FALSE TEST*****************")
    assert not __classify_digits_test(good_binary_classification_results, bad_test_labels)
    print("********No Classification test*************")
    classifications = __classify_digits_test(no_classifications, good_test_labels)
    classifications = classify_digits(no_classifications)
    assert 0 == check_classification(classifications, good_test_labels)

    print("Success")
