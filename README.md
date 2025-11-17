# 🍽️ SaveUs – AI 기반 식단 진단 & 건강습관 챌린지 플랫폼

SaveUs는 **AI 기반 식단 분석**을 통해 사용자의 식습관을 진단하고,  
개인 맞춤형 식단 유형 분석 + 건강 챌린지를 제공하는 **헬스케어 웹 서비스 플랫폼**입니다.

사용자는 매일 업로드하는 식단·활동 데이터를 기반으로  
식습관 유형 분석, 건강 점수, 챌린지 추천 등 다양한 맞춤 서비스를 받을 수 있습니다.

---

## 🚀 주요 기능

### 🔍 1. AI 식단 분석
- 이미지 기반 음식 분석 (OpenCV + TensorFlow)
- 영양정보 DB 매칭 후 1일 영양 리포트 생성
- 사용자 식습관 패턴 분석

### 🧬 2. 설문 기반 식단 유형 분석
- 사용자 설문 결과 기반
- 단백질 유형 / 지방 유형 / 탄수화물 유형 개별 진단
- 종합 식단 유형(DIET_TYPE) 생성 및 USER_DIET_TYPE 테이블 저장

### 👤 3. 회원 시스템
- 회원가입 / 로그인 / 로그아웃
- 이메일 중복 확인
- 닉네임 중복 확인
- 비밀번호 변경
- 회원탈퇴 기능

### 📝 4. 마이페이지
- 사용자 프로필 조회
- 설문 결과 기반 식단 유형 표시
- 목표 / 키 / 체중 / 프로필 이미지 확인

### 🛠 5. 프로필 수정
- 프로필 이미지 업로드 및 미리보기(JS)
- 목표·키·체중 수정 가능
- 비밀번호 변경 기능
- 입력값 유효성 검증

### 🎯 6. 챌린지 & 뱃지
- 챌린지 진행률 표시
- 기간 기반 진행률 갱신
- 향후 뱃지 시스템 연동 준비됨

---

## 🗂️ 프로젝트 폴더 구조
```
src
├─ main
│ ├─ java
│ │ ├─ controller
│ │ ├─ dto
│ │ ├─ mapper
│ │ ├─ config
│ │ └─ service
│ ├─ resources
│ │ ├─ mapper
│ │ ├─ templates
│ │ ├─ static/css
│ │ ├─ static/js
│ │ └─ application.properties
│
└─ uploads (프로필 이미지 저장)
```

---

## 🧩 기술 스택

### Backend
- **Java 17**
- **Spring Boot**
- **MyBatis**
- **Oracle DB**
- **Spring MVC**
- **Spring Validation**

### AI & 분석
- **Python Flask**
- **TensorFlow**
- **scikit-learn**
- **OpenCV**

### Frontend
- **Thymeleaf**
- **JavaScript / HTML / CSS**
- **Chart.js**

---

## 🗄️ DB 테이블 구조(중요 테이블)

### ✔ USERS
```sql
CREATE TABLE USERS (
    USER_ID NUMBER PRIMARY KEY,
    EMAIL VARCHAR2(100) NOT NULL UNIQUE,
    PASSWORD VARCHAR2(255) NOT NULL,
    NICKNAME VARCHAR2(50) NOT NULL,
    BIRTHDATE DATE,
    AGE NUMBER,
    GENDER VARCHAR2(10),
    HEIGHT NUMBER,
    CURRENT_WEIGHT NUMBER,
    MAIN_GOAL NUMBER NOT NULL,
    PROFILE_IMAGE_URL VARCHAR2(255),
    CREATED_AT DATE DEFAULT SYSDATE,
    STATUS VARCHAR2(20) DEFAULT 'ACTIVE',
    ROLE VARCHAR2(20) DEFAULT 'USER'
);
```

### ✔ USER_DIET_TYPE (설문 기반 식단 유형)
```
CREATE TABLE USER_DIET_TYPE (
    USER_ID NUMBER PRIMARY KEY,
    PROTEIN_TYPE VARCHAR2(20),
    FAT_TYPE VARCHAR2(20),
    CARB_TYPE VARCHAR2(20),
    DIET_TYPE VARCHAR2(50),
    UPDATED_AT TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID) ON DELETE CASCADE
);
```

🛠 설치 및 실행 방법
### 1. 프로젝트 클론
```
git clone https://github.com/Team-SaveUs/project_SaveUs.git
```
### 2. 백엔드 실행
```
./mvnw spring-boot:run
```

### 3. 프론트(Thymeleaf)
- Spring Boot와 함께 자동 실행됨

### 4. AI 서버 실행(Python)

📌 현재 진행 상황 요약

마이페이지 구현 완료

프로필 수정 구현 완료

이미지 업로드 정상 작동

설문 → USER_DIET_TYPE 저장 기능 동작

로그인·회원가입 모든 유효성검증 적용

향후 챌린지/뱃지 자동 생성 기능 확장 예정
