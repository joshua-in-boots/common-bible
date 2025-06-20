#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 생성기 모듈 테스트
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
from src.html_generator import HTMLGenerator
from src.config import config


class TestHTMLGenerator(unittest.TestCase):
    """HTML 생성기 테스트 클래스"""
    
    def setUp(self):
        """테스트 준비"""
        # 템플릿 디렉토리 확인
        self.template_dir = os.path.join(PROJECT_ROOT, 'templates')
        self.template_file = os.path.join(self.template_dir, 'chapter_template.html')
        
        # 테스트용 출력 디렉토리
        self.output_dir = os.path.join(PROJECT_ROOT, 'tests', 'output')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 테스트 템플릿이 없으면 스킵
        if not os.path.exists(self.template_file):
            self.skipTest(f"템플릿 파일이 없습니다: {self.template_file}")
    
    def test_html_generator_init(self):
        """생성기 초기화 테스트"""
        generator = HTMLGenerator(self.template_dir)
        
        self.assertEqual(generator.template_dir, self.template_dir)
        self.assertTrue(hasattr(generator, 'jinja_env'))
        self.assertTrue(hasattr(generator, 'output_dir'))
    
    def test_generate_verse_html(self):
        """절 HTML 생성 테스트"""
        # 절 객체 생성
        verse = Verse(number=1, text="한처음에 하느님께서 하늘과 땅을 지어내셨다.")
        verse.id = "창세-1-1"
        
        html = verse.to_html()
        
        # HTML 요소 확인
        self.assertIn('<span class="verse"', html)
        self.assertIn('<span class="verse-number"', html)
        self.assertIn('aria-hidden="true"', html)
        self.assertIn('한처음에 하느님께서', html)
    
    def test_generate_chapter_html(self):
        """장 HTML 생성 테스트"""
        # 장 객체 생성
        chapter = Chapter(
            book_name="창세기", 
            chapter_number=1,
            book_abbr="창세",
            id="창세-1"
        )
        
        # 절 추가
        verse1 = Verse(number=1, text="한처음에 하느님께서 하늘과 땅을 지어내셨다.")
        verse2 = Verse(number=2, text="¶ 땅은 아직 모양을 갖추지 않고 비어 있었는데, 어둠이 깊은 물 위에 뒤덮여 있었다.")
        verse3 = Verse(number=3, text="하느님께서 \"빛이 생겨라.\" 하시자 빛이 생겨났다.")
        
        chapter.add_verse(verse1)
        chapter.add_verse(verse2)
        chapter.add_verse(verse3)
        
        # HTML 생성기
        generator = HTMLGenerator(self.template_dir)
        generator.output_dir = self.output_dir
        
        try:
            # HTML 생성
            html_content = generator.generate_chapter_html(chapter)
            
            # 기본 검증
            self.assertIsNotNone(html_content)
            self.assertIn('<!DOCTYPE html>', html_content)
            self.assertIn('<html lang="ko">', html_content)
            self.assertIn('창세기 1장', html_content)
            
            # 절 내용 검증
            self.assertIn('한처음에 하느님께서 하늘과 땅을 지어내셨다', html_content)
            self.assertIn('빛이 생겨라', html_content)
            
            # 파일로 저장 테스트
            file_path = generator._save_html_file(chapter.id, html_content)
            self.assertTrue(os.path.exists(file_path))
            
        except Exception as e:
            self.fail(f"HTML 생성 중 예외 발생: {e}")
    
    def test_fallback_html_generation(self):
        """템플릿 없을 때 기본 HTML 생성 테스트"""
        # 가짜 템플릿 디렉토리로 초기화
        fake_dir = os.path.join(PROJECT_ROOT, 'tests', 'fake_templates')
        
        # 장 객체 생성
        chapter = Chapter(
            book_name="창세기", 
            chapter_number=1,
            book_abbr="창세",
            id="창세-1"
        )
        
        verse = Verse(number=1, text="테스트 절입니다.")
        chapter.add_verse(verse)
        
        # HTML 생성기
        generator = HTMLGenerator(fake_dir)
        generator.output_dir = self.output_dir
        
        # 기본 HTML 생성 시도
        html_content = generator._generate_default_html(chapter)
        
        # 기본 검증
        self.assertIsNotNone(html_content)
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('창세기 1장', html_content)
        self.assertIn('테스트 절입니다', html_content)


if __name__ == '__main__':
    unittest.main()
