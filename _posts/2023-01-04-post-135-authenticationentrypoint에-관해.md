---
layout: default
title: "AuthenticationEntryPoint에 관해"
date: 2023-01-04 01:45:31 +0900
categories: [Etc]
slug: post-135-authenticationentrypoint에-관해
render_with_liquid: false
image: /images/135/img.png
---

먼저 본인 프로젝트의 문제가 header에 JWT가 포함되어야하는 API에서 header가 없을때 exception을 발생시켜야 한다.

![](/images/135/img.png)

security config 쪽에 AuthenticationEntryPoint의 구현체로 설정해준다.

![](/images/135/img_1.png)

그후 인증되지 않은 사용자가 접근시 예외를 뱉어내게 한다.

![](/images/135/img_2.png)

추가적인 설명으로 해당 내용은 AuthenticationEntryPoint에서  ExceptionTranslationFilter의 설명이다.

빨간줄내용으로는 모든 AccessDeniedException(입장불가예외) 및  AuthenticationException(인증예외) 발생시 예외처리를 filter chain으로 처리한다고 기재되어 있다.

참조: <https://mighty96.github.io/til/access-authentication/>