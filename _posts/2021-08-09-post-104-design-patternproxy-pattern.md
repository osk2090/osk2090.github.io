---
layout: default
title: "[Design Pattern]Proxy Pattern"
date: 2021-08-09 09:47:22 +0900
categories: [Design Pattern]
slug: post-104-design-patternproxy-pattern
---
{% raw %}

참조:<https://coding-factory.tistory.com/711>

### 프록시 패턴이란?

프록시는 대리인이라는 뜻으로 무엇인가를 대신 처리하는 의미이다.

일종의 비서라고 생각하면 된다.사장님한테 사소한 질문을 하기보다는 비서한테 먼저 물어보는 개념이라고 생각할 수 있다.이렇게 어떤 객체를 사용하고자 할때 객체를 직접적으로 참조하는 것이 아니라 해당 객체를 대행(대리.Proxy)하는 객체를 통해 대상 객체에 접근하는 방식을 사용하면 해당 객체가 메모리에 존재하지 않아도 기본적인 정보를 참조하거나 설정할 수 있고 또한 실제 객체의 기능이 반드시 필요한 시점까지 객체의 생성을 미룰 수 있다.

예를 들어 용량이 큰 이미지와 글이 같이 있는 문서를 모니터 화면에 띄운다고 가정하였을 때

이미지 파일은 용량이 크고 텍스트는 용량이 작아서 텍스트는 빠르게 나타나지만 그림은 조금 느리게 로딩되는 것을 본적이 있을 것이다.만약 이렇게 처리가 안되고 이미지와 텍스트가 모두 로딩이 된 후에야 화면이 나온다면

사용자는 페이지가 로딩될때까지 의미없이 기다려야 한다.그러므로 먼저 로딩이 되는 텍스트라도 먼저 나오는게 좋다.

이런 방식을 취하려면 텍스트 처리용 프로세서,그림 처리용 프로세스를 별도로 운영하면 된다.

이런 구조를 갖도록 설계하는 것이 바로 프록시 패턴이다.일반적으로 프록시는 다른 무언가와 이어지는 인터페이스의 역할을 하는 클래스를 의미한다.

### 프록시가 사용되는 대표적인 3가지

#### 가상프록시

꼭 필요로 하는 시점까지 객체의 생성을 연기하고 해당 객체가 생성된 것처럼 동작하도록 만들고 싶을때

사용하는 패턴이다.프록시 클래스에서 자잘한 작업들을 처리하고 리소스가 많이 요구되는 작업들이 필요할 때에만

주체 클래스를 사용하도록 구혀나며 위의 예와 같이 해상도가 아주 높은 이미지를 처리해야 하는 경우 작업을 분산하는 것을 예로 들 수 있다.

#### 원격프록시

원격 객체에 대한 접근을 제어 로컬 환경에 존재하며 원격객체에 대한 대변자 역할을 하는 객체 서로 다른 주소 공간에

있는 객체에 대한 마치 같은 주소 공간에 있는 것처럼 동작하게 만드는 패턴이다.

예시로 Google Docs를 보면 브라우저는 브라우저대로 필요한 자원을 로컬에 가지고 있고

또다른 자원은 Google 서버에 있는 형태이다.

#### 보호프록시

주체 클래스에 대한 접근을 제어하기 위한 경웨 객체에 대한 접근 권한을 제어하거나 객체마다 접근 권한을 달리하고 싶을 때 사용하는 패턴으로 프록시 클래스에서 클라이언트가 주체 클래스에 대한 접근을 허용할지 말지 결정하도록 할 수 있다.

### 프록시 패턴의 장단점

#### 프록시 패턴 장점

1. 사이즈가 큰 객체(ex:이미지)가 로딩되기 전에도 프록시를 통해 참조를 할 수 있다.
2. 실제 객체의 public.protected 메소드를을 숨기고 인터페이스를 통해 노출시킬 수 있다.
3. 로컬에 있지 않고 떨어져 있는 객체를 사용할 수 있다.
4. 원래 객체의 접근에 대해서 사전처리 할 수 있다.

#### 프록시 패턴 단점

1. 객체를 생성할때 한단계를 거치게 되므로,빈번한 객체 생성이 필요한 경우 성능이 저하될 수 있다.
2. 프록시 내부에서 객체 생성을 위해 스레드 생성,동기화가 구현되야 하는 경우 성능이 저하될 수 있다.
3. 로직이 난해해져 가독성이 떨어질 수 있다.

### 프록시 패턴 예제

```java
public interface Image {
   void displayImage();
}
```
```java
public class Real_Image implements Image {

    private String fileName;
    
    public Real_Image(String fileName) {
        this.fileName = fileName;
        loadFromDisk(fileName);
    }
    
    private void loadFromDisk(String fileName) {
        System.out.println("Loading " + fileName);
    }
    
    @Override
    public void displayImage() {
        System.out.println("Displaying " + fileName);
    }
}
```
```java
public class Proxy_Image implements Image {
    private Real_Image realImage;
    private String fileName;
    
    public Proxy_Image(String fileName) {
        this.fileName = fileName;
    }
    
    @Override
    public void displayImage() {
        if (realImage == null) {
            realImage = new Real_Image(fileName);
        }
        realImage.displayImage();
    }
}
```
```java
public class Proxy_Main {
    public static void main(String[] args) {
        Image image1 = new Proxy_Image("test1.png");
        Image image2 = new Proxy_Image("test2.png");
        
        image1.displayImage();
        System.out.println();
        image2.displayImage();
    }
}
```

#### 결과

```html
Loading test1.png
Displaying test1.png

Loading test2.png
Displaying test2.png
```
{% endraw %}