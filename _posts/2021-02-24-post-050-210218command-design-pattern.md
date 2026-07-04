---
layout: default
title: "[210218]Command Design Pattern"
date: 2021-02-24 19:09:49 +0900
categories: [Design Pattern]
slug: post-050-210218command-design-pattern
---

### - 학습 목표 달성 확인 목록

**- [] 커맨드 디자인 패턴의 사용처를 설명할 수 있는가?**

한 개의 명령어를 처리하는 메서드를 별개의 클래스로 분리하는 기법이다.

이렇게 하면 명령어가 추가될 때마다 새 클래스를 만들면 되기 때문에 기존 코드를 손대지 않아서 유지보수에 좋다

즉 기존 소스코드를 건들지 않고 추가를 할수 있다는 장점이 있다

거기에 인터페이스를 이용하면 메서드 호출규칙을 단일화 할 수 있어 코딩의 일관성을 높혀줄 수 있다

그렇게 기능을 추가한 만큼 클래스 개수는 늘어난다.

**- [] 커맨드 패턴을 적용할 수 있는가?**

%[https://gist.github.com/osk2090/5a77340ba7714b16ab4b8d81a091e067]

```java
public interface Command {
    public void service() throws CloneNotSupportedException;
}
//맨 처음 메뉴에서 1,2,3번을 누르면 동작하는 메서드들을 service로 단일화 시켜 유지보수에 좀 더 편리하게 했다
```

**- [] 커맨드 패턴을 적용할 때 인터페이스 문법의 용도를 이해하는가?**

프로그래밍의 일관성을 위해 인터페이스 클래스를 이용하면 객체 사용규칙을 통일 할 수 있다는 장점이 있다.

**- [] Map 을 사용하여 객체를 다룰 수 있는가?**

```java
public static void main(String[] args) throws CloneNotSupportedException {
        ArrayList<Client> clientList = new ArrayList<>();

        HashMap<Integer, Command> commandMap = new HashMap<>();
        //입력한 숫자를 Key역할,Command 인터페이스로 엮은 service 메서드를 value로 선언했다.

        AdminCheckResultHandler adminCheckResultHandler = new AdminCheckResultHandler(clientList);
        AdminLogicHandler adminLogicHandler = new AdminLogicHandler(clientList);
        AdminWinnerCheckHandler adminWinnerCheckHandler = new AdminWinnerCheckHandler(clientList);
        AdminWinnerResultHandler adminWinnerResultHandler = new AdminWinnerResultHandler(clientList);

        ClientAddHandler clientAddHandler = new ClientAddHandler(clientList);
        ClientInfoHandler clientInfoHandler = new ClientInfoHandler(clientList);
        ClientStatusHandler clientStatusHandler = new ClientStatusHandler(clientList);
        ClientListHandler clientListHandler = new ClientListHandler(clientList);
        commandMap.put(1, new ClientPrintOneHandler(clientList, clientAddHandler));
        commandMap.put(2, new ClientPrintTwoHandler(clientList, adminCheckResultHandler,
                adminLogicHandler, clientInfoHandler, clientListHandler, adminWinnerResultHandler));
        commandMap.put(3, new ClientPrintThreeHandler(clientList, clientInfoHandler
                , adminWinnerCheckHandler));

        loop:
        while (true) {
            clientStatusHandler.statusPannel(adminWinnerResultHandler, clientInfoHandler);
            int choice = Prompt.promptInt("-Nike-\n-Draw-\n1. 응모자 2. 관리자 3. 당첨자 수령하기 4. History 0. 종료");

            commandStack.push(choice);//사용자가 입력한 명령을 보관
            commandQueue.offer(choice);

            try {
                switch (choice) {
                    case 4:
                        printCommandHistory(commandQueue.iterator());
                        break;
                    case 0:
                        System.out.println("종료합니다.");
                        break loop;
                    default:
                        Command commandHandler = commandMap.get(choice);

                        if (0 > choice || choice > 4) {//1,2,3에만 반응할 수 있게 만들었다.
                            System.out.println("다시 선택해주세요.");
                        } else {
                            commandHandler.service();//해당 번호의 메서드를 동작하게 만들었다.
                        }
                }
            } catch (Exception e) {
                System.out.println("==================================================");
                System.out.printf("명령어 실행중 오류 발생: %s = %s\n", e.getClass().getName(), e.getMessage());
                System.out.println("==================================================");
            }
        }
    }
```