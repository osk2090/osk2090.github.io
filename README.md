## Welcome to GitHub Pages

오은석의 홈페이지!

You can use the [editor on GitHub](https://github.com/osk2090/osk2090.github.io/edit/main/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/osk2090/osk2090.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.


### \- 학습 목표 달성 확인 목록

**\- \[\] mutable 객체와 immutable 객체의 차이를 예를 들어 설명할 수 있는가?**

String 객체는 immutable(불변) 객체이다.즉 한번 객체에 값을 담으면 변경할 수 없다.

값 자체를 변경할 수 없지만 새로운 String 객체를 만든다.

replace:왼쪽값을 오른쪽값으로 변환하여 새로운 객체를 만든다.하지만 원본 데이터는 변하지 않는다.

concat:원본값에 해당 값을 합쳐서 새로운 객체를 만든다.

```
 String s1 = new String("Hello");
 
    String s2 = s1.replace('l', 'x');
    System.out.printf("%s : %s\n", s1, s2); // 원본은 바뀌지 않는다.

    String s3 = s1.concat(", world!");
    System.out.printf("%s : %s\n", s1, s3); // 원본은 바뀌지 않는다.
    
    //결과
    Hello : Hexxo
    Hello : Hello, world!
```

**반면에 StringBuffer 객체는 mutable 객체이다.**

**해당 인스턴스의 데이터를 직접 변경할 수 있다.**

**원래의 문자열을 변경하고 싶을 때 사용하는 클래스이다.**

```
StringBuffer buf = new StringBuffer("Hello");
    System.out.println(buf);

    buf.replace(2, 4, "xxxx");// 원본을 바꾼다.
    System.out.println(buf);
    
    //결과
    Hello
    Hexxxxo

```

**\- \[\] 리터럴로 만든 String 객체와 new 로 만든 String 객체의 차이점을 설명할 수 있는가?**

```
public class Sp {
    public static void main(String[] args) {
        String name = "osk";
        String name1 = new String("osk");

        System.out.println(name == name1);
        System.out.println(name.equals(name1));

    }
}

//결과
false
true

```

String name = ""으로 생성된 문자열은 Heap 메모리에 String pool(상수풀)이라는 공간이 있는데 여기에 문자열을 할당하게 된다.

여기서 특징은 같은 문자열이 있는지 확인해서 있다면 단 하나만 생성해서 메모리를 절약할 수 있는 장점이 있다.

반면에 String name1 = new String("")으로 생성된 문자열은 우리가 일반적으로 아는 Heap 메모리에는 해당 문자열을 할당

Stack 메모리에는 Heap 메모리에 저장된 곳의 주소값을 저장한다.그래서 상수풀과는 달리 같은 문자열을 선언해도 따로따로 메모리를 할당하기 때문에 메모리 낭비가 있다.

상수풀의 경우

```
        String name1 = "osk";
        String name2 = "osk";

        System.out.println(name1.hashCode());
        System.out.println(name2.hashCode());
        System.out.println(name1 == name2);
        
        //결과
        110343
        110343
        true
        hashcode()메서드로 확인하면 주소값이 같은걸 볼 수 있다.
        그렇기에 ==연산자로 확인해보면 true가 나오는것을 확인할 수 있다.
```

객체의 경우

```
        String name1 = "osk";
        String name3 = new String("osk");
        String name4 = new String("osk");

        System.out.println(name1 == name3);
        System.out.println(name3 == name4);

        System.out.println(name1.equals(name3));
        System.out.println(name3.equals(name4));
        
        //결과
        false//주소값이 다르기때문에 false
        false//각각 다른 객체를 생성했기에 주소값이 다르다 그래서 false
        true//문자열 데이터를 직접 확인하기에 true
        true//동일
```

**\- \[\] 래퍼(wrapper) 클래스의 용도와 사용법을 알고 있는가?**

<table style="border-collapse: collapse; width: 82.326%; height: 290px;" border="1" data-ke-style="style3"><tbody><tr style="height: 19px;"><td style="text-align: center; height: 19px;">기본 타입</td><td style="text-align: center; height: 19px;">래퍼 클래스</td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">byte</td><td style="text-align: center; height: 19px;">Byte</td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">short</td><td style="text-align: center; height: 19px;">Short</td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">int</td><td style="text-align: center; height: 19px;"><b>Integer</b></td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">long</td><td style="text-align: center; height: 19px;">Long</td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">float</td><td style="text-align: center; height: 19px;">Float</td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">double</td><td style="text-align: center; height: 19px;">Double</td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">char</td><td style="text-align: center; height: 19px;"><b>Character</b></td></tr><tr style="height: 19px;"><td style="text-align: center; height: 19px;">boolean</td><td style="text-align: center; height: 19px;">Boolean</td></tr></tbody></table>

primitive data type를 객체처럼 다룰 수 있도록 자바에서 제공한다.

포장하는 객체라고 해서 wrapper 클래스라고 부른다.

primitive data type의 값을 객체로 주고 받을 때 사용한다.

primitive data type의 값을 객체에 담아 전달하고 싶다면

언제든 wrapper 클래스의 인스턴스를 만들면 된다.

가장 큰 목적은 

primitive data type을 포함해서 모든 값을 쉽게 주고 받기 위해서이다.

[##_Image|kage@cQlrSh/btqVFBMu09T/PFQ4Xh26CcRGjJVuazkRZ0/img.png|alignCenter|data-origin-width="0" data-origin-height="0" data-ke-mobilestyle="widthContent"|||_##]

그림과 같이 기본 타입의 데이터를 래퍼 클래스의 인스턴스로 변환하는 과정을 박싱(boxing)이라고 한다.

반대로 래퍼 클래스의 인스턴스에 저장된 값을 다시 기본 타입의 데이터로 꺼내는 과정을 언박싱(unboxing)이라고 한다.

이것을 수동으로하면 개발자가 너무 힘들다 그래서 자동으로 변환을 해주는 기능이 있다.

```
primitive data type 값을 Wrapper 클래스의 인스턴스에 바로 할당할 수 있다.
    //
    Integer obj = 100; // ==> Integer.valueOf(100)

    // obj는 레퍼런스인데 어떻게 가능한가?
    // => 내부적으로 Integer.valueOf(100) 호출 코드로 바뀐다.
    // => 즉 int 값이 obj에 바로 저장되는 것이 아니라,
    //    내부적으로 Integer 객체가 생성되어 그 주소가 저장된다.
    // => 이렇게 int 값을 자동으로 Integer 객체로 만드는 것을
    //    "오토박싱(auto-boxing)"이라 한다.
```

```
Wrapper 객체의 값을 primitive data type 변수에 직접 할당할 수 있다.
    //
    Integer obj = Integer.valueOf(300);
    int i = obj; // ==> obj.intValue()

    // obj에 저장된 것은 int 값이 아니라 Integer 객체의 주소인데 어떻게 가능한가?
    // => 내부적으로 obj.intValue() 호출 코드로로 바뀐다.
    // => 즉 obj에 들어있는 인스턴스 주소가 i에 저장되는 것이 아니라,
    //    obj 인스턴스에 들어 있는 값을 꺼내 i에 저장하는 것이다.
    // => 이렇게 Wrapper 객체 안에 들어 있는 값을 자동으로 꺼낸다고 해서
    //    "오토언박싱"이라 부른다.
```

**\- \[\] java.util.Date, java.sql.Date, java.util.Calendar 클래스를 사용할 수 있는가?**

```
    // Date(long) : 1970-01-01 00:00:00 부터 지금까지 경과된 밀리초
    Date d2 = new Date(1000);
    System.out.println(d2);
    
    // java.sql.Date
    java.sql.Date d5 = new java.sql.Date(System.currentTimeMillis());//현재시간 출력
    System.out.println(d5);
```

**\- \[\] 기능을 확장하기 위해 사용하는 기법의 유형을 설명할 수 있는가?**

1) 기존 클래스에 코드를 추가하는 방법

 \- 기존 코드를 변경하게 되면 원래 되던 기능도 오류가 발생할 수 있는 위험이 있다.

 \- 그래서 원래 코드를 손대는 것은 매우 위험한 일이다.

 \- 기존에 잘 되던 기능까지 동작이 안되는 문제가 발생할 수 있기 때문이다.

2) 기존 코드를 복사하여 새 클래스를 만드는 방법

 \- 장점

 \- 기존 코드를 손대지 않기 때문에 문제가 발생할 가능성은 줄인다.

 \- 단점

 \- 기존 코드의 크기가 큰 경우에는 복사 붙여넣기가 어렵다.

 \- 기존 클래스의 소스가 없는 경우에는 이 방법이 불가능하다.

 엥? 다른 개발자가 배포한 라이브러리만 있는 경우를 말한다.

 소스가 없는 다른 개발자가 만든 클래스에 기능을 덧 붙일 때는 이 방법이 불가능하다.

 \- 기존 코드에 버그가 있을 때 복사 붙여넣기 해서 만든 클래스도 영향을 받는다.

 \- 기존 코드를 변경했을 때 복사 붙여넣기 한 모든 클래스를 찾아 변경해야 한다.

