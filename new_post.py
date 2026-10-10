#!/usr/bin/env python3
import os
import datetime
import re

POSTS_DIR = "_posts"
CATEGORIES = [
    "Java", "Spring", "Spring Batch", "Database", "Kafka", 
    "Kubernetes", "Design Pattern", "Git", "DevOps", "Node.js", 
    "Life & Career", "Etc"
]

# 한글 기술 키워드 -> 영문 매핑 사전
KOREAN_TECH_DICT = {
    # 아키텍처 / 핵심 개념
    "아키텍처": "architecture", "동작원리": "architecture", "원리": "principles",
    "구조": "structure", "내부": "internal", "분석": "analysis",
    "동작": "operation", "메커니즘": "mechanism", "개념": "concepts",
    "설계": "design", "시스템": "system", "서버": "server", "클라이언트": "client",
    "스레드": "thread", "비동기": "async", "네트워크": "network",
    
    # DB / 스토리지 / WAL
    "데이터베이스": "database", "체크포인트": "checkpoint", "세그먼트": "segment",
    "버퍼": "buffer", "레코드": "record", "페이지": "page", "튜플": "tuple",
    "인덱스": "index", "트랜잭션": "transaction", "테이블": "table",
    "커밋": "commit", "롤백": "rollback", "복구": "recovery", "장애": "crash",
    "락": "lock", "데드락": "deadlock", "격리수준": "isolation",
    "캐시": "cache", "메모리": "memory", "디스크": "disk", "로그": "log",
    
    # 프레임워크 / 백엔드
    "스프링": "spring", "부트": "boot", "배치": "batch", "시큐리티": "security",
    "자바": "java", "코틀린": "kotlin", "파이썬": "python",
    "카프카": "kafka", "프로듀서": "producer", "컨슈머": "consumer",
    "파티션": "partition", "브로커": "broker", "클러스터": "cluster",
    "쿠버네티스": "k8s", "도커": "docker", "컨테이너": "container", "파드": "pod",
    "디자인패턴": "design-pattern", "패턴": "pattern",
    "배포": "deploy", "파이프라인": "pipeline", "모니터링": "monitoring",
    
    # 작업 / 실무 / 튜닝
    "최적화": "optimization", "튜닝": "tuning", "성능": "performance",
    "트러블슈팅": "troubleshooting", "해결": "fix", "이슈": "issue", "에러": "error",
    "가이드": "guide", "정리": "summary", "기초": "basics", "입문": "intro",
    "시작": "start", "설정": "setup", "설치": "install", "비교": "vs",
    "회고": "retrospective", "면접": "interview", "후기": "review"
}

def clean_title(raw_title):
    """제목의 줄바꿈, 제어 문자 및 불필요한 연속 공백을 정돈합니다."""
    # 줄바꿈 및 제어 문자 제거
    title = re.sub(r"[\r\n\t]", " ", raw_title)
    title = title.strip()
    title = re.sub(r"\s+", " ", title)
    return title

def generate_smart_slug(title, category=""):
    """
    한글 제목에서 영문/숫자 및 기술 키워드를 추출하여
    깔끔한 kebab-case 영문 슬러그를 생성합니다.
    """
    text = title.strip()
    
    # 괄호 안의 시리즈 번호 보존 (예: (4) -> -4-)
    text = re.sub(r"[\(\[\{]\s*(\d+)\s*[\)\]\}]", r"-\1-", text)
    
    # 구분 기호 및 특수문자를 공백으로 변환
    text = re.sub(r"[\(\)\[\]\{\}·:,→\-_/|\"\']", " ", text)
    
    tokens = text.split()
    converted_tokens = []
    
    for token in tokens:
        lower_token = token.lower()
        matched = False
        
        # 1. 기술 사전 매핑 검사
        for ko, en in KOREAN_TECH_DICT.items():
            if ko in lower_token:
                converted_tokens.extend(en.split("-"))
                matched = True
                break
                
        # 2. 매핑되지 않은 경우 영문/숫자 추출
        if not matched:
            cleaned = re.sub(r"[^a-zA-Z0-9]", "", token)
            if cleaned:
                converted_tokens.append(cleaned.lower())
                
    # 중복 단어 제거 (순서 유지)
    seen = set()
    deduped_tokens = []
    for t in converted_tokens:
        if t not in seen:
            seen.add(t)
            deduped_tokens.append(t)
            
    # 너무 길어지지 않도록 최대 5개 핵심 토큰으로 제한
    if len(deduped_tokens) > 5:
        deduped_tokens = deduped_tokens[:5]
        
    slug = "-".join(deduped_tokens)
    slug = re.sub(r"\-+", "-", slug).strip("-")
    
    # 영문 토큰이 전혀 없는 경우 카테고리 기반 슬러그 생성
    if not slug or len(slug) < 2:
        cat_cleaned = re.sub(r"[^a-zA-Z0-9]", "", category.lower()) if category else "post"
        slug = f"{cat_cleaned}-note"
        
    return slug

