# SaveUs

## 🌟 프로젝트 소개 (Project Introduction)
**SaveUs**는 사용자의 건강을 종합적으로 관리하고 개선하기 위한 AI 기반 헬스케어 플랫폼입니다.
이 프로젝트는 사용자가 섭취하는 음식을 자동으로 인식하고, 개인의 건강 상태에 맞춘 운동을 추천하며, 당뇨와 같은 질병 위험도를 예측하여 예방할 수 있도록 돕습니다.

Spring Boot 백엔드와 다양한 Python AI 모델(FastAPI)이 연동되어 작동하는 마이크로서비스 아키텍처를 지향합니다.

## 📚 목차 (Table of Contents)
- [프로젝트 소개](#-프로젝트-소개-project-introduction)
- [주요 기능](#-주요-기능-key-features)
- [기술 스택](#-기술-스택-tech-stack)
- [프로젝트 구조](#-프로젝트-구조-project-structure)
- [설치 및 실행 방법](#-설치-및-실행-방법-installation--execution)
- [기여 방법](#-기여-방법-contributing)
- [라이선스](#-라이선스-license)

## 🔑 주요 기능 (Key Features)

### 1. 음식 인식 및 영양 분석 (Food Detection)
- 📸 **AI 카메라**: 스마트폰이나 웹캠으로 음식 사진을 찍으면 YOLO 기반 딥러닝 모델이 음식을 자동으로 인식합니다.
- 🥗 **영양소 계산**: 인식된 음식의 칼로리 및 영양 성분을 자동으로 계산하여 식단 관리를 돕습니다.

### 2. 맞춤형 운동 추천 (Exercise Recommendation)
- 🏋️‍♂️ **개인화 추천**: 사용자의 신체 정보와 건강 목표에 맞춰 최적의 운동 루틴을 제안합니다.

### 3. 질병 위험도 예측 (Disease Risk Prediction)
- 🏥 **당뇨 위험 예측**: 사용자의 건강 검진 데이터와 생활 습관 데이터를 ML 모델(XGBoost)로 분석하여 당뇨 발병 위험도를 예측합니다.
- 📊 **영양 위험도 분석**: 식습관 패턴을 분석하여 영양 결핍이나 과다 섭취 위험을 경고합니다.

## 🛠 기술 스택 (Tech Stack)

### Backend Service
- **Language**: Java 17
- **Framework**: Spring Boot 3.4.9
- **Build Tool**: Maven
- **Database**: Oracle, MySQL, H2
- **ORM**: Spring Data JPA, MyBatis (혼용)
- **Template Engine**: Thymeleaf

### AI & Deep Learning Service
- **Language**: Python 3.10+
- **Framework**: FastAPI (API Serving)
- **Deep Learning**: PyTorch, torchvision
- **Object Detection**: Ultralytics YOLOv8 (Food Detection)
- **Machine Learning**: XGBoost (Diabetes Prediction), Scikit-learn
- **Data Analyze**: Pandas, NumPy
- **Image Processing**: OpenCV, Pillow

## 📂 프로젝트 구조 (Project Structure)
```bash
SaveUs/
├── spring/                  # Java Spring Boot Main Application
│   ├── src/main/java       # Source code
│   └── pom.xml             # Maven dependencies
└── python/                  # Python AI Microservices
    ├── food_detection/     # 음식 인식 서비스 (FastAPI + YOLO)
    ├── exercise_recommend/ # 운동 추천 알고리즘
    ├── diabetes-risk-ml-xgb/ # 당뇨 위험 예측 모델
    └── nutritional_risk/   # 영양 위험도 분석 로직
```

## 🚀 설치 및 실행 방법 (Installation & Execution)

### 1. 사전 준비 (Prerequisites)
- **Java**: JDK 17 이상 설치
- **Python**: 3.8 이상 설치
- **Database**: MySQL 또는 Oracle 데이터베이스가 실행 중이어야 합니다.

### 2. 저장소 복제 (Clone)
```bash
git clone https://github.com/jeongryuni/project_SaveUs.git
cd project_SaveUs
```

### 3. Spring Boot 백엔드 실행
Spring Boot 애플리케이션은 메인 웹 서버 역할을 합니다.

```bash
cd spring
# Windows
mvnw.cmd spring-boot:run

# Mac/Linux
./mvnw spring-boot:run
```
* 서버는 기본적으로 `http://localhost:8080`에서 실행됩니다.

### 4. Python AI 서비스 실행
각 AI 기능은 별도의 API 서버로 동작할 수 있습니다. 예시로 **음식 인식(Food Detection)** 서비스를 실행하는 방법입니다.

```bash
cd ../python/food_detection

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```
* Python 서버 주소는 각 `main.py` 설정에 따릅니다 (보통 `http://localhost:8000`).

## 🤝 기여 방법 (Contributing)
SaveUs 프로젝트에 기여하고 싶으신가요? 언제든 환영합니다!

1. 이 프로젝트를 **Fork** 하세요.
2. 새로운 **Feature Branch**를 생성하세요 (`git checkout -b feature/NewFeature`).
3. 변경 사항을 **Commit** 하세요 (`git commit -m 'Add some NewFeature'`).
4. 브랜치에 **Push** 하세요 (`git push origin feature/NewFeature`).
5. **Pull Request**를 보내주세요.

## 📝 라이선스 (License)
This project is licensed under the MIT License - details see the [LICENSE](LICENSE) file.

## 👥 저자 (Authors)
- **Team SaveUs** - *Initial work*
