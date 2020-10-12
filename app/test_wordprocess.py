import pytest
import wordprocess

def test_is_palindrome():
    assert wordprocess.is_palindrome('madam') == True
    assert wordprocess.is_palindrome('1') == True
    assert wordprocess.is_palindrome('mister') == False

def test_merge_counts():
    assert wordprocess.merge_counts({'WORD_COUNTS':{'abc':1, 'def':1, 'madam': 1}, 'PALINDROMS': 1, 'TOTAL':3, 'LONGEST': ['madam'], 'TOTAL_LEN': 11 },{'WORD_COUNTS':{'ghost':1,'rocker':1, 'madam': 1}, 'PALINDROMS': 1, 'TOTAL':3, 'LONGEST': ['rocker'], 'TOTAL_LEN': 16 }) == {'WORD_COUNTS':{'abc':1, 'def':1, 'madam': 2, 'ghost':1,'rocker':1 }, 'PALINDROMS': 2, 'TOTAL':6, 'LONGEST': ['rocker'], 'TOTAL_LEN': 27, 'AVG_LENGHT': 4 }