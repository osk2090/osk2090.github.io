# 📝 나의 개발 블로그 운영 가이드

이 저장소는 GitHub Pages와 Jekyll(Cayman 테마)을 이용한 개인 기술 블로그입니다.  
글 작성, 이미지 정리, 깃 커밋 및 배포까지 통합 관리할 수 있는 도구를 제공합니다.

---

## ⚡️ 0. 초간단 블로그 매니저 CLI (`blog` 커맨드)

터미널 어디서든 **`blog`** 명령어 하나로 블로그 디렉토리 이동 및 주요 작업을 대화형 메뉴로 실행할 수 있습니다.

```text
========================================
       🐙 DevLog 블로그 관리 매니저     
========================================
현재 위치: /Users/osk2090/Documents/Git/blog

  [1] 📝 새 포스트 작성 (new_post.py)
  [2] 🚀 스마트 커밋 & 푸시 (auto_commit.py)
  [3] 🔍 Git 상태 확인 (git status)
  [4] 🌐 로컬 웹 서버 실행 (테스트용)
  [5] 💻 직접 명령어 입력 (메뉴 닫기)
```

- **`1`**: 카테고리/슬러그 선택 기반 새 포스트 템플릿 생성
- **`2`**: 마크다운 내 로컬 이미지 자동 레포지토리 복사 + 스마트 커밋 메시지 추천 및 푸시
- **`5` 또는 `q` / 엔터**: 매니저를 종료하고 현재 블로그 폴더에서 직접 셸 커맨드 입력 가능

### 🛠 `blog` 단축 커맨드 등록 (최초 1회 설정)
Oh My Zsh 환경에서 `.zshrc`를 수정하지 않고 커스텀 폴더에 연결할 수 있습니다:
```bash
cp .blog-env.zsh ~/.oh-my-zsh/custom/blog.zsh && source ~/.zshrc
```
*(직접 실행 시: `./blog.sh`)*

---

## 🚀 1. 새 글 작성하기 (`new_post.py`)

새 글 생성 도구인 `new_post.py` 스크립트를 사용하면 양식과 파일명이 완벽히 설정된 새 포스트 파일을 즉시 만들 수 있습니다.

```bash
python3 new_post.py
# 또는 blog 명령어 실행 후 [1] 선택
```

1. **제목 입력** (예: `PostgreSQL WAL 레코드 구조 분석`)
2. **카테고리 번호 선택** (목록 중 선택, 기본값: Etc)
3. **URL 슬러그 확인** (엔터 클릭 시 제목 기반 자동 생성)
4. 생성된 `_posts/YYYY-MM-DD-slug.md` 마크다운 파일을 열어 본문을 작성합니다.

---

## ✍️ 2. 포스트 본문 작성 규칙

새 글 파일의 기본 구조:

```yaml
---
layout: default
title: "글 제목"
date: 2026-10-10 12:00:00 +0900
categories: [Database]
slug: postgresql-wal-record
---
{% raw %}

여기에 글 내용을 마크다운 형식으로 편하게 작성하세요.

{% endraw %}
```

### ⚠️ 필수 규칙
- **본문 전체가 `{% raw %}`와 `{% endraw %}`로 감싸여 있습니다.**  
  코드 블록 등에 프로그래밍 중괄호(`{ }`)나 `{{` 가 들어가면 Jekyll 빌드 엔진이 에러를 냅니다. 이를 방지하기 위한 설정이므로 **글 내용은 반드시 이 두 태그 사이에 작성**해 주세요.
- **이미지 및 HTML 시뮬레이션 첨부 파일 규칙:**
  - 웹 리소스 파일명은 공백이나 특수문자 없이 **영문 소문자와 하이픈(kebab-case)**으로 작성합니다.
  - 마크다운 본문 이미지 삽입: `![설명](/images/폴더/이미지.png)`
  - 인터랙티브 시뮬레이션 삽입 시:
    ```markdown
    <iframe src="/assets/html/insert-commit-checkpoint-simulation.html?v=1" width="100%" height="820px" style="border: 1px solid #cfd9de; border-radius: 12px; margin: 20px 0; background: #fff;" loading="lazy"></iframe>

    > 🔗 화면이 작거나 잘 보이지 않는다면 [새 탭에서 전체 화면으로 보기](https://blog.nebulix.io/assets/html/insert-commit-checkpoint-simulation.html?v=1){:target="_blank"}를 클릭.
    ```

---

## 🚀 3. 스마트 Git 커밋 & 푸시 (`auto_commit.py`)

`auto_commit.py` 스크립트는 수작업으로 이미지를 옮기고 커밋 메시지를 작성하는 번거로움을 자동화해 줍니다.

```bash
python3 auto_commit.py
# 또는 blog 명령어 실행 후 [2] 선택
```

### ✨ 자동화 기능
1. **로컬 이미지 자동 감지 및 이전**:  
   마크다운 작성기(MarkText, Typora 등)로 글을 쓰면서 붙여넣은 Mac 로컬 절대경로(`file:///Users/...`) 이미지를 감지하여, 자동으로 `images/{slug}/` 폴더에 복사하고 마크다운 링크를 웹 절대경로로 자동 치환합니다.
2. **고품질 커밋 메시지 추천**:  
   변경된 포스트 제목과 변경 유형을 분석하여 Conventional Commits(`feat(post): ...`, `docs(post): ...`) 형식의 메시지를 자동 생성 및 추천합니다.
3. **Staging / Commit / Push 원클릭 처리**.

---

## 💻 4. 로컬에서 미리보기 (선택 사항)

### 간단 정적 서버 (HTML/이미지 확인용)
```bash
python3 -m http.server 8000
# http://localhost:8000 접속
```

### 전체 Jekyll 사이트 빌드 & 서버 구동
```bash
bundle exec jekyll serve
# http://localhost:4000 접속
```

---

## 🤫 5. 임시 글 저장하기 (초안 작성)

아직 미완성이라 나중에 발행하고 싶은 글은 `_drafts` 폴더를 활용하세요.

1. 프로젝트 루트에 `_drafts/my-draft.md` 형식으로 초안을 작성합니다. (GitHub에 푸시해도 사이트에는 노출되지 않음)
2. 글이 완성되면 파일명을 `YYYY-MM-DD-slug.md` 형식으로 변경하고 `_posts/` 폴더로 이동한 뒤 푸시하면 공식 발행됩니다.
