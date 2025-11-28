package com.example.Ex02.dto;

import lombok.Data;
import java.util.List;

@Data
public class ExerciseRecommendResponseDto {

    private int user_id;
    private String predicted_category;
    private Routine routine;

    @Data
    public static class Routine {
        private String 준비운동;
        private List<String> 본운동;
        private String 정리운동;
    }
}
