---
layout: default
title: "Spring Security 커스텀 AuthenticationEntryPoint 구현 및 예외 처리 아키텍처"
date: 2023-01-04 01:45:31 +0900
categories: [Spring]
slug: post-135-authenticationentrypoint에-관해
image: /images/135/img.png
---
{% raw %}

Spring Security와 JWT(JSON Web Token)를 결합하여 API 서버를 설계할 때 흔히 마주치는 시나리오 중 하나는, **인증되지 않은 사용자(예: Authorization 헤더에 JWT 토큰이 누락되었거나 유효하지 않은 경우)가 권한이 필요한 보호된 API에 접근했을 때 적절한 예외 응답을 클라이언트에 전달하는 것**입니다.

이번 포스팅에서는 Spring Security의 예외 처리 아키텍처와 함께 `AuthenticationEntryPoint`의 역할 및 이를 커스텀 구현하여 예외 처리를 정교하게 구성하는 방법에 대해 알아보겠습니다.

---

## 1. Spring Security 예외 처리 아키텍처

Spring Security는 기본적으로 수많은 서블릿 필터(Filter)의 체인으로 동작합니다. 이 중 인증 및 인가 관련 예외를 처리하는 핵심 필터가 바로 **`ExceptionTranslationFilter`**입니다.

```text
[Filter Chain 흐름]
... ──> FilterSecurityInterceptor (인가 검사 수행)
             ↓ (예외 발생!)
       ExceptionTranslationFilter (예외 캐치 및 처리 분기)
        ├─ 1) AuthenticationException (인증 실패) ──> AuthenticationEntryPoint 실행 (401)
        └─ 2) AccessDeniedException (인가 실패) ──> AccessDeniedHandler 실행 (403)
```

`ExceptionTranslationFilter`는 필터 체인의 하단(보통 인가 처리를 담당하는 `FilterSecurityInterceptor` 바로 위)에 위치하며, 하위 필터나 컨트롤러 레이어에서 던져지는 예외를 가로챕니다.

### 예외 처리 분기 기준
1. **`AuthenticationException` (인증 예외)**
   * **상황**: 익명 사용자(Anonymous User)이거나 로그인 정보가 유효하지 않은 상태에서 권한이 요구되는 자원에 접근하려 할 때 발생합니다.
   * **조치**: **`AuthenticationEntryPoint`**를 호출하여 로그인을 유도하거나 에러 응답을 보냅니다.
2. **`AccessDeniedException` (인가/접근 거부 예외)**
   * **상황**: 사용자가 로그인(인증)은 완료했으나, 해당 자원에 접근할 수 있는 필요한 권한(Role)이 없는 상태에서 접근하려 할 때 발생합니다.
   * **조치**: **`AccessDeniedHandler`**를 호출하여 거부 처리(예: 403 Forbidden)를 보냅니다.

---

## 2. 커스텀 AuthenticationEntryPoint 구현

전형적인 웹 애플리케이션의 경우 인증 실패 시 로그인 페이지(Redirect URL)로 안내하지만, REST API 서버는 클라이언트에 리다이렉트가 아닌 공통 에러 포맷의 JSON 데이터와 HTTP Status Code 401(Unauthorized)을 직접 내려주어야 합니다.

이를 구현하기 위해 `AuthenticationEntryPoint` 인터페이스를 직접 구현하여 처리합니다.

### CustomAuthenticationEntryPoint.java
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.MediaType;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Component
public class CustomAuthenticationEntryPoint implements AuthenticationEntryPoint {

    @Override
    public void commence(HttpServletRequest request, 
                         HttpServletResponse response,
                         AuthenticationException authException) throws IOException, ServletException {
                         
        // REST API 환경에 맞는 JSON 형태의 에러 응답 생성
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED); // 401 에러 설정

        final Map<String, Object> body = new HashMap<>();
        body.put("status", HttpServletResponse.SC_UNAUTHORIZED);
        body.put("error", "Unauthorized");
        body.put("message", "인증 정보가 유효하지 않거나 누락되었습니다. 요청 헤더를 확인해 주세요.");
        body.put("path", request.getServletPath());

        final ObjectMapper mapper = new ObjectMapper();
        mapper.writeValue(response.getOutputStream(), body);
    }
}
```

### SecurityConfig.java 연동
작성한 커스텀 구현체를 Spring Security 설정 클래스에 등록해 줍니다.
```java
@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final CustomAuthenticationEntryPoint authenticationEntryPoint;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            // ... 중략 ...
            .exceptionHandling()
            .authenticationEntryPoint(authenticationEntryPoint); // 커스텀 진입점 주입
            
        return http.build();
    }
}
```

---

## Summary

`ExceptionTranslationFilter` 공식 문서의 핵심 내용에 따르면, 모든 `AccessDeniedException` 및 `AuthenticationException` 예외는 Spring Security 필터 체인 레벨에서 수집되어 일관되게 처리됩니다.

인증 예외가 발생할 때 리다이렉트가 아닌 API 규약에 알맞은 HTTP Status와 JSON 결과값을 내려주기 위해 커스텀 `AuthenticationEntryPoint` 설정을 적용하는 것은 모던 웹 애플리케이션의 필수 요소입니다.

![](/images/135/img.png)

![](/images/135/img_1.png)

![](/images/135/img_2.png)

* 참조: <https://mighty96.github.io/til/access-authentication/>
{% endraw %}