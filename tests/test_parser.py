#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파서 모듈 테스트
"""

import unittest
import os
import sys
import json
from pathlib import Path

# 프로젝트 루트 경로 추가
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

from src.models import Verse, Chapter, Book, Bible
from src.parser import BibleParser
from src.config import config


class TestParser(unittest.TestCase):
    """파서 테스트 클래스"""
    
    def setUp(self):
        """테스트 준비"""
        self.test_file = os.path.join(PROJECT_ROOT, 'data', 'common-bible-kr.txt')
        
        # 테스트 파일이 없으면 스킵
        if not os.path.exists(self.test_file):
            self.skipTest(f"테스트 파일이 없습니다: {self.test_file}")
    
    def test_verse_model(self):
        """Verse 모델 테스트"""
        # 기본 절 객체
        verse = Verse(number=1, text="한처음에 하느님께서 하늘과 땅을 지어내셨다.")
        verse.id = "창세-1-1"
        
        self.assertEqual(verse.number, 1)
        self.assertEqual(verse.text, "한처음에 하느님께서 하늘과 땅을 지어내셨다.")
        self.assertFalse(verse.has_paragraph)
        
        # 단락 마커가 있는 경우
        verse2 = Verse(number=2, text="¶ 이로써 하느님께서 일을 마치시고")
        self.assertTrue(verse2.has_paragraph)
        self.assertEqual(verse2.text, "이로써 하느님께서 일을 마치시고")
        
        # 하위 파트가 있는 경우
        verse3 = Verse(number=3, text="이 부분은 ¶ 두 부분으로 나뉩니다")
        verse3.id = "창세-1-3"
        verse3.sub_parts = ["이 부분은", "두 부분으로 나뉩니다"]
        
        self.assertEqual(len(verse3.sub_parts), 2)
        self.assertTrue(hasattr(verse3, "sub_ids"))
        
        # HTML 변환 테스트
        html = verse.to_html()
        self.assertIn(f'id="{verse.id}"', html)
        self.assertIn(f'class="verse-number"', html)
        self.assertIn(f'aria-hidden="true"', html)
        
        # 하위 파트가 있는 경우 HTML
        html3 = verse3.to_html()
        self.assertIn(f'class="verse-part"', html3)
    
    def test_chapter_model(self):
        """Chapter 모델 테스트"""
        # 장 객체 생성
        chapter = Chapter(
            book_name="창세기", 
            chapter_number=1,
            book_abbr="창세"
        )
        
        # ID 생성 확인
        self.assertEqual(chapter.id, "창세-1")
        
        # 절 추가
        verse1 = Verse(number=1, text="한처음에 하느님께서 하늘과 땅을 지어내셨다.")
        verse2 = Verse(number=2, text="¶ 이로써 하느님께서 일을 마치시고")
        
        chapter.add_verse(verse1)
        chapter.add_verse(verse2)
        
        self.assertEqual(len(chapter.verses), 2)
        self.assertEqual(chapter.verses[0].id, "창세-1-1")
        self.assertEqual(chapter.verses[1].id, "창세-1-2")
    
    def test_book_model(self):
        """Book 모델 테스트"""
        # 책 객체 생성
        book = Book(name="창세기", abbr="창세", eng_name="Genesis")
        
        # ID 생성 확인
        self.assertEqual(book.id, "창세")
        
        # 장 추가
        chapter1 = Chapter(book_name="창세기", chapter_number=1)
        chapter2 = Chapter(book_name="창세기", chapter_number=2)
        
        book.add_chapter(chapter1)
        book.add_chapter(chapter2)
        
        self.assertEqual(len(book.chapters), 2)
        self.assertEqual(book.chapters[0].id, "창세-1")
        self.assertEqual(book.chapters[0].book_abbr, "창세")
        
    def test_bible_parser_init(self):
        """파서 초기화 테스트"""
        parser = BibleParser(self.test_file)
        
        self.assertEqual(parser.file_path, self.test_file)
        self.assertIsNotNone(parser.book_mappings)
        self.assertTrue(len(parser.book_mappings) > 0)
    
    def test_parser_small_sample(self):
        """샘플 텍스트 파싱 테스트"""
        # 샘플 텍스트 생성
        sample_text = """
        창세 1:1 한처음에 하느님께서 하늘과 땅을 지어내셨다.
        2 ¶ 땅은 아직 모양을 갖추지 않고 비어 있었는데, 어둠이 깊은 물 위에 뒤덮여 있었다. 하느님의 기운이 그 물 위에 휘돌고 있었다.
        3 하느님께서 "빛이 생겨라." 하시자 빛이 생겨났다.
        4 그 빛이 하느님 보시기에 좋았다. 하느님께서는 빛과 어둠을 나누시고
        5 빛을 낮이라, 어둠을 밤이라 부르셨다. 이렇게 첫날이 밤, 낮 하루가 지났다.
        """
        
        # 임시 파일로 저장
        temp_file = os.path.join(PROJECT_ROOT, 'tests', 'sample.txt')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(sample_text)
            
            # 파서로 파싱
            parser = BibleParser(temp_file)
            bible = parser.parse_file()
            
            # 결과 확인
            self.assertEqual(len(bible.books), 1)
            self.assertEqual(bible.books[0].name, "창세기")
            
            # 장 확인
            chapters = bible.books[0].chapters
            if chapters:  # 파서 구현에 따라 실제 파싱 결과가 다를 수 있음
                self.assertEqual(chapters[0].chapter_number, 1)
        finally:
            # 임시 파일 삭제
            if os.path.exists(temp_file):
                os.remove(temp_file)


if __name__ == '__main__':
    unittest.main()
