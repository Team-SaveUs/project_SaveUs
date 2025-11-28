from typing import Optional, List

from repositories import FoodNutritionRepository
from api import FoodNutritionClient, ProductInfoClient
from utils.barcode_detector import BarcodeDetector
from ml.yolo_inference import detect_objects
from models.food_nutrition import Food
from utils.mapper import label_map

import asyncio

food_nutrition_repository = FoodNutritionRepository()

barcode_detector = BarcodeDetector()
product_info_client = ProductInfoClient()
food_nutrition_client = FoodNutritionClient()

async def detect_food(imageBytes) -> Optional[List[Food]]:
    detected_barcode = barcode_detector.detect_codes_from_file(imageBytes)

    if not detected_barcode:
        detected_foods = await detect_objects(imageBytes)
        items = [label_map.get(res) for res in detected_foods]
        nutrition_items = [Food(**food_info) for item in items if (food_info := food_nutrition_repository.get_food_nutrition_by_name(item))]

        return nutrition_items

    barcode = detected_barcode[0]

    barcode_fetch_result = await product_info_client.get_prd_report_no(barcode)

    if barcode_fetch_result is None:
        return

    food_name, prd_no = barcode_fetch_result
    food_name = food_name.replace(" ", "")

    if (nutrition_item := food_nutrition_repository.get_food_nutrition_by_name(food_name)) is None:
        nutrition_item = await food_nutrition_client.get_food_data(
            query_params={
                "ITEM_REPORT_NO": prd_no,
            }
        )
        nutrition_item["food_name"] = food_name.replace(" ", "")
        food_nutrition_repository.insert_food_nutrition(nutrition_item)

    return [nutrition_item]
