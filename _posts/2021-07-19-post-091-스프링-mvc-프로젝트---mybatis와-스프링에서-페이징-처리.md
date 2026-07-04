---
layout: default
title: "스프링 MVC 프로젝트 - MyBatis와 스프링에서 페이징 처리"
date: 2021-07-19 09:16:35 +0900
categories: [Spring]
slug: post-091-스프링-mvc-프로젝트---mybatis와-스프링에서-페이징-처리
image: /images/91/img.png
---

MyBatis는 SQL을 그대로 사용할 수 있기 때문에 인라인뷰를 이용하는 SQL을 작성하고

필요한 파라미터를 지정하는 방식으로 페이징 처리를 하게 된다.여기서 신경써야 하는 점은 페이징 처리를 위해서는 SQL을 실행할 때 몇 가지 파라미터가 필요하다는 점이다.

페이징 처리를 위해서 필요한 파라미터는

1. 페이지 번호
2. 한 페이지당 몇 개의 데이터를 보여줄 것인지가 결정되어야만 한다.

페이지 번호와 몇 개의 데이터가 필요한지를 별도의 파라미터로 전달하는 방식도 나쁘지는 않지만

아예 이 데이터들을 하나의 객체로 묶어서 전달하는 방식이 나중을 생각하면 좀 더 확장성이 좋다.

com.osk2090.domain 패키지에 Criteria 이름의 클래스를 작성한다.Criteria는 검색의 기준을 의미한다.

Criteria.class

```java
package com.osk2090.domain;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class Criteria {
    private int pageNum;
    private int amount;

    public Criteria() {
        this(1, 10);
    }

    public Criteria(int pageNum, int amount) {
        this.pageNum = pageNum;
        this.amount = amount;
    }
}
```

Criteria 클래스의 용도는 pageNum과 amount 값을 같이 전달하는 용도지만 생성자를 통해서 기본값을 1페이지,10개로 지정해서 처리한다.Lombok을 이용해서 getter/setter를 생성해 준다.

### MyBatis 처리와 테스트

BoardMapper는 인터페이스와 어노테이션을 이용하기 때문에 페이징 처리와 같이 경우에 따라 SQL 구문 처리가 필요한 상황에서는 복잡하게 작성된다.

com.osk2090.mapper 패키지의 BoardMapper에는 위애서 작성한 Criteria 타입을 파라미터로 사용하는 getListWithPaging() 메서드를 작성한다.

BoardMapper.interface

```java
package com.osk2090.mapper;

import com.osk2090.domain.BoardVO;
import com.osk2090.domain.Criteria;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface BoardMapper {
...

    public List<BoardVO> getListWithPaging(Criteria cri);
...
}
```

기존에 만들어둔 src/main/resources의 BoardMapper.xml에 getListWithPaging에 해당하는 태그를 추가한다.

BoardMapper.xml

```sql
<select id="getListWithPaging" resultType="com.osk2090.domain.BoardVO">
    <![CDATA[
        select bno,title,content,writer,regdate,updatedate
            from
            (
                select /*+index_desc(tbl_board pk_board)*/
                rownum rn,bno,title,content,writer,regdate,updatedate
                from
                tbl_board
                where rownum<=20
            )
        where rn>10
    ]]>
</select>
```

작성된 BoardMapper.xml에서는 xml의 CDATA 처리가 들어간다.

CDATA 섹션은 xml에서 사용할 수 없는 부등호를 사용하기 위함인데, xml을 사용할 경우에는 '<,>'는 태그로 인식하는데

이로 인해 생기는 문제를 막기 위함이다.

인라인뷰에서는 BoardVO를 구성하는데 필요한 모든 칼럼과 ROWNUM을 RN이라는 가명을 이용해서 만들어 주고 바깥쪽 SQL에서는 RN 칼럼을 조건으로 처리한다.

#### 페이징 테스트와 수정

MyBatis의 '#{}'를 적용하기 전에 xml 설정이 제대로 동작하는지 테스트를 먼저 진행하는 것이 좋다.

테스트 환경은 이미 준비되어 있으므로 간단히 테스트 코드만을 추가할 수 있다.

src/test/java 내에 있는 BoardMapperTests 클래스에 메서드를 추가한다.

BoardMapperTests.class

```java
@Test
public void testPaging() {
    Criteria cri = new Criteria();
    List<BoardVO> list = mapper.getListWithPaging(cri);
    list.forEach(board -> log.info(board));
}
```

Criteria 클래스에서 생성된 객체는 pageNum()은 1,amount는 10이라는 기본값을 가지므로 별도의 파라미터 없이 생성한다.현재는 파라미터의 값이 반영되지 않았으므로 2페이지의 내용이 정상적으로 나오는지 확인한다.

```html
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914967, title=asda, content=sd, writer=asd, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914966, title=asdasd, content=asdasd, writer=asdad, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914965, title=asd, content=asd, writer=asd, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914964, title=asd, content=asf, writer=asd, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914963, title=TTTT, content=CCCC, writer=WWWW, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914962, title=ooo, content=ooo, writer=ooo, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914961, title=oo, content=oo, writer=oo, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914960, title=o, content=o, writer=o, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914959, title=title, content=content, writer=osk, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
INFO : com.osk2090.mapper.BoardMapperTest - BoardVO(bno=8914958, title=새로 작성하는 글, content=새로 작성하는 내용, writer=newbie, regdate=Wed Jul 14 18:20:39 KST 2021, updatedate=Wed Jul 14 18:20:39 KST 2021)
```

