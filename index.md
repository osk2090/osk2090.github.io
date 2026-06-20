---
layout: default
title: "나의 개발 블로그"
description: "공부하고 공유하고 싶은 내용을 기록하는 공간입니다."
---

## 📝 최신 블로그 글 목록

<ul class="post-list" style="list-style-type: none; padding-left: 0;">
  {% if site.posts.size > 0 %}
    {% for post in site.posts %}
      <li style="margin-bottom: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 1em;">
        <span class="post-meta" style="color: #666; font-size: 0.9em; display: block; margin-bottom: 0.3em;">
          📅 {{ post.date | date: "%Y년 %m월 %d일" }}
        </span>
        <h3 style="margin: 0; font-size: 1.3em;">
          <a class="post-link" href="{{ post.url | relative_url }}" style="text-decoration: none; color: #1e6bb8; font-weight: bold;">
            {{ post.title }}
          </a>
        </h3>
        {% if post.description %}
          <p style="margin: 0.5em 0 0 0; color: #555; font-size: 0.95em;">
            {{ post.description }}
          </p>
        {% endif %}
      </li>
    {% endfor %}
  {% else %}
    <li>아직 작성된 글이 없습니다.</li>
  {% endif %}
</ul>

<style>
.post-link:hover {
  text-decoration: underline !important;
  color: #154c80 !important;
}
</style>
