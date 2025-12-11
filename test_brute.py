import pytest
from brute import Brute


def describe_brute_once():
    def it_returns_true_when_called_with_correct_password():
        b = Brute("password")
        assert b.bruteOnce("password") == True

    def it_returns_false_when_called_with_incorrect_password():
        b = Brute("password")
        assert b.bruteOnce("foobar") == False

    def it_works_when_called_with_empty_string():
        b = Brute("")
        assert b.bruteOnce("") == True


def describe_brute_many():
    def it_returns_positive_number_if_password_guessed_correctly(mocker):
        b = Brute("password")
        mock_guess = mocker.patch(
            "brute.Brute.randomGuess", return_value="password")
        assert b.bruteMany(100) > 0
        mock_guess.assert_called_once()

    def it_returns_negative_one_if_password_never_guessed(mocker):
        b = Brute("password")
        mock_guess = mocker.patch(
            "brute.Brute.randomGuess", return_value="username")
        assert b.bruteMany(100) == -1
        assert mock_guess.call_count == 100
