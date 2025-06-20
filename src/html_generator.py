#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 생성기 모듈

파싱된 성경 데이터를 기반으로 접근성을 고려한 HTML 파일을 생성합니다.
- 장별 HTML 생성
- 절 스타일 및 ID 적용
- 접근성 속성 추가
"""

import os
import json
import logging
import argparse
from typing import Dict, List, Optional, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from models import Bible, Book, Chapter, Verse
from config import config


class HTMLGenerator:
    """HTML 생성기 클래스"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        HTML 생성기 초기화
        
        Args:
            template_dir: 템플릿 디렉토리 경로 (기본값: config에서 설정된 경로)
        """
        self.logger = logging.getLogger(__name__)
        
        # 템플릿 디렉토리 설정
        if template_dir is None:
            template_dir = config.paths['templates_dir']
        self.template_dir = template_dir
        
        # Jinja2 환경 설정
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
        
        # 출력 디렉토리 설정
        self.output_dir = os.path.join(config.paths['output_dir'], 'html')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # 정적 파일 경로
        self.static_dir = config.paths['static_dir']
        
        self.logger.info(f"HTML 생성기 초기화: 템플릿 디렉토리={template_dir}")
    
    def generate_html_from_bible(self, bible: Bible) -> Dict[str, str]:
        """
        Bible 객체로부터 HTML 파일들 생성
        
        Args:
            bible: 변환할 Bible 객체
        
        Returns:
            파일 경로 사전 {장ID: HTML 파일 경로}
        """
        result = {}
        
        for book in bible.books:
            for chapter in book.chapters:
                html_content = self.generate_chapter_html(chapter)
                file_path = self._save_html_file(chapter.id, html_content)
                result[chapter.id] = file_path
        
        self.logger.info(f"전체 HTML 생성 완료: {len(result)}개 파일")
        return result
    
    def generate_html_from_json(self, json_dir: str) -> Dict[str, str]:
        """
        JSON 파일들로부터 HTML 파일들 생성
        
        Args:
            json_dir: JSON 파일 디렉토리
        
        Returns:
            파일 경로 사전 {장ID: HTML 파일 경로}
        """
        result = {}
        
        # JSON 디렉토리를 순회하며 파일 찾기
        for root, _, files in os.walk(json_dir):
            for file in files:
                if not file.endswith('.json'):
                    continue
                
                json_path = os.path.join(root, file)
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        chapter_data = json.load(f)
                    
                    # JSON을 Chapter 객체로 변환
                    chapter = self._create_chapter_from_json(chapter_data)
                    if chapter:
                        html_content = self.generate_chapter_html(chapter)
                        file_path = self._save_html_file(chapter.id, html_content)
                        result[chapter.id] = file_path
                except Exception as e:
                    self.logger.error(f"JSON 처리 실패: {json_path} - {e}")
        
        self.logger.info(f"JSON으로부터 HTML 생성 완료: {len(result)}개 파일")
        return result
    
    def _create_chapter_from_json(self, data: Dict[str, Any]) -> Optional[Chapter]:
        """
        JSON 데이터로부터 Chapter 객체 생성
        
        Args:
            data: 장 데이터 사전
        
        Returns:
            생성된 Chapter 객체 또는 None
        """
        try:
            # 기본 장 정보 추출
            chapter = Chapter(
                book_name=data['book_name'],
                chapter_number=data['chapter_number'],
                id=data['id'],
                book_abbr=data['book_abbr']
            )
            
            # 절 정보 추출
            for verse_data in data['verses']:
                verse = Verse(
                    number=verse_data['number'],
                    text=verse_data['text'],
                    has_paragraph=verse_data['has_paragraph'],
                    id=verse_data['id']
                )
                
                # 하위 파트 처리
                if 'sub_parts' in verse_data:
                    verse.sub_parts = verse_data['sub_parts']
                    if 'sub_ids' in verse_data:
                        verse.sub_ids = verse_data['sub_ids']
                
                chapter.add_verse(verse)
            
            return chapter
        except Exception as e:
            self.logger.error(f"Chapter 객체 생성 실패: {e}")
            return None
    
    def generate_chapter_html(self, chapter: Chapter) -> str:
        """
        장 객체로부터 HTML 생성
        
        Args:
            chapter: 변환할 Chapter 객체
        
        Returns:
            생성된 HTML 문자열
        """
        # 템플릿 로드
        try:
            template = self.jinja_env.get_template('chapter_template.html')
        except Exception as e:
            self.logger.error(f"템플릿 로드 실패: {e}")
            # 기본 템플릿으로 폴백
            return self._generate_default_html(chapter)
        
        # CSS 및 JS 파일 경로
        css_path = os.path.join(self.static_dir, 'verse-style.css')
        js_path = os.path.join(self.static_dir, 'verse-navigator.js')
        
        # 상대 경로 계산
        css_rel_path = os.path.relpath(css_path, self.output_dir)
        js_rel_path = os.path.relpath(js_path, self.output_dir)
        
        # HTML 생성
        verses_html = self._generate_verses_html(chapter)
        
        context = {
            'book_name': chapter.book_name,
            'chapter_number': chapter.chapter_number,
            'chapter_id': chapter.id,
            'book_abbr': chapter.book_abbr,
            'verses_html': verses_html,
            'css_path': css_rel_path.replace('\\', '/'),
            'js_path': js_rel_path.replace('\\', '/')
        }
        
        return template.render(**context)
    
    def _generate_verses_html(self, chapter: Chapter) -> str:
        """
        장의 모든 절에 대한 HTML 생성
        
        Args:
            chapter: 변환할 Chapter 객체
        
        Returns:
            절들의 HTML 문자열
        """
        verses_html = []
        
        current_paragraph = []
        for verse in chapter.verses:
            # 단락 구분 처리
            verse_html = verse.to_html()
            
            if verse.has_paragraph and current_paragraph:
                # 이전 단락 종료
                p_html = f'<p class="paragraph">{" ".join(current_paragraph)}</p>'
                verses_html.append(p_html)
                current_paragraph = [verse_html]
            else:
                current_paragraph.append(verse_html)
        
        # 마지막 단락 처리
        if current_paragraph:
            p_html = f'<p class="paragraph">{" ".join(current_paragraph)}</p>'
            verses_html.append(p_html)
        
        return "\n".join(verses_html)
    
    def _generate_default_html(self, chapter: Chapter) -> str:
        """
        기본 HTML 템플릿 생성 (템플릿 로드 실패 시 대체용)
        
        Args:
            chapter: 변환할 Chapter 객체
        
        Returns:
            생성된 HTML 문자열
        """
        title = f"{chapter.book_name} {chapter.chapter_number}장"
        
        # 절 HTML 생성
        verses_html = self._generate_verses_html(chapter)
        
        # HTML 기본 구조
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../static/verse-style.css">
</head>
<body>
    <main>
        <article id="{chapter.id}" class="bible-chapter">
            <h1>{title}</h1>
            {verses_html}
        </article>
    </main>
    <script src="../static/verse-navigator.js"></script>
</body>
</html>
"""
        return html
    
    def _save_html_file(self, chapter_id: str, html_content: str) -> str:
        """
        생성된 HTML을 파일로 저장
        
        Args:
            chapter_id: 장 ID (예: "창세-1")
            html_content: HTML 내용
        
        Returns:
            저장된 파일 경로
        """
        # 파일 경로 생성
        file_name = f"{chapter_id}.html"
        output_path = os.path.join(self.output_dir, file_name)
        
        # 파일 저장
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.debug(f"HTML 파일 저장: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"HTML 파일 저장 실패: {output_path} - {e}")
            return ""


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(description='HTML 생성 도구')
    parser.add_argument('--chapters', '-c', help='장 JSON 파일 또는 디렉토리 경로')
    parser.add_argument('--bible', '-b', help='Bible JSON 파일 경로')
    parser.add_argument('--output', '-o', help='출력 디렉토리')
    parser.add_argument('--template', '-t', help='템플릿 디렉토리')
    args = parser.parse_args()
    
    # HTML 생성기 초기화
    generator = HTMLGenerator(args.template)
    
    # 출력 디렉토리 설정
    if args.output:
        generator.output_dir = args.output
        if not os.path.exists(args.output):
            os.makedirs(args.output)
    
    # 입력 소스에 따라 처리
    if args.chapters:
        path = args.chapters
        if os.path.isdir(path):
            generator.generate_html_from_json(path)
        elif os.path.isfile(path) and path.endswith('.json'):
            # 단일 JSON 파일 처리
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    chapter_data = json.load(f)
                chapter = generator._create_chapter_from_json(chapter_data)
                if chapter:
                    html_content = generator.generate_chapter_html(chapter)
                    file_path = generator._save_html_file(chapter.id, html_content)
                    print(f"HTML 생성 완료: {file_path}")
                else:
                    print("장 데이터 변환 실패")
            except Exception as e:
                print(f"JSON 파일 처리 실패: {e}")
    
    elif args.bible:
        try:
            with open(args.bible, 'r', encoding='utf-8') as f:
                bible_data = json.load(f)
            
            # Bible 객체 생성 (간단한 방식)
            bible = Bible(title=bible_data.get('title', '공동번역성서'))
            
            # TODO: Bible 데이터 분석 및 변환 로직 구현
            print("Bible JSON에서 HTML 생성 기능은 아직 구현되지 않았습니다.")
        except Exception as e:
            print(f"Bible JSON 파일 처리 실패: {e}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
