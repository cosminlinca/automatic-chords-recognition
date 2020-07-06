package com.ubb.acousticrecognizer.data.model

import com.squareup.moshi.JsonClass
import java.io.Serializable

@JsonClass(generateAdapter = true)
data class OnsetEntity(
    public var Id: Int,
    public var Pitch_start: Double,
    public var Duration: Double,
    public var Predictions: List<PredictionEntity>
): Serializable