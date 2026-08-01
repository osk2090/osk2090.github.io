#!/usr/bin/env python3
import subprocess
import sys
import os
import re
import shutil

def run_cmd(cmd):
    """Run a shell command and return stdout string."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_git_status():
    """Get status lines from git status -s."""
    status_output = run_cmd("git -c core.quotepath=false status -s")
    if not status_output:
        return []
    return [line for line in status_output.split("\n") if line.strip()]

def get_post_info(filepath):
    """Extract title and slug from Jekyll post markdown front matter."""
    title = ""
    slug = ""
    if not os.path.exists(filepath):
        return title, slug
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        tm = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
        if tm:
            title = tm.group(1).strip()
        sm = re.search(r'^slug:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
        if sm:
            slug = sm.group(1).strip()
    except Exception:
        pass

    if not title:
        basename = os.path.basename(filepath)
        basename = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", basename)
        title = re.sub(r"\.md$", "", basename).replace("-", " ")
    if not slug:
        slug = re.sub(r"[^\w\-]", "", title.lower().replace(" ", "-"))
        
    return title, slug

def auto_fix_local_images_in_posts():
    """Scan all modified/untracked markdown posts and convert local Mac image paths to repo images."""
    status_lines = get_git_status()
    modified_posts = []
    for line in status_lines:
        filepath = line[3:].strip('"')
        if filepath.startswith("_posts/") and filepath.endswith(".md"):
            modified_posts.append(filepath)

    if not modified_posts:
        return

    fixed_any = False
    for post_path in modified_posts:
        if not os.path.exists(post_path):
            continue
        with open(post_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Regex for local image paths (MarkText / desktop absolute paths)
        # e.g., ![](file:///Users/...) or ![](/Users/...)
        local_img_pattern = r'!\[(.*?)\]\(((?:file://)?/(?:Users|Users/.*?)/[^\)]+\.(?:png|jpg|jpeg|gif|webp))\)'
        matches = re.findall(local_img_pattern, content, re.IGNORECASE)

        if not matches:
            continue

        title, slug = get_post_info(post_path)
        folder_name = slug if slug else "general"
        target_dir = os.path.join("images", folder_name)
        os.makedirs(target_dir, exist_ok=True)

        print(f"\n📷 [{os.path.basename(post_path)}] 로컬 이미지 {len(matches)}개 자동 감지 및 레포지토리 복사 중...")

        new_content = content
        for idx, (alt, raw_src) in enumerate(matches, 1):
            src_path = raw_src.replace("file://", "").replace("%20", " ")
            if not os.path.exists(src_path):
                print(f"  ⚠️  경고: local image missing: {src_path}")
                continue

            ext = os.path.splitext(src_path)[1].lower()
            dest_filename = f"img_{idx}{ext}"
            dest_path = os.path.join(target_dir, dest_filename)
            shutil.copy2(src_path, dest_path)

            web_url = f"/{target_dir}/{dest_filename}".replace("\\", "/")
            new_content = new_content.replace(raw_src, web_url)
            print(f"  ✓ {os.path.basename(src_path)} -> {web_url}")

        if new_content != content:
            with open(post_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            fixed_any = True

    if fixed_any:
        print("✨ 모든 로컬 이미지 레포지토리 이전 및 마크다운 링크 자동 보정 완료!")

def generate_commit_candidates(status_lines):
    """Generate 3 high quality commit message candidates based on git status."""
    post_adds = []
    post_mods = []
    config_mods = []
    layout_mods = []
    other_files = []

    for line in status_lines:
        code = line[:2].strip()
        filepath = line[3:].strip('"')

        if filepath.startswith("_posts/"):
            title, _ = get_post_info(filepath)
            if "?" in code or "A" in code:
                post_adds.append((filepath, title))
            else:
                post_mods.append((filepath, title))
        elif filepath in ["_config.yml", "Gemfile", "ads.txt", "robots.txt"]:
            config_mods.append(filepath)
        elif filepath.startswith("_layouts/") or filepath.startswith("_includes/") or filepath.startswith("assets/"):
            layout_mods.append(filepath)
        else:
            other_files.append(filepath)

    candidates = []

    # Priority 1: Post creation/modification
    if post_adds or post_mods:
        if len(post_adds) == 1 and not post_mods:
            title = post_adds[0][1]
            candidates.append(f"feat(post): '{title}' 포스트 추가")
            candidates.append(f"docs: '{title}' 신규 기술 포스트 작성\n\n- {title} 블로그 포스트 추가")
            candidates.append(f"포스트 추가: {title}")
        elif len(post_mods) == 1 and not post_adds:
            title = post_mods[0][1]
            candidates.append(f"docs(post): '{title}' 포스트 내용 수정 및 보강")
            candidates.append(f"refactor(post): '{title}' 포스트 가독성 개선")
            candidates.append(f"포스트 수정: {title}")
        else:
            total_cnt = len(post_adds) + len(post_mods)
            candidates.append(f"docs(post): 블로그 포스트 {total_cnt}개 업데이트")
            candidates.append(f"feat(blog): 기술 포스트 신규 작성 및 기존 글 보강 ({total_cnt}개)")
            candidates.append(f"포스트 {total_cnt}개 추가 및 수정")

    # Priority 2: Layout / Theme modifications
    elif layout_mods:
        candidates.append("feat(theme): 블로그 레이아웃 및 디자인 개선")
        candidates.append("style: 테마 CSS 및 UI 컴포넌트 스타일 수정")
        candidates.append("UI 및 레이아웃 수정")

    # Priority 3: Config / Setting modifications
    elif config_mods:
        candidates.append(f"chore(config): {', '.join(config_mods)} 설정 업데이트")
        candidates.append("config: 블로그 환경 설정 및 SEO/AdSense 옵션 변경")
        candidates.append("설정 파일 업데이트")

    # Priority 4: General files / scripts
    else:
        first_file = other_files[0] if other_files else "files"
        candidates.append(f"feat: {first_file} 스크립트 및 도구 추가/수정")
        candidates.append(f"chore: {len(other_files)}개 파일 변경 사항 업데이트")
        candidates.append("코드 및 스크립트 업데이트")

    return candidates

def main():
    print("\n=========================================")
    print("🚀 Auto Git Commit & Push CLI (With Auto Image Fix)")
    print("=========================================")

    # Step 1: Auto detect & fix local mac image paths in posts
    auto_fix_local_images_in_posts()

    # Step 2: Read updated git status
    status_lines = get_git_status()
    if not status_lines:
        print("\n✅ 변경된 파일이 없습니다. (Working tree clean)")
        sys.exit(0)

    print("\n📋 [현재 변경된 파일 목록]")
    for line in status_lines:
        print(f"  {line}")
    print()

    candidates = generate_commit_candidates(status_lines)

    print("💡 [추천 깃 커밋 메시지 목록]")
    for idx, cand in enumerate(candidates, 1):
        formatted_cand = cand.replace("\n", " ")
        print(f"  [{idx}] {formatted_cand}")
    print("  [4] 직접 커밋 메시지 입력")
    print("  [0] 취소")

    try:
        choice = input("\n👉 사용할 커밋 메시지 번호를 선택하세요 (기본값: 1): ").strip()
        if not choice:
            choice = "1"
    except (KeyboardInterrupt, EOFError):
        print("\n취소되었습니다.")
        sys.exit(0)

    if choice == "0":
        print("취소되었습니다.")
        sys.exit(0)
    elif choice in ["1", "2", "3"]:
        commit_msg = candidates[int(choice) - 1]
    elif choice == "4":
        commit_msg = input("\n✍️  커밋 메시지를 입력하세요: ").strip()
        if not commit_msg:
            print("❌ 커밋 메시지가 입력되지 않았습니다.")
            sys.exit(1)
    else:
        commit_msg = candidates[0]

    print("\n-----------------------------------------")
    print(f"📌 선택된 커밋 메시지:\n{commit_msg}")
    print("-----------------------------------------")

    # Confirm staging and committing
    do_commit = input("\n💾 'git add .' 후 커밋하시겠습니까? [Y/n]: ").strip().lower()
    if do_commit in ["", "y", "yes"]:
        run_cmd("git add .")
        # Save to temporary file if multiline
        msg_file = "/tmp/git_commit_msg.txt"
        with open(msg_file, "w", encoding="utf-8") as f:
            f.write(commit_msg)
        
        commit_res = run_cmd(f'git commit -F "{msg_file}"')
        if os.path.exists(msg_file):
            os.remove(msg_file)
        print("\n✅ 커밋 완료!")
        print(commit_res)

        # Confirm push
        do_push = input("\n🚀 'git push origin main'을 실행하시겠습니까? [Y/n]: ").strip().lower()
        if do_push in ["", "y", "yes"]:
            print("\nPush 중...")
            push_res = run_cmd("git push origin main")
            print("🎉 Push 완료!")
            print(push_res)
    else:
        print("커밋이 취소되었습니다.")

if __name__ == "__main__":
    main()
