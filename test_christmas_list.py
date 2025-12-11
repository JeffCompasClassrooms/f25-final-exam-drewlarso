import pytest
import os
import shutil
from christmas_list import ChristmasList


@pytest.fixture
def my_list():
    shutil.copyfile("christmas_list.pkl", "xmas_testing.db")
    yield ChristmasList("xmas_testing.db")
    os.remove("xmas_testing.db")


@pytest.fixture
def wishlist():
    return [
        {"name": "legos", "purchased": False},
        {"name": "puppy", "purchased": False},
        {"name": "coal", "purchased": False},
    ]


def describe_christmas_list():
    def describe_load():
        def test_load_items_works_with_regular_list(my_list, wishlist):
            assert my_list.loadItems() == []
            my_list.saveItems(wishlist)
            assert my_list.loadItems() == wishlist

        def test_load_items_works_with_big_duplicate_list(my_list, wishlist):
            big_wishlist = wishlist * 100
            my_list.saveItems(big_wishlist)
            assert my_list.loadItems() == big_wishlist

    def describe_save():
        def test_save_items_stores_correct_values(my_list, wishlist):
            assert my_list.loadItems() != wishlist
            my_list.saveItems(wishlist)
            assert my_list.loadItems() == wishlist

    def describe_add():
        def test_add_correctly_adds_items_to_database(my_list, wishlist):
            assert my_list.loadItems() == []
            for i in range(len(wishlist)):
                my_list.add(wishlist[i]["name"])
                assert my_list.loadItems() == wishlist[:i+1]

        def test_add_sets_purchased_to_false(my_list, wishlist):
            for i in range(len(wishlist)):
                my_list.add(wishlist[i]["name"])
                assert my_list.loadItems()[i]["purchased"] == False

    def describe_check_off():
        def test_check_off_sets_value_to_true(my_list, wishlist):
            my_list.saveItems(wishlist)
            for i in range(len(wishlist)):
                my_list.check_off(wishlist[i]["name"])
                assert my_list.loadItems()[i]["purchased"] == True

        def test_check_off_ignores_invalid_names(my_list, wishlist):
            my_list.saveItems(wishlist)
            for item in ["rusty nail", "old tire", "boot", "tin can"]:
                my_list.check_off(item)

            for i in range(len(wishlist)):
                my_list.add(wishlist[i]["name"])
                assert my_list.loadItems()[i]["purchased"] == False

    def describe_remove():
        def test_remove_gets_rid_of_valid_item(my_list, wishlist):
            my_list.saveItems(wishlist)
            assert my_list.loadItems() == wishlist
            my_list.remove(wishlist[0]["name"])
            assert my_list.loadItems() == wishlist[1:]

        def test_remove_ignores_invalid_item(my_list, wishlist):
            my_list.saveItems(wishlist)
            assert my_list.loadItems() == wishlist
            my_list.remove("tin can")
            assert my_list.loadItems() == wishlist

        def test_remove_works_on_empty_list(my_list):
            assert my_list.loadItems() == []
            my_list.remove("tin can")
            assert my_list.loadItems() == []

        def test_remove_works_on_list_with_many_duplicates(my_list, wishlist):
            dupe_list = [wishlist[0] for i in range(10)]
            my_list.saveItems(dupe_list)
            assert my_list.loadItems() == dupe_list
            my_list.remove("legos")
            assert my_list.loadItems() == []

    def describe_print_list():
        def test_print_list_gives_correct_output_given_multiple_items(capsys, my_list, wishlist):
            my_list.saveItems(wishlist)
            my_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[_] legos\n[_] puppy\n[_] coal\n"

        def test_print_list_gives_correct_output_given_some_marked_off(capsys, my_list, wishlist):
            my_list.saveItems(wishlist)
            my_list.check_off("legos")
            my_list.check_off("puppy")
            my_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[x] legos\n[x] puppy\n[_] coal\n"

        def test_print_list_gives_correct_output_given_no_items(capsys, my_list):
            my_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == ""
