from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np


test = FastAPI()

MODEL_PATH = "diabetes_risk_model_v5_xgb.pkl"
try:
    # diabetes_risk_model_v5_xgb.pkl 파일이 현재 실행 경로에 있어야 합니다.
    diet_model = joblib.load(MODEL_PATH)
    print(f"✅ 당뇨 모델 로드 성공: {MODEL_PATH}")
except Exception as e:
    # 모델 파일이 없는 경우, 이 API는 작동하지 않습니다.
    print(f"❌ 당뇨 모델 로드 실패: {e}")
    diet_model = None


class UserDietInfo(BaseModel):
    user_id: int
    age: int
    sex: int          # 1:남, 2:여 (DB값 그대로)
    height: float
    weight: float
    total_kcal: float
    total_carbs: float
    total_fat: float
    total_protein: float
    total_sodium: float
    total_sugar: float



# CORS 설정 (자바 서버에서 오는 요청 허용)
test.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@test.post("/api/calculate-score")
def calculate_diet_score(users: List[UserDietInfo]):
    """
    사용자들의 일주일간의 식단 영양 정보(UserDietInfo 리스트)를 받아
    당뇨 위험도를 예측하고 점수를 계산하여 반환합니다.
    """
    if diet_model is None:
        raise HTTPException(status_code=503, detail="Diabetes risk model not loaded")

    if not users:
        return []

    results = []

    for u in users:
        try:
            # 1. 전처리 (모델 학습 때와 동일한 공식 적용)
            # BMI 계산
            bmi = u.weight / ((u.height / 100) ** 2)

            # 성별 권장 칼로리 (남:30, 여:25) * 표준체중
            rec_calorie = (u.height - 100) * 0.9 * (30 if u.sex == 1 else 25)

            # 비율 계산 (0 나누기 방어 로직)
            pct_calorie = u.total_kcal / rec_calorie if rec_calorie > 0 else 0
            pct_protein = u.total_protein / u.weight if u.weight > 0 else 0
            pct_sodium = u.total_sodium / 2000.0 # 나트륨 권장량 2000mg 대비 비율

            ratio_fat = (u.total_fat * 9) / u.total_kcal if u.total_kcal > 0 else 0    # 지방 에너지 비율
            ratio_cho = (u.total_carbs * 4) / u.total_kcal if u.total_kcal > 0 else 0  # 탄수화물 에너지 비율
            ratio_sugar_to_cho = u.total_sugar / u.total_carbs if u.total_carbs > 0 else 0 # 탄수화물 중 당류 비율

            # 2. 로그 변환 및 DataFrame 생성
            # 모델의 Feature 순서 및 이름 일치 중요
            input_df = pd.DataFrame([{
                'AGE': u.age,
                'BMI': bmi,
                'SEX': u.sex,
                'LOG_PCT_CALORIE': np.log1p(pct_calorie),
                'PCT_PROTEIN': pct_protein,
                'LOG_PCT_SODIUM': np.log1p(pct_sodium),
                'RATIO_SUGAR_TO_CHO': ratio_sugar_to_cho,
                'LOG_RATIO_FAT': np.log1p(ratio_fat),
                'RATIO_CHO': ratio_cho
            }])

            features = ['AGE', 'BMI', 'SEX', 'LOG_PCT_CALORIE', 'PCT_PROTEIN',
                        'LOG_PCT_SODIUM', 'RATIO_SUGAR_TO_CHO', 'LOG_RATIO_FAT', 'RATIO_CHO']

            # 3. 예측 (실제 위험도)
            # 당뇨 발병 확률 (0~1 사이 값)
            real_risk = diet_model.predict_proba(input_df[features])[:, 1][0]

            # 4. 아바타 비교 (상대평가 점수)
            # 모델이 아바타(평균적인 위험 식습관)의 데이터로 계산한 위험도
            avatar_df = input_df.copy()
            avatar_df['AGE'] = 52
            avatar_df['BMI'] = 26.0
            avatar_df['SEX'] = 1
            avatar_risk = diet_model.predict_proba(avatar_df[features])[:, 1][0]

            # 아바타 위험도(avatar_risk)를 기준으로 점수를 산정
            if avatar_risk <= 0.20:
                score = 100
            elif avatar_risk <= 0.53:
                # 0.20 ~ 0.53 구간을 80 ~ 100점으로 선형 보간
                score = 80 + ((0.53 - avatar_risk) / (0.53 - 0.20) * 20)
            elif avatar_risk <= 0.68:
                # 0.53 ~ 0.68 구간을 40 ~ 80점으로 선형 보간
                score = 40 + ((0.68 - avatar_risk) / (0.68 - 0.53) * 40)
            else:
                # 0.68 ~ 0.91 구간을 0 ~ 40점으로 선형 보간 (0.91 초과는 0점)
                score = ((0.91 - avatar_risk) / (0.91 - 0.68) * 40)

            # 점수를 0~100 사이로 클립하고 정수로 변환
            final_score = int(np.clip(score, 0, 100))
            # 실제 위험도를 백분율로 변환
            similarity = int(real_risk * 100)

            # 결과 리스트에 추가
            results.append({
                "user_id": u.user_id,
                "score": final_score,
                "similarity": similarity,
                "risk_level": "DANGER" if final_score < 50 else ("WARNING" if final_score < 80 else "GOOD")
            })

        except Exception as e:
            print(f"❌ User {u.user_id} 처리 중 오류 발생: {e}")
            # 특정 사용자 처리 중 오류가 발생하더라도 나머지 사용자는 계속 처리
            continue

    return results
# ================================================================


if __name__ == "__main__":
    import uvicorn

    # uvicorn 서버 실행
    uvicorn.run(test, host="0.0.0.0", port=8000)