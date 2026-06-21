---
layout: default
title: "문어발 개발자 오은석의 DevLog"
description: "자바, 스프링, 데이터베이스부터 쿠버네티스까지 — 견고한 백엔드 시스템 구축을 위한 배움과 경험의 기록입니다."
---

<div class="blog-controls">
  <!-- 검색 창 -->
  <div class="search-wrapper">
    <span class="prompt-prefix">osk2090@nebulix:~$ grep -i</span>
    <input type="text" id="search-input" placeholder="[keyword] posts/...">
  </div>

  <!-- 카테고리 필터 버튼 목록 -->
  <div class="category-container">
    <button class="category-btn active" data-category="all">
      --all
    </button>
    {% for category in site.categories %}
      {% assign cat_id = category[0] | downcase | replace: ' ', '-' %}
      <button class="category-btn" data-category="{{ cat_id }}">
        --{{ category[0] | downcase | replace: ' ', '-' }}
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
          <span class="title-prompt">&gt;</span>
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

<!-- 페이지네이션 컨트롤 -->
<div class="pagination-controls" id="pagination-controls"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const buttons = document.querySelectorAll('.category-btn');
  const cards = document.querySelectorAll('.post-card');
  const noResults = document.getElementById('no-results');
  const paginationContainer = document.getElementById('pagination-controls');
  
  let currentCategory = 'all';
  let searchQuery = '';
  let currentPage = 1;
  const postsPerPage = 8;

  function filterPosts() {
    let matchedCards = [];
    
    cards.forEach(card => {
      const cardCategory = card.getAttribute('data-category');
      const cardTitle = card.getAttribute('data-title') || '';
      const cardExcerpt = card.querySelector('.post-excerpt').textContent.toLowerCase();
      
      const matchesCategory = (currentCategory === 'all' || cardCategory === currentCategory);
      const matchesSearch = (cardTitle.includes(searchQuery) || cardExcerpt.includes(searchQuery));
      
      if (matchesCategory && matchesSearch) {
        matchedCards.push(card);
      } else {
        card.style.display = 'none';
      }
    });

    const totalMatched = matchedCards.length;
    
    if (totalMatched === 0) {
      noResults.style.display = 'block';
      paginationContainer.style.display = 'none';
      cards.forEach(card => card.style.display = 'none');
    } else {
      noResults.style.display = 'none';
      paginationContainer.style.display = 'flex';
      
      // Calculate total pages
      const totalPages = Math.ceil(totalMatched / postsPerPage);
      
      // Bound current page
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;
      
      // Calculate slice indices
      const startIndex = (currentPage - 1) * postsPerPage;
      const endIndex = startIndex + postsPerPage;
      
      // Display cards of the current page, hide others
      matchedCards.forEach((card, index) => {
        if (index >= startIndex && index < endIndex) {
          card.style.display = 'block';
          card.style.opacity = '1';
        } else {
          card.style.display = 'none';
        }
      });
      
      renderPagination(totalPages);
    }
  }

  function renderPagination(totalPages) {
    paginationContainer.innerHTML = '';
    
    if (totalPages <= 1) {
      paginationContainer.style.display = 'none';
      return;
    }
    
    // Previous button
    const prevBtn = document.createElement('div');
    prevBtn.className = `page-num ${currentPage === 1 ? 'disabled' : ''}`;
    prevBtn.textContent = '<< Prev';
    if (currentPage > 1) {
      prevBtn.addEventListener('click', () => {
        currentPage--;
        filterPosts();
        window.scrollTo({ top: 300, behavior: 'smooth' });
      });
    }
    paginationContainer.appendChild(prevBtn);
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
      const pageBtn = document.createElement('div');
      pageBtn.className = `page-num ${i === currentPage ? 'active' : ''}`;
      pageBtn.textContent = i;
      pageBtn.addEventListener('click', () => {
        currentPage = i;
        filterPosts();
        window.scrollTo({ top: 300, behavior: 'smooth' });
      });
      paginationContainer.appendChild(pageBtn);
    }
    
    // Next button
    const nextBtn = document.createElement('div');
    nextBtn.className = `page-num ${currentPage === totalPages ? 'disabled' : ''}`;
    nextBtn.textContent = 'Next >>';
    if (currentPage < totalPages) {
      nextBtn.addEventListener('click', () => {
        currentPage++;
        filterPosts();
        window.scrollTo({ top: 300, behavior: 'smooth' });
      });
    }
    paginationContainer.appendChild(nextBtn);
  }

  // Category filter click event
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      buttons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      currentCategory = this.getAttribute('data-category');
      currentPage = 1; // Reset to page 1 on filter change
      filterPosts();
    });
  });

  // Live search event
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      searchQuery = e.target.value.toLowerCase().trim();
      currentPage = 1; // Reset to page 1 on search change
      filterPosts();
    });
  }

  // Initial run
  filterPosts();
});
</script>
