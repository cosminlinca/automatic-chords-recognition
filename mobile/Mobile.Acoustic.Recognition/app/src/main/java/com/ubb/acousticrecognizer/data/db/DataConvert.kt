package com.ubb.acousticrecognizer.data.db

import androidx.room.TypeConverter
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.ubb.acousticrecognizer.data.model.OnsetEntity
import com.ubb.acousticrecognizer.data.model.PredictionEntity

class DataConvert {
    @TypeConverter
    fun fromOnsetsList(onsets: List<OnsetEntity?>?): String? {
        if (onsets == null) {
            return null
        }
        val gson = Gson()
        val type = object :
            TypeToken<List<OnsetEntity?>?>() {}.type
        return gson.toJson(onsets, type)
    }

    @TypeConverter
    fun toOnsetsList(onsets: String?): List<OnsetEntity>? {
        if (onsets == null) {
            return null
        }
        val gson = Gson()
        val type = object :
            TypeToken<List<OnsetEntity?>?>() {}.type
        return gson.fromJson<List<OnsetEntity>>(onsets, type)
    }

    @TypeConverter
    fun fromPredictionsList(predictionEntities: List<PredictionEntity?>?): String? {
        if (predictionEntities == null) {
            return null
        }
        val gson = Gson()
        val type = object :
            TypeToken<List<PredictionEntity?>?>() {}.type
        return gson.toJson(predictionEntities, type)
    }

    @TypeConverter
    fun toPredictionsList(predictions: String?): List<PredictionEntity>? {
        if (predictions == null) {
            return null
        }
        val gson = Gson()
        val type = object :
            TypeToken<List<PredictionEntity?>?>() {}.type
        return gson.fromJson<List<PredictionEntity>>(predictions, type)
    }
}