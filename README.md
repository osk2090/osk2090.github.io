# 📝 나의 개발 블로그 운영 가이드

이 저장소는 GitHub Pages와 Jekyll(Cayman 테마)을 이용한 개인 기술 블로그([https://blog.nebulix.io/](https://blog.nebulix.io/))입니다.  
글 작성, 스마트 슬러그 생성, 임시 글(초안) 관리, 이미지 자동 정리, 깃 커밋 및 배포까지 한 번에 관리할 수 있는 도구를 제공합니다.

---

## ⚡️ 0. 통합 블로그 매니저 CLI (`blog` 커맨드)

터미널 어디서든 **`blog`** 명령어 하나로 블로그 디렉토리 이동 및 모든 작업을 대화형 메뉴로 수행할 수 있습니다.

```text
========================================
       🐙 DevLog 블로그 관리 매니저     
========================================
현재 위치: /Users/osk2090/Documents/Git/blog

  [1] 📝 새 포스트 작성 (_posts)
  [2] 🤫 임시 글 작성 (_drafts)
  [3] 🚀 임시 글 정식 발행 (draft -> post)
  [4] 📦 스마트 커밋 & 푸시 (auto_commit.py)
  [5] 🔍 Git 상태 확인 (git status)
  [6] 🌐 로컬 웹 서버 실행 (테스트용)
  [7] 💻 직접 명령어 입력 (메뉴 닫기)
```

- **`1`**: 한글 제목 분석 기반 스마트 슬러그 추천 및 정식 포스트(`_posts/`) 생성
- **`2`**: 웹사이트에 노출되지 않는 초안/임시 글(`_drafts/`) 바로 생성
- **`3`**: 작성 완료된 임시 글을 오늘 날짜의 정식 포스트(`_posts/`)로 원클릭 승격 발행
- **`4`**: 마크다운 내 로컬 이미지 자동 레포지토리 복사 + 스마트 커밋 메시지 추천 및 푸시
- **`7` 또는 `q` / 엔터**: 매니저를 종료하고 현재 블로그 폴더에서 즉시 셸 커맨드 입력 가능

### 🛠 `blog` 단축 커맨드 등록 (최초 1회 설정)
Oh My Zsh 환경에서 `.zshrc`를 수정하지 않고 커스텀 폴더에 안전하게 연결할 수 있습니다:
```bash
cp .blog-env.zsh ~/.oh-my-zsh/custom/blog.zsh && source ~/.zshrc
```
*(직접 실행 시: `./blog.sh`)*

---

## 🚀 1. 포스트 및 임시 글 작성 (`new_post.py`)

### 💡 지능형 스마트 슬러그 생성 엔진 탑재
한글 제목을 입력하면 기술 용어 사전을 기반으로 **깔끔한 영문 kebab-case 슬러그**를 자동 추천합니다. 엔터(Enter)만 누르면 추천 슬러그가 확정됩니다.

| 입력한 한글 제목 예시 | 자동 추천 슬러그 |
| :--- | :--- |
| `PostgreSQL WAL (4) WAL 레코드 내부 구조 분석` | `postgresql-wal-4-record-internal` |
| `PostgreSQL WAL (5) 커밋 후 복구 메커니즘과 동작 원리` | `postgresql-wal-5-commit-recovery` |
| `Kafka 파티션과 컨슈머 그룹 최적화 가이드` | `kafka-partition-consumer-optimization-guide` |
| `스프링 부트 3.0과 스프링 배치 5.0 시작하기` | `spring-boot-30-batch-50` |
| `가상 면접 사례로 배우는 대규모 시스템 설계` | `interview-system-design` |

---

### 📝 포스트 작성 및 초안 관리 커맨드

#### ① 정식 포스트 바로 작성 (`_posts/`)
```bash
python3 new_post.py
# 또는 blog 명령어 실행 후 [1] 선택
```
- 오늘 날짜 접두사가 붙은 `_posts/YYYY-MM-DD-slug.md` 파일이 생성됩니다.

#### ② 임시 글(초안) 작성 (`_drafts/`)
```bash
python3 new_post.py --draft
# 또는 blog 명령어 실행 후 [2] 선택
```
- `_drafts/slug.md` 경로로 생성되며, `published: false` 속성이 적용되어 GitHub에 푸시해도 실서버에 절대 노출되지 않습니다.

#### ③ 임시 글 정식 발행 (`_drafts` ➔ `_posts`)
```bash
python3 new_post.py --publish
# 또는 blog 명령어 실행 후 [3] 선택
```
- `_drafts` 내 글 목록을 보고 번호를 선택하면, 자동으로 **오늘 날짜가 붙어 `_posts/`로 이동**하며 `published: false`가 제거되어 공식 발행 상태로 변환됩니다.

---

## ✍️ 2. 포스트 본문 작성 규칙

새 글 파일의 기본 템플릿:

```yaml
---
layout: default
title: "글 제목"
date: 2026-10-10 12:00:00 +0900
categories: [Database]
slug: postgresql-wal-record
---
{% raw %}

여기에 글 내용을 마크다운 형식으로 작성하세요.

{% endraw %}
```

### ⚠️ 필수 작성 규칙
1. **`{% raw %}`와 `{% endraw %}` 보존**  
   코드 블록 내 중괄호(`{ }`)나 `{{` 기호로 인한 Jekyll Liquid 빌드 오류를 방지하기 위해 **모든 본문 내용은 이 두 태그 사이**에 작성합니다.
2. **웹 리소스 네이밍 규칙 (중요)**  
   - 이미지, HTML 시뮬레이션 파일명은 한글이나 특수문자(`→`) 대신 **영문 소문자 + 하이픈(kebab-case)**을 사용해야 배포 시 404가 발생하지 않습니다.
3. **인터랙티브 시뮬레이션 HTML 삽입 규칙**  
   - 시뮬레이션 HTML은 `assets/html/`에 저장하며, 본문에는 iframe 및 새 탭 보기 링크를 절대 URL 도메인으로 함께 기재합니다:
     ```markdown
     <iframe src="/assets/html/insert-commit-checkpoint-simulation.html?v=1" width="100%" height="820px" style="border: 1px solid #cfd9de; border-radius: 12px; margin: 20px 0; background: #fff;" loading="lazy"></iframe>

     > 🔗 화면이 작거나 잘 보이지 않는다면 [새 탭에서 전체 화면으로 보기](https://blog.nebulix.io/assets/html/insert-commit-checkpoint-simulation.html?v=1){:target="_blank"}를 클릭.
     ```

---

## 📦 3. 스마트 Git 커밋 & 푸시 (`auto_commit.py`)

`auto_commit.py` 스크립트는 이미지 경로 처리와 깃 커밋 작업을 자동화합니다.

```bash
python3 auto_commit.py
# 또는 blog 명령어 실행 후 [4] 선택
```

### ✨ 핵심 자동화 기능
1. **로컬 Mac 이미지 자동 감지 및 이전**:  
   마크다운 에디터(MarkText, Typora 등)에서 복사/붙여넣기하여 들어간 로컬 절대경로(`file:///Users/...`) 이미지를 자동 감지하여 `images/{slug}/` 폴더에 복사하고, 마크다운 본문의 링크를 웹 상대/절대경로로 자동 치환합니다.
2. **Conventional Commits 기반 메시지 자동 추천**:  
   수정/추가된 포스트 제목을 파싱하여 `feat(post): ...`, `docs(post): ...` 형식의 고품질 커밋 메시지 후보 3가지를 생성 및 제안합니다.
3. **Staging / Commit / Push 원스톱 처리**.

---

## 💻 4. 로컬 미리보기 (선택 사항)

### 안전한 정적 서버 (HTML/시뮬레이션 확인용)
외부 네트워크(공용 Wi-Fi) 노출을 차단하도록 로컬호스트(`127.0.0.1`)에만 바인딩되어 안전합니다:
```bash
python3 -m http.server 8000 --bind 127.0.0.1
# 또는 blog 실행 후 [6] 선택 -> http://localhost:8000 접속
```

### 전체 Jekyll 사이트 빌드 & 서버 구동
```bash
bundle exec jekyll serve
# http://localhost:4000 접속
```
*(임시 글까지 함께 미리보려면: `bundle exec jekyll serve --drafts`)*

---

## 🔒 5. 보안 및 안전 설계
- **명령어 주입 차단 (Command Injection Free)**: 메뉴 스크립트 분기 처리에 안전한 bash 구문을 적용했습니다.
- **경로 탈출 차단 (Path Traversal Protection)**: 슬러그 입력 시 영문/숫자/하이픈 외 모든 특수문자 및 `../` 경로 이동 문자를 원천 제거합니다.
- **YAML Front Matter 안전성 보장**: 글 제목의 큰따옴표 이스케이프 및 줄바꿈/제어 문자를 정제하여 파싱 오류를 사전에 차단합니다.
- **로컬 웹 서버 격리**: `127.0.0.1` 루프백 인터페이스에만 바인딩하여 공용 Wi-Fi 환경에서 비공개 초안이 노출되지 않도록 보호합니다.