3) 기존 코드를 상속 받아 기능을 추가하는 방법

 \- 장점

 \- 기존 클래스의 소스 코드가 필요 없다.

 \- 간단한 선언으로 상속 받겠다고 표시한 후 새 기능만 추가하면 된다.

 \- 단점

 \- 일부 기능만 상속 받을 수 없다.

 \- 쓰든 안쓰든 모든 기능을 상속 받는다.

**\- \[\] 상속을 이용하여 기능을 확장할 수 있는가?**

```
public class Score {

  public String name;
  public int kor;
  public int eng;
  public int math;
  public int sum;
  public float aver;

  public void compute() {
    this.sum = this.kor + this.eng + this.math;
    this.aver = this.sum / 3f;
  }
}
```

```
public class Score2 extends Score {

  // 새 필드를 추가한다.
  public int music;
  public int art;


  // 기존 코드를 변경한다.
  @Override
  public void compute() {
    this.sum = this.kor + this.eng + this.math + this.music + this.art;
    this.aver = this.sum / 3f;
  }
}
```

```
public class Exam03 {
  public static void main(String[] args) {

    Score2 s = new Score2();
    s.name = "홍길동";
    s.kor = 100;
    s.eng = 100;
    s.math = 100;
    s.music = 100;
    s.art = 100;
    s.compute();

    System.out.printf("%s: %d(%.1f)\n", s.name, s.sum, s.aver);
  }
}
```

