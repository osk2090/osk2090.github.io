#!/usr/bin/env bash

# 색상 정의
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 작업 디렉토리를 스크립트 위치(blog 루트)로 보장
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

show_menu() {
    clear
    echo -e "${CYAN}${BOLD}========================================${NC}"
    echo -e "${CYAN}${BOLD}       🐙 DevLog 블로그 관리 매니저     ${NC}"
    echo -e "${CYAN}${BOLD}========================================${NC}"
    echo -e "${BOLD}현재 위치:${NC} $SCRIPT_DIR"
    echo ""
    echo -e "  ${GREEN}[1]${NC} 📝 새 포스트 작성 (_posts)"
    echo -e "  ${GREEN}[2]${NC} 🤫 임시 글 작성 (_drafts)"
    echo -e "  ${GREEN}[3]${NC} 🚀 임시 글 정식 발행 (draft -> post)"
    echo -e "  ${GREEN}[4]${NC} 📦 스마트 커밋 & 푸시 (auto_commit.py)"
    echo -e "  ${GREEN}[5]${NC} 🔍 Git 상태 확인 (git status)"
    echo -e "  ${GREEN}[6]${NC} 🌐 로컬 웹 서버 실행 (테스트용)"
    echo -e "  ${YELLOW}[7]${NC} 💻 직접 명령어 입력 (메뉴 닫기)"
    echo ""
    echo -e "${CYAN}----------------------------------------${NC}"
}

start_local_server() {
    echo ""
    echo -e "${CYAN}${BOLD}[로컬 웹 서버 실행]${NC}"
    echo -e "${GREEN}http://localhost:8000 에서 확인하실 수 있습니다. (종료: Ctrl+C)${NC}"
    echo -e "${YELLOW}🔒 보안: 127.0.0.1(로컬호스트)에만 바인딩되어 외부 네트워크 접근이 차단됩니다.${NC}"
    python3 -m http.server 8000 --bind 127.0.0.1
}

# 메인 루프
while true; do
    show_menu
    read -rp "원하는 작업 번호를 선택하세요 (1-7, 종료는 q 또는 7): " choice
    case "$choice" in
        1)
            echo ""
            python3 new_post.py
            echo ""
            read -rp "계속하려면 Enter를 누르세요..." _
            ;;
        2)
            echo ""
            python3 new_post.py --draft
            echo ""
            read -rp "계속하려면 Enter를 누르세요..." _
            ;;
        3)
            echo ""
            python3 new_post.py --publish
            echo ""
            read -rp "계속하려면 Enter를 누르세요..." _
            ;;
        4)
            echo ""
            python3 auto_commit.py
            echo ""
            read -rp "계속하려면 Enter를 누르세요..." _
            ;;
        5)
            echo ""
            git status
            echo ""
            read -rp "계속하려면 Enter를 누르세요..." _
            ;;
        6)
            start_local_server
            read -rp "계속하려면 Enter를 누르세요..." _
            ;;
        7|q|Q|exit)
            echo -e "${GREEN}터미널로 돌아갑니다. 명령어를 직접 입력하세요.${NC}"
            exit 0
            ;;
        *)
            # 1~6 외의 다른 키나 엔터 입력 시 바로 터미널로 나감
            echo -e "${GREEN}메뉴를 종료하고 셸로 전환합니다.${NC}"
            exit 0
            ;;
    esac
done
