## 1. 개발 환경

Visual Studio Code

![vscode](https://github.com/user-attachments/assets/cea98ce7-de28-4928-842a-a859b6aced35)

**사용한 프레임 워크**

PySide6

<img width="328" height="153" alt="pyside6image" src="https://github.com/user-attachments/assets/527a6fc0-57c5-4256-a458-3763d5c3e057" />

## 2. 사용한 언어

Python

![bf534326c82256e07ebcf3a115ed38f5e86a8fb61ea5db06aac1c5195b72e17db21c18b364865e765c22de9795a736590d630966d7d887a17a023fc6ce4bc7b3e6fa33322a215727df10002f4d1ae06b41cc18027fae6b6bce8187e715eed522](https://user-images.githubusercontent.com/62977669/148309905-f7dbb320-8b73-484f-98de-bc5e991ef6f1.png)

## 3. 실행 화면

![python 2025-12-23 13-07-20](https://github.com/user-attachments/assets/455a4dfe-62ba-4b87-adc0-880b4c99d7d3)

## 4. 기능 설명

이 애플리케이션은 PySide6와 SQLite를 사용한 간단한 게시판 프로그램입니다.
게시글의 작성, 조회, 수정, 삭제 (CRUD) 기능을 제공하며 
QStackedWidget과 Signal-Slot 구조를 사용해 페이지 간 전환을 구현했습니다.

**▪게시글 목록 조회**

프로그램 실행 시 게시글 목록이 표시됩니다.
각 게시글은 제목과 작성일 기준으로 확인할 수 있으며,
게시글 선택 시 상세 조회 페이지로 이동합니다.

**▪ 게시글 작성**

‘글쓰기’ 버튼을 통해 게시글 작성 페이지로 이동할 수 있습니다.
제목과 내용을 입력한 후 저장 시 SQLite 데이터베이스에 게시글이 저장되며,
입력값이 없을 경우 저장되지 않도록 유효성 검사를 수행합니다.

**▪ 게시글 상세 조회**

목록에서 게시글을 선택하면 상세 조회 페이지로 이동합니다.
제목, 작성자, 작성일, 수정일, 내용을 읽기 전용으로 확인할 수 있으며
수정, 삭제, 목록 이동 기능을 제공합니다.

**▪ 게시글 수정**

상세 조회 페이지에서 수정 버튼을 클릭하면 수정 페이지로 이동합니다.
기존 게시글 내용을 불러와 수정할 수 있으며,
저장 시 수정일(updated_at)이 갱신됩니다.

**▪ 게시글 삭제**

상세 조회 페이지에서 삭제 버튼을 클릭하면
삭제 확인 메시지를 통해 사용자 확인 후 게시글이 삭제됩니다.
삭제 완료 후 목록 페이지로 이동합니다.