**\- \[\] 수퍼 클래스와 서브 클래스의 용어를 이해하는가?**

```
public class A {//A클래스의 슈퍼클래스는 Object
  void m1() {
    System.out.println("A.m1()");
  }
}
```

```
public class B extends A {//B클래스의 슈퍼클래스는 A클래스
  public void m2() {
    System.out.println("B.m2()");
  }
}
```

```
public class C extends B {//C클래스의 슈퍼클래스는 B클래스
  public void m3() {
    System.out.println("C.m3()");
  }
}

```

```
public class D extends C {//D클래스의 슈퍼클래스는 C클래스
  public void m4() {
    System.out.println("D.m4()");
  }
}

```

```
    D obj = new D();
    obj.m4(); // obj 레퍼런스의 클래스에서 m4()를 찾아 호출한다.
    obj.m3(); // obj 레퍼런스의 클래스(D)에서 m3()를 찾아보고 없다면 수퍼 클래스에서 찾는다.
    obj.m2(); // 만약 D의 수퍼 클래스에서도 못찾는다면 그 위의 클래스에서 찾아본다.
    obj.m1(); // 그 위에 클래스에서도 없다면 더 위에 클래스에서 찾아본다.
    //obj.m0(); // 더 위에 있는 클래스에서도 찾을 수 없다면 컴파일 오류이다!
```

**\- \[\] 상속 관계에 있는 클래스의 인스턴스 생성 과정을 이해하는가?**

```
public class A {
  int v1;

  static { 
    System.out.println("A클래스의 static{} 실행!");
  }
}
```

```
public class B extends A {
  int v2;

  static {
    System.out.println("B클래스의 static{} 실행!");
  }
}
```

```
B obj = new B();

    obj.v2 = 200; // B 클래스 설계도에 따라 만든 변수
    obj.v1 = 100; // A 클래스 설계도에 따라 만든 변수

    System.out.printf("v2=%d, v1=%d\n", obj.v2, obj.v1);
    System.out.println("---------------------------------");

    // 클래스는 오직 한 번만 로딩된다.
    // - 그래서 static 블록도 위에서 한 번 실행되면 다시 실행하지 않는다.
    //
    B obj2 = new B();
    obj2.v2 = 2000;
    obj2.v1 = 1000;
    System.out.printf("v2=%d, v1=%d\n", obj2.v2, obj2.v1);

//결과
A클래스의 static{} 실행!
B클래스의 static{} 실행!
v2=200, v1=100
---------------------------------
v2=2000, v1=1000


인스턴스 생성 절차 정리!
    // 1) 상속 받은 수퍼 클래스를 먼저 메모리에 로딩한다.
    //    이미 로딩되어 있다면 다시 로딩하지는 않는다.
    // 2) 그런 후 해당 클래스를 메모리에 로딩한다.
    //    마찬가지로 이미 로딩되어 있다면 다시 로딩하지는 않는다.
    // 3) 수퍼 클래스에 선언된 대로 인스턴스 변수를 Heap에 만든다.
    // 4) 해당 클래스에 선언된 대로 인스턴스 변수를 Heap에 만든다.
    // 5) 수퍼 클래스부터 생성자를 실행하며 해당 클래스까지 내려온다.
```

**\- \[\] 상속 관계에 있는 클래스의 생성자 호출 과정을 이해하는가?**

```
public class A /*extends Object*/ {
  int v1;

  A() {
    // 수퍼 클래스의 어떤 생성자를 호출할지 지정하지 않으면 컴파일러는
    // 다음과 같이 수퍼 클래스의 기본 생성자를 호출하라는 명령을 붙인다.
    //    super(); // 즉 개발자가 붙이지 않으면 자동으로 붙인다.

    System.out.println("A() 생성자!");
    this.v1 = 100;
    //super();//뒤에 붙이면 컴파일에러가 뜬다
  }
}
```

```
public class B extends A {
  int v2;

  B() {
    System.out.println("B() 생성자!");
    this.v2 = 200;
  }
}
```

```
public class C extends B {
  int v3;

  C() {
    System.out.println("C() 생성자!");
    this.v3 = 300;
  }
}

```

```
C obj = new C();
    System.out.printf("v1=%d, v2=%d, v3=%d\n", obj.v1, obj.v2, obj.v3);
    
    //결과
    A() 생성자!
    B() 생성자!
    C() 생성자!
    v1=100, v2=200, v3=300

```

**\- \[\] 수퍼 클래스의 생성자를 호출하는 \`super()\` 의 사용법을 아는가?**

```
public class A /*extends Object*/ {
  int v1;
  
  A(int value) {
    this.v1 = value;
    System.out.println("A(int) 생성자!");
  }
}
```

```
public class B extends A {
  int v2;

  B() {
  	//부모클래스의 기본생성자를 호출하라는 명령이 있으면
    // - 개발자가 직접 수퍼 클래스에 있는 생성자를 호출해야된다
    super(100);
    System.out.println("B() 생성자!");
  }
}
```

```
public class Exam01 {
  public static void main(String[] args) {
    B obj = new B();
    System.out.printf("v1=%d, v2=%d\n", obj.v1, obj.v2);
  }
}

//결과
A(int) 생성자!
B() 생성자!
v1=100, v2=0
```

**\- \[\] 자바에서 다중 상속을 지원하지 않는 이유를 아는가?**

만약 두 클래스를 상속받을때,

필드나 메서드의 이름이 같다면 개발자에게 혼동이 올 수 있으므로 자바에서는 다중 상속을 지원하지 않는다.  

**\- \[\] specialization과 generalization 상속 기법을 설명할 수 있는가?**

specialization:예를 들면 자동차는 승용차와 트럭으로 나뉜다.

```
public class Car {
    void engine() {
        System.out.println("부릉부릉");
    }

    void tire() {
        System.out.println("금호타이어");
    }

    void caution() {
        System.out.println("빵빵");
    }
}
```

Car 클래스를 상속받으며 각 차종에 다르게 기능이 있는 것을 말한다.이것이 specialization!

```
public class Benz extends Car {
    void trunk() {
        System.out.println("트렁크를 열어 짐을 싣는다.");
    }
}
```

```
public class Truck extends Car {
    void function() {
        System.out.println("덤프기능");
    }
}
```

generalization:반대로 공통 필드나 메서드를 한대 묶어서 관리하는 것을 말한다.

그렇게 되면 Car클래스가 generalization 한것이다.

**\- \[\] 추상 클래스의 용도와 사용법을 아는가?**

**주로 generalization 과정에서 정의 슈퍼클래스에 대해 추상 클래스로 설정한다.**

**그래서 나중에 서브 클래스에서 필드나 메서드를 선언한다.**

주의할 점은 추상클래스는 인스턴스 생성이 불가하다.(new생성자를 사용한 인스턴스화)

```
abstract class A{
...
}
```

**\- \[\] 추상 메서드의 용도와 사용법을 아는가?**

```
public abstract class ab1 {
    abstract void m1();
}
```

```
public abstract class ab2 extends ab1 {
    abstract void m2();
}
```

```
public class aabb {
    public static void main(String[] args) {
        ab2 a = new ab2() {
            @Override//오버라이딩을 이용하여 추상메서드의 body를 완성한다.
            void m1() {
                System.out.println("1");
            }

            @Override//오버라이딩을 이용하여 추상메서드의 body를 완성한다.
            void m2() {
                System.out.println("2");
            }
        };
        a.m1();
        a.m2();
    }
}

//결과
1
2
```

서브 클래스에서 재정의 해야만 하고 슈퍼클래스에서 구체적으로 구현하지 않는것이 좋다.