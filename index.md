---
layout: default
title: "나의 개발 블로그"
description: "공부하고 공유하고 싶은 기술과 경험을 기록하는 공간입니다."
---

<div class="blog-controls" style="margin-bottom: 2em; display: flex; flex-direction: column; gap: 1em;">
  <!-- 검색 창 -->
  <div class="search-wrapper" style="position: relative; width: 100%;">
    <input type="text" id="search-input" placeholder="🔍 제목 또는 내용 검색..." style="width: 100%; padding: 12px 20px; font-size: 1em; border: 2px solid #e1e4e8; border-radius: 8px; box-sizing: border-box; outline: none; transition: border-color 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
  </div>

  <!-- 카테고리 필터 버튼 목록 -->
  <div class="category-container" style="display: flex; flex-wrap: wrap; gap: 0.6em; padding-bottom: 0.5em; border-bottom: 1px solid #eaecef;">
    <button class="category-btn active" data-category="all" style="padding: 8px 16px; font-size: 0.9em; border: 1px solid #1e6bb8; border-radius: 20px; background-color: #1e6bb8; color: white; cursor: pointer; font-weight: bold; transition: all 0.2s ease;">
      전체보기 ({{ site.posts.size }})
    </button>
    {% for category in site.categories %}
      {% assign cat_id = category[0] | downcase | replace: ' ', '-' %}
      <button class="category-btn" data-category="{{ cat_id }}" style="padding: 8px 16px; font-size: 0.9em; border: 1px solid #e1e4e8; border-radius: 20px; background-color: #f6f8fa; color: #586069; cursor: pointer; transition: all 0.2s ease;">
        {{ category[0] }} ({{ category[1].size }})
      </button>
    {% endfor %}
  </div>
</div>

<!-- 포스트 카드 그리드 -->
<div class="post-grid" id="post-grid" style="display: flex; flex-direction: column; gap: 1.2em;">
  {% if site.posts.size > 0 %}
    {% for post in site.posts %}
      {% assign post_cat_id = post.categories[0] | downcase | replace: ' ', '-' %}
      <article class="post-card" data-category="{{ post_cat_id }}" data-title="{{ post.title | downcase }}" style="border: 1px solid #e1e4e8; border-radius: 8px; padding: 1.5em; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.03); transition: transform 0.2s ease, box-shadow 0.2s ease; display: block;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8em; flex-wrap: wrap; gap: 0.5em;">
          <span style="font-size: 0.85em; color: #586069; font-weight: 500;">
            📅 {{ post.date | date: "%Y년 %m월 %d일" }}
          </span>
          <span class="category-badge" style="font-size: 0.75em; padding: 4px 10px; border-radius: 12px; font-weight: bold; background-color: #e2f0fd; color: #1e6bb8; border: 1px solid #b8daff;">
            {{ post.categories[0] | default: "Etc" }}
          </span>
        </div>
        <h3 style="margin: 0 0 0.5em 0; font-size: 1.25em; line-height: 1.4;">
          <a class="post-link" href="{{ post.url | relative_url }}" style="text-decoration: none; color: #1e6bb8; font-weight: bold;">
            {{ post.title }}
          </a>
        </h3>
        <!-- 본문 일부 추출 -->
        <p class="post-excerpt" style="margin: 0; color: #586069; font-size: 0.9em; line-height: 1.5; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
          {{ post.content | strip_html | truncate: 150 }}
        </p>
      </article>
    {% endfor %}
  {% else %}
    <div id="no-posts" style="text-align: center; padding: 3em 0; color: #586069;">
      <h3>아직 작성된 글이 없습니다.</h3>
    </div>
  {% endif %}
  
  <div id="no-results" style="display: none; text-align: center; padding: 3em 0; color: #586069;">
    <h3>🔍 검색 결과가 없습니다.</h3>
    <p>다른 키워드를 시도해 보세요.</p>
  </div>
</div>

<style>
.category-btn:hover {
  border-color: #1e6bb8 !important;
  color: #1e6bb8 !important;
  background-color: #f1f8ff !important;
  transform: translateY(-1px);
}
.category-btn.active {
  background-color: #1e6bb8 !important;
  color: white !important;
  border-color: #1e6bb8 !important;
  box-shadow: 0 2px 4px rgba(30,107,184,0.3);
}
.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.08) !important;
  border-color: #1e6bb8 !important;
}
.post-link:hover {
  text-decoration: underline !important;
  color: #154c80 !important;
}
#search-input:focus {
  border-color: #1e6bb8 !important;
  box-shadow: 0 0 0 3px rgba(30,107,184,0.15) !important;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const buttons = document.querySelectorAll('.category-btn');
  const cards = document.querySelectorAll('.post-card');
  const noResults = document.getElementById('no-results');
  let currentCategory = 'all';
  let searchQuery = '';

  function filterPosts() {
    let visibleCount = 0;
    
    cards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const cardTitle = card.getAttribute('data-title') || '';
      const cardExcerpt = card.querySelector('.post-excerpt').textContent.toLowerCase();
      
      const matchesCategory = (currentCategory === 'all' || cardCategory === currentCategory);
      const matchesSearch = (cardTitle.includes(searchQuery) || cardExcerpt.includes(searchQuery));
      
      if (matchesCategory && matchesSearch) {
        card.style.display = 'block';
        // Fade in effect
        card.style.opacity = '0';
        setTimeout(() => {
          card.style.opacity = '1';
          card.style.transition = 'opacity 0.2s ease';
        }, 10);
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (visibleCount === 0 && cards.length > 0) {
      noResults.style.display = 'block';
    } else {
      noResults.style.display = 'none';
    }
  }

  // 카테고리 필터 클릭 이벤트
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      buttons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      currentCategory = this.getAttribute('data-category');
      filterPosts();
    });
  });

  // 검색 실시간 필터 이벤트
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      searchQuery = e.target.value.toLowerCase().trim();
      filterPosts();
    });
  }
});
</script>
