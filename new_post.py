import os
import datetime
import re

POSTS_DIR = "_posts"
CATEGORIES = [
    "Java", "Spring", "Spring Batch", "Database", "Kafka", 
    "Kubernetes", "Design Pattern", "Git", "DevOps", "Node.js", 
    "Life & Career", "Etc"
]

def sanitize_slug(title):
    # Convert title to lowercase, replace spaces and special characters with hyphens
    slug = title.lower().strip()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"[^\w\-]", "", slug)
    slug = re.sub(r"\-+", "-", slug)
    return slug

def create_new_post():
    print("=========================================")
    print("📝 새로운 블로그 포스트 생성 도구")
    print("=========================================\n")
    
    # 1. 제목 입력
    title = input("1. 글 제목을 입력하세요: ").strip()
    if not title:
        print("❌ 제목은 필수 입력 항목입니다.")
        return
        
    # 2. 카테고리 선택
    print("\n2. 카테고리를 선택하세요:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f"   [{idx}] {cat}")
    
    try:
        cat_choice = int(input("\n👉 카테고리 번호 선택 (기본값 Etc: 12): ") or 12)
        if 1 <= cat_choice <= len(CATEGORIES):
            category = CATEGORIES[cat_choice - 1]
        else:
            category = "Etc"
    except ValueError:
        category = "Etc"
        
    # 3. 파일명 슬러그 생성 및 확인
    default_slug = sanitize_slug(title)
    slug = input(f"\n3. 글 URL 슬러그 입력 (엔터 입력 시 기본값 '{default_slug}'): ").strip()
    if not slug:
        slug = default_slug
        
    # 4. 파일 생성 처리
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")
    
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    # 파일 중복 검사
    if os.path.exists(filepath):
        print(f"\n❌ 이미 동일한 파일명이 존재합니다: {filepath}")
        return
        
    # Front Matter 및 기본 본문 템플릿 구성
    template = f"""---
layout: default
title: "{title}"
date: {datetime_str}
categories: [{category}]
slug: {slug}
---
{{% raw %}}

여기에 본문 마크다운 내용을 작성하세요. (코드 블록 안의 중괄호 {{ }} 도 오류 없이 안전하게 렌더링됩니다!)

{{% endraw %}}
"""
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template)
        
    print("\n=========================================")
    print("🎉 새 포스트 생성이 완료되었습니다!")
    print(f"📂 파일 경로: {filepath}")
    print("=========================================")
    print(f"👉 바로 편집하시려면 다음 링크를 클릭하세요: file://{os.path.abspath(filepath)}")

if __name__ == "__main__":
    create_new_post()
