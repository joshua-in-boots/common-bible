#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
명령줄 인터페이스 도구

다양한 CLI 명령을 제공하여 시스템을 더 쉽게 사용할 수 있게 합니다.
- 파싱, 생성, 게시 등 모든 기능 접근 제공
- 대화형 모드 지원
- 설정 관리 및 상태 확인
"""

import os
import sys
import time
import click
import logging
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn

# 프로젝트 내 모듈 import
from src.config import config
from src.parser import BibleParser
from src.html_generator import HTMLGenerator
from src.wp_publisher import WordPressPublisher
from src.security import security
from src.logger import set_log_level

# Rich 콘솔 설정
console = Console()


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='자세한 로그 출력')
def cli(verbose):
    """공동번역성서 변환 도구"""
    # 로그 레벨 설정
    if verbose:
        set_log_level('DEBUG')
    else:
        set_log_level('INFO')


@cli.command()
@click.option('--input', '-i', help='입력 텍스트 파일 경로')
@click.option('--output', '-o', help='출력 JSON 파일 경로')
@click.option('--split', '-s', is_flag=True, help='장별로 분할하여 저장')
def parse(input, output, split):
    """텍스트 파일을 파싱하여 구조화된 데이터로 변환"""
    try:
        # 입력/출력 파일 경로 설정
        if not input:
            input = os.path.join(config.paths['data_dir'], 'common-bible-kr.txt')
        
        if not output:
            output = os.path.join(config.paths['output_dir'], 'bible.json')
        
        console.print(f"[bold]파싱 시작[/bold]: {input}")
        
        # 파싱 시작
        start_time = time.time()
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("[cyan]파싱 중...", total=100)
            
            # 파서 초기화 및 실행
            parser = BibleParser(input)
            progress.update(task, completed=30)
            
            bible = parser.parse_file()
            progress.update(task, completed=70)
            
            # 결과 저장
            parser.save_to_json(output)
            
            # 장별 저장
            if split:
                parser.save_chapters_json()
                progress.update(task, completed=100)
        
        elapsed_time = time.time() - start_time
        
        # 결과 출력
        console.print(f"[green]파싱 완료[/green] (소요 시간: {elapsed_time:.2f}초)")
        console.print(f"총 {len(bible.books)}권, {sum(len(book.chapters) for book in bible.books)}장 파싱됨")
        console.print(f"결과 저장: {output}")
        
        return True
    
    except Exception as e:
        console.print(f"[bold red]오류 발생[/bold red]: {e}", style="red")
        return False


@cli.command()
@click.option('--input', '-i', help='입력 JSON 파일 또는 디렉토리')
@click.option('--output', '-o', help='출력 HTML 디렉토리')
@click.option('--template', '-t', help='템플릿 디렉토리')
def generate(input, output, template):
    """구조화된 데이터를 HTML로 변환"""
    try:
        # 입력/출력 경로 설정
        if not input:
            input = os.path.join(config.paths['output_dir'], 'chapters')
        
        if not output:
            output = os.path.join(config.paths['output_dir'], 'html')
        
        console.print(f"[bold]HTML 생성 시작[/bold]: {input}")
        
        # HTML 생성 시작
        start_time = time.time()
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("[cyan]HTML 생성 중...", total=100)
            
            # HTML 생성기 초기화
            generator = HTMLGenerator(template)
            progress.update(task, completed=30)
            
            # 출력 디렉토리 설정
            if output:
                generator.output_dir = output
                if not os.path.exists(output):
                    os.makedirs(output)
            
            # 입력 경로에 따라 처리
            if os.path.isdir(input):
                result = generator.generate_html_from_json(input)
            elif os.path.isfile(input) and input.endswith('.json'):
                console.print("[yellow]단일 JSON 파일 처리는 아직 구현되지 않았습니다[/yellow]")
                result = {}
            else:
                console.print(f"[bold red]잘못된 입력 경로: {input}[/bold red]")
                return False
            
            progress.update(task, completed=100)
        
        elapsed_time = time.time() - start_time
        
        # 결과 출력
        console.print(f"[green]HTML 생성 완료[/green] (소요 시간: {elapsed_time:.2f}초)")
        console.print(f"총 {len(result)}개 HTML 파일 생성됨")
        console.print(f"결과 저장: {output}")
        
        return True
    
    except Exception as e:
        console.print(f"[bold red]오류 발생[/bold red]: {e}", style="red")
        return False


@cli.command()
@click.option('--input', '-i', help='입력 HTML 디렉토리')
@click.option('--status', '-s', default='private', 
             type=click.Choice(['private', 'draft', 'publish']),
             help='게시 상태')
@click.option('--test', is_flag=True, help='인증 테스트만 수행')
def publish(input, status, test):
    """HTML 파일을 워드프레스에 게시"""
    try:
        console.print("[bold]워드프레스 게시 시작[/bold]")
        
        # 워드프레스 게시자 초기화
        publisher = WordPressPublisher()
        
        # 인증 테스트
        if test or not publisher.validate_auth():
            is_valid = publisher.validate_auth()
            
            if is_valid:
                console.print("[green]인증 테스트 성공[/green]: WordPress API에 연결되었습니다")
            else:
                console.print("[bold red]인증 테스트 실패[/bold red]: 환경변수와 API 설정을 확인하세요")
            
            if test:  # 테스트 모드면 여기서 종료
                return is_valid
            
            if not is_valid:  # 실제 게시 모드인데 인증 실패
                return False
        
        # HTML 디렉토리 확인
        if not input:
            input = os.path.join(config.paths['output_dir'], 'html')
        
        if not os.path.exists(input):
            console.print(f"[bold red]HTML 디렉토리를 찾을 수 없음: {input}[/bold red]")
            return False
        
        console.print(f"HTML 디렉토리: {input}")
        console.print(f"게시 상태: {status}")
        
        # 일괄 게시 시작
        start_time = time.time()
        
        # HTML 파일 목록 가져오기
        html_files = []
        for root, _, files in os.walk(input):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        total_files = len(html_files)
        console.print(f"총 {total_files}개 HTML 파일 발견")
        
        if not html_files:
            console.print("[yellow]게시할 HTML 파일이 없습니다[/yellow]")
            return False
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("[cyan]게시 중...", total=total_files)
            
            # 각 파일 게시
            success_count = 0
            for file_path in html_files:
                progress.update(task, description=f"[cyan]게시 중... ({os.path.basename(file_path)})")
                
                post_id = publisher.publish_html_file(file_path, status)
                if post_id:
                    success_count += 1
                
                progress.update(task, advance=1)
                
                # API 호출 제한 고려한 지연
                if task.completed % 10 == 0 and task.completed < total_files:
                    time.sleep(60 / publisher.api_rate_limit)
        
        # 메타데이터 저장
        publisher.save_posts_metadata()
        
        elapsed_time = time.time() - start_time
        
        # 결과 출력
        success_rate = (success_count / total_files) * 100 if total_files > 0 else 0
        console.print(f"[green]게시 완료[/green] (소요 시간: {elapsed_time:.2f}초)")
        console.print(f"성공: {success_count}/{total_files} ({success_rate:.1f}%)")
        
        return success_count > 0
    
    except Exception as e:
        console.print(f"[bold red]오류 발생[/bold red]: {e}", style="red")
        return False


@cli.command()
@click.option('--status', default='publish', 
             type=click.Choice(['private', 'draft', 'publish']),
             help='변경할 게시 상태')
def update_status(status):
    """이전에 게시된 글의 상태 일괄 업데이트"""
    try:
        console.print(f"[bold]게시물 상태 업데이트[/bold]: -> {status}")
        
        # 워드프레스 게시자 초기화
        publisher = WordPressPublisher()
        
        # 인증 확인
        if not publisher.validate_auth():
            console.print("[bold red]인증 실패[/bold red]: 환경변수와 API 설정을 확인하세요")
            return False
        
        # 이전 메타데이터 로드
        meta_path = os.path.join(config.paths['output_dir'], 'published_posts.json')
        if not os.path.exists(meta_path):
            console.print(f"[bold red]게시물 메타데이터 파일을 찾을 수 없음: {meta_path}[/bold red]")
            return False
        
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                publisher.published_posts = json.load(f)
        except Exception as e:
            console.print(f"[bold red]메타데이터 로드 실패: {e}[/bold red]")
            return False
        
        total_posts = len(publisher.published_posts)
        console.print(f"총 {total_posts}개 게시물 상태 업데이트 시작")
        
        if not total_posts:
            console.print("[yellow]업데이트할 게시물이 없습니다[/yellow]")
            return False
        
        # 일괄 업데이트 시작
        start_time = time.time()
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("[cyan]상태 업데이트 중...", total=total_posts)
            
            count = 0
            success, fail = 0, 0
            
            for chapter_id, post_data in publisher.published_posts.items():
                post_id = post_data['post_id']
                title = post_data['title']
                
                progress.update(task, description=f"[cyan]업데이트 중... ({title})")
                
                if publisher.update_post_status(post_id, status):
                    success += 1
                else:
                    fail += 1
                
                count += 1
                progress.update(task, completed=count)
                
                # API 호출 제한 고려한 지연
                if count % 10 == 0 and count < total_posts:
                    time.sleep(60 / publisher.api_rate_limit)
        
        # 메타데이터 다시 저장
        publisher.save_posts_metadata()
        
        elapsed_time = time.time() - start_time
        
        # 결과 출력
        success_rate = (success / total_posts) * 100 if total_posts > 0 else 0
        console.print(f"[green]상태 업데이트 완료[/green] (소요 시간: {elapsed_time:.2f}초)")
        console.print(f"성공: {success}/{total_posts} ({success_rate:.1f}%), 실패: {fail}")
        
        return success > 0
    
    except Exception as e:
        console.print(f"[bold red]오류 발생[/bold red]: {e}", style="red")
        return False


@cli.command()
@click.option('--input', '-i', help='입력 텍스트 파일 경로')
@click.option('--status', default='private', 
             type=click.Choice(['private', 'draft', 'publish']),
             help='게시 상태')
def pipeline(input, status):
    """전체 파이프라인 실행 (파싱 → HTML 생성 → 게시)"""
    try:
        console.print("[bold cyan]===== 전체 파이프라인 실행 =====[/bold cyan]")
        
        start_time = time.time()
        
        # 1. 파싱
        console.print("\n[bold]1. 텍스트 파싱[/bold]")
        parse_result = parse.callback(input=input, output=None, split=True)
        
        if not parse_result:
            console.print("[bold red]파싱 단계 실패, 파이프라인 중단[/bold red]")
            return False
        
        # 2. HTML 생성
        console.print("\n[bold]2. HTML 생성[/bold]")
        json_input = os.path.join(config.paths['output_dir'], 'chapters')
        html_output = os.path.join(config.paths['output_dir'], 'html')
        
        html_result = generate.callback(input=json_input, output=html_output, template=None)
        
        if not html_result:
            console.print("[bold red]HTML 생성 단계 실패, 파이프라인 중단[/bold red]")
            return False
        
        # 3. 워드프레스 게시
        console.print("\n[bold]3. 워드프레스 게시[/bold]")
        publish_result = publish.callback(input=html_output, status=status, test=False)
        
        if not publish_result:
            console.print("[bold red]워드프레스 게시 단계 실패[/bold red]")
            return False
        
        elapsed_time = time.time() - start_time
        
        # 결과 출력
        console.print(f"\n[bold green]===== 전체 파이프라인 완료 =====[/bold green]")
        console.print(f"총 소요 시간: {elapsed_time:.2f}초")
        
        return True
    
    except Exception as e:
        console.print(f"[bold red]오류 발생[/bold red]: {e}", style="red")
        return False


@cli.command()
def info():
    """시스템 상태 및 설정 정보 표시"""
    try:
        console.print("[bold cyan]===== 시스템 정보 =====[/bold cyan]")
        
        # 경로 정보
        table = Table(title="경로 정보")
        table.add_column("항목", style="cyan")
        table.add_column("경로", style="green")
        
        for key, path in config.paths.items():
            table.add_row(key, path)
        
        console.print(table)
        
        # 워드프레스 설정
        wp_config = config.get_wp_config()
        
        table = Table(title="워드프레스 설정")
        table.add_column("항목", style="cyan")
        table.add_column("값", style="green")
        
        # URL 표시
        table.add_row("API URL", wp_config['base_url'])
        
        # 토큰 마스킹
        if wp_config['auth_token']:
            token = wp_config['auth_token']
            masked_token = token[:4] + '*' * (len(token) - 8) + token[-4:]
            table.add_row("인증 토큰", masked_token)
        else:
            table.add_row("인증 토큰", "[red]설정되지 않음[/red]")
        
        table.add_row("API 호출 제한", str(wp_config['api_rate_limit']))
        
        # HTTPS 사용 여부
        if wp_config['base_url']:
            is_https = security.validate_https(wp_config['base_url'])
            https_status = "[green]사용 중[/green]" if is_https else "[red]미사용[/red]"
            table.add_row("HTTPS 보안", https_status)
        
        console.print(table)
        
        # 성경 책 매핑 정보
        book_mappings = config.load_book_mappings()
        
        table = Table(title="성경 책 매핑")
        table.add_column("약칭", style="cyan")
        table.add_column("전체 이름", style="green")
        table.add_column("영문 이름", style="yellow")
        
        # 일부만 표시
        for book in book_mappings[:10]:  # 처음 10개만
            table.add_row(
                book.get('약칭', ''),
                book.get('전체 이름', ''),
                book.get('영문 이름', '')
            )
        
        if len(book_mappings) > 10:
            table.add_row("...", "...", "...")
            table.add_row(
                f"총 {len(book_mappings)}권",
                "",
                ""
            )
        
        console.print(table)
        
        # 설정 유효성 검사
        valid = config.validate()
        validation_status = "[green]유효함[/green]" if valid else "[red]오류 있음[/red]"
        console.print(f"\n설정 유효성: {validation_status}")
        
        return True
    
    except Exception as e:
        console.print(f"[bold red]오류 발생[/bold red]: {e}", style="red")
        return False


if __name__ == '__main__':
    cli()