def create_new_post():
    print("=========================================")
    print("📝 새로운 블로그 포스트 생성 도구 (스마트 슬러그)")
    print("=========================================\n")
    
    # 1. 제목 입력
    while True:
        raw_title = input("1. 글 제목을 입력하세요: ").strip()
        title = clean_title(raw_title)
        if title:
            break
        print("❌ 제목은 필수 입력 항목입니다. 다시 입력해 주세요.\n")
        
    # 2. 카테고리 선택
    print("\n2. 카테고리를 선택하세요:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"   [{idx:2d}] {cat}")
    
    try:
        cat_choice = int(input("\n👉 카테고리 번호 선택 (기본값 Database: 4): ") or 4)
        if 1 <= cat_choice <= len(CATEGORIES):
            category = CATEGORIES[cat_choice - 1]
        else:
            category = "Database"
    except ValueError:
        category = "Database"
        
    # 3. 파일명 슬러그 생성 및 추천
    recommended_slug = generate_smart_slug(title, category)
    print(f"\n💡 제목 분석 완료! 추천 슬러그: \033[1;36m{recommended_slug}\033[0m")
    
    slug_input = input(f"3. 글 URL 슬러그 입력 (엔터 입력 시 '{recommended_slug}'): ").strip()
    if not slug_input:
        slug = recommended_slug
    else:
        # 사용자가 직접 입력한 슬러그도 깔끔한 kebab-case로 정돈
        slug = re.sub(r"[^\w\-]", "", slug_input.lower().replace(" ", "-"))
        slug = re.sub(r"\-+", "-", slug).strip("-")
        
    # 4. 파일 생성 처리
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")
    
    # 보안: slug에서 영문/숫자/하이픈 외 모든 문자 제거 (Path Traversal 및 파일명 위조 원천 방지)
    slug = re.sub(r"[^a-zA-Z0-9\-]", "", slug).strip("-")
    if not slug:
        slug = f"post-{int(now.timestamp())}"

    # 보안: YAML Front Matter 파싱 깨짐 방지를 위한 큰따옴표 이스케이프
    escaped_title = title.replace("\\", "\\\\").replace('"', '\\"')

    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    # 파일 중복 검사
    if os.path.exists(filepath):
        print(f"\n❌ 이미 동일한 파일명이 존재합니다: {filepath}")
        return
        
    # Front Matter 및 기본 본문 템플릿 구성
    template = f"""---
layout: default
title: "{escaped_title}"
date: {datetime_str}
categories: [{category}]
slug: {slug}
---
{{% raw %}}

## 1. 개요

여기에 본문 마크다운 내용을 작성하세요.

{{% endraw %}}
"""
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template)
        
    print("\n=========================================")
    print("🎉 새 포스트 생성이 완료되었습니다!")
    print(f"📌 제목: {title}")
    print(f"📂 파일 경로: {filepath}")
    print(f"🔗 슬러그: {slug}")
    print("=========================================")
    print(f"👉 바로 편집하시려면 다음 링크를 클릭하세요: file://{os.path.abspath(filepath)}")

if __name__ == "__main__":
    create_new_post()
