---
layout: default
title: "문어발 개발자 오은석의 DevLog"
description: "자바, 스프링, 데이터베이스부터 쿠버네티스까지 — 견고한 백엔드 시스템 구축을 위한 배움과 경험의 기록입니다."
---

<div class="blog-controls">
  <!-- 검색 창 -->
  <div class="search-wrapper">
    <input type="text" id="search-input" placeholder="🔍 제목 또는 내용 검색...">
  </div>

  <!-- 카테고리 필터 버튼 목록 -->
  <div class="category-container">
    <button class="category-btn active" data-category="all">
      전체보기 ({{ site.posts.size }})
    </button>
    {% for category in site.categories %}
      {% assign cat_id = category[0] | downcase | replace: ' ', '-' %}
      <button class="category-btn" data-category="{{ cat_id }}">
        {{ category[0] }} ({{ category[1].size }})
      </button>
    {% endfor %}
  </div>
</div>

<!-- 포스트 카드 그리드 -->
<div class="post-grid" id="post-grid">
  {% if site.posts.size > 0 %}
    {% for post in site.posts %}
      {% assign post_cat_id = post.categories[0] | downcase | replace: ' ', '-' %}
      <article class="post-card" data-category="{{ post_cat_id }}" data-title="{{ post.title | downcase }}">
        <div class="post-card-meta">
          <span class="post-card-date">
            📅 {{ post.date | date: "%Y년 %m월 %d일" }}
          </span>
          <span class="category-badge">
            {{ post.categories[0] | default: "Etc" }}
          </span>
        </div>
        <h3 class="post-card-title">
          <a class="post-link" href="{{ post.url | relative_url }}">
            {{ post.title }}
          </a>
        </h3>
        <!-- 본문 일부 추출 -->
        <p class="post-excerpt">
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
