# drf_session3(User, Todo, Todocomments)

## DB 설계서
### 1. USER
+ id : int형, 고유값
+ username : char형, 유저이름
+ password : char형, 비밀번호
+ email : email형, unique, 이메일 입력
+ club : text형, 동아리 명

### 2. TODO
+ id : int형, 고유값
+ Todo_content : text형, todo 할 일 내용
+ Todo_comlete : boolean형, default값 False, 완료여부
+ Todo_created_at : datetime형, 작성시간 자동 등록


### 3. TODOCOMMENTS
+ id : int형, 고유값
+ content : text형, 댓글 내용
+ created_date : datetime형, 작성시간 자동 등록
+ author : fk, 작성자(고유값으로 구분)
+ post : fk, 작성글(고유값으로 구분)

----

## SERIALIZER
### 1. USERSERIALIZER
+ 회원가입 serialzer
+ fields=['id','username','email','password','club']
+ create 함수
  + email, username, club, password를 받고 회원가입

### 2. USERLOGINSERIALIZER
+ 로그인 serializer
+ email, password로 로그인
+ validate 함수
  + email과 password가 일치하는지 확인

### 3. TODOCOMMENTSERIALIZER
+ TODO(할 일 게시판) 댓글 serializer
+ fields=['id','post','author','content','created_at']

### 4. TODOSRIALZER
+ TODO(할 일 게시판) serializer
+ fields=['id','Todo_content','Todo_complete','Todo_created_at','Todo_comment']

----

## APIView
### 1. SignupView
+ post
  + 회원가입 기능
### 2. LoginView
+ post
  + 로그인 기능
### 3. TodoView
+ get
  + 할 일 리스트 전체 조회
+ post
  + 할 일 생성(업로드)
### 4. TodoDetailView
+ pk 값으로 특정 할 일 받아오기
+ get 
  + 특정 할 일 조회(+댓글)
+ delete
  + 특정 할 일 삭제
+ put 
  + 특정 할 일 수정
### 5. TodoCommentView
+ get
  + 댓글 전체 조회(+게시글)
+ post
  + 댓글 작성
  + 게시글 고유값으로 작성
### 6. TodoCommentDetailView
+ get
  + 특정 댓글 조회
  + 댓글 고유값으로 조회
+ put 
  + 특정 댓글 수정
+ delete
  + 특정 댓글 삭제