SQL에 문제가 없다는 것을 확인했다면 이제 Criteria 객체 내부의 값을 이용해서 SQL이 동작하도록 수정한다.

20과 10이라는 값은 결국 pageNum과 amount를 이용해서 조정되는 값이다.

![](/images/91/img.png)

BoardMapper.xml을 수정해서 페이지 번호(pageNum)와 데이터 수(amount)를 변경할 수 있게 수정한다.

BoardMapper.xml

```sql
    <select id="getListWithPaging" resultType="com.osk2090.domain.BoardVO">
        <![CDATA[
        select bno, title, content, writer, regdate, updatedate
        from (
                 select /*+index_desc(tbl_board pk_board)*/
                     rownum rn,
                     bno,
                     title,
                     content,
                     writer,
                     regdate,
                     updatedate
                 from tbl_board
                 where rownum <= #{pageNum} * #{amount}
             )
        where rn > (#{pageNum} - 1) * #{amount}
    ]]>
    </select>
```

SQL의 동작에 문제가 없는지 확인해야 한다.이전의 testPaging()을 조금 수정해서 확인하도록 한다.

BoardMapperTests.class

```java
@Test
public void testPaging() {
    Criteria cri = new Criteria();
    //10개씩 3페이지
    cri.setPageNum(3);
    cri.setAmount(10);

    List<BoardVO> list = mapper.getListWithPaging(cri);
    list.forEach(board -> log.info(board.getBno()));
}
```

확인을 위해서 Criteria 객체를 생성할 때 파라미터를 추가해보거나, setter를 이용해서 내용을 추가한다.

위의 경우는 한 페이지당 10개씩 출력하는 3페이지에 해당하는 데이터를 구한 것이다.

테스트 코드가 동작한 후에는 SQL Developer에서 실행된 결과와 동일한지 체크하고 페이지 번호를 변경해서 정상적으로 처리되는지 확인한다.

### BoardController와 BoardService 수정

페이징 처리는 브라우저에서 들어오는 정보들을 기준으로 동작하기 때문에 Board Controller와 BoardService역시 전달되는 파라미터들을 받는 형태로 수정해야 한다.

#### BoardService 수정

BoardService는 Criteria를 파라미터로 처리하도록 BoardService 인터페이스와 boardServiceImpl 클래스를 수정한다.

BoardService.interface

```java
package com.osk2090.service;

import com.osk2090.domain.BoardVO;
import com.osk2090.domain.Criteria;

import java.util.List;

public interface BoardService {
...

//    public List<BoardVO> getList();

    public List<BoardVO> getList(Criteria cri);
}
```

BoardServiceImpl.class

```java
package com.osk2090.service;

import com.osk2090.domain.BoardVO;
import com.osk2090.domain.Criteria;
import com.osk2090.mapper.BoardMapper;
import lombok.AllArgsConstructor;
import lombok.Setter;
import lombok.extern.log4j.Log4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Log4j
@Service
@AllArgsConstructor
public class BoardServiceImpl implements BoardService {
...

//    @Override
//    public List<BoardVO> getList() {
//        log.info("getList");
//        return mapper.getList();
//    }

    @Override
    public List<BoardVO> getList(Criteria cri) {
        log.info("get List with criteria: " + cri);
        return mapper.getListWithPaging(cri);
    }

}
```

원칙적으로는 BoardService 쪽에 대한 수정이 이루어 쪗으니 이에 대한 테스트를 진행한다.

메서드를 수정하면 이미 테스트 코드 역시 에러가 발생하므로 다음과 같이 수정해서 테스트 진행한다.

BoardServiceTest.class

```java
@Test
public void testGetList() {
		//service.getList().forEach(board -> log.info(board));
		service.getList(new Criteria(2, 10)).forEach(board -> log.info(board));
}
```

#### BoardController 수정

기존 BoardController와 list()는 아무런 파라미터가 없이 처리되었기 때문에 pageNum과 amount를 처리하기 위해서 아래과 같이 수정한다.

BoardController.class

```java
package com.osk2090.controller;

import com.osk2090.domain.BoardVO;
import com.osk2090.domain.Criteria;
import com.osk2090.service.BoardService;
import lombok.AllArgsConstructor;
import lombok.extern.log4j.Log4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@Log4j
@RequestMapping("/board/")
@AllArgsConstructor
public class BoardController {
    private BoardService service;

//    @GetMapping("/list")
//    public void list(Model model) {
//        log.info("list");
//        model.addAttribute("list", service.getList());
//    }

    @GetMapping("/list")
    public void list(Criteria cri, Model model) {
        log.info("list: " + cri);
        model.addAttribute("list", service.getList(cri));
    }

    ...
}
```

Criteria 클래스를 하나 만들어 두면 위와 같이 편하게 하나의 타입만으로 파라미터나 리턴 타입을 사용할 수 있기 때문에 여러모로 편리하다.

BoardController 역시 이전에 테스트를 진행했으므로 pageNum과 amount를 파라미터로 테스트한다.

BoardControllerTests.class

```java
@Test
public void testListPaging()throws Exception {
  log.info(mockMvc.perform(
  MockMvcRequestBuilders.get("/board/list")
  .param("pageNum", "2")
  .param("amount" , "50"))
  .andReturn().getModelAndView().getModelMap()
);
```