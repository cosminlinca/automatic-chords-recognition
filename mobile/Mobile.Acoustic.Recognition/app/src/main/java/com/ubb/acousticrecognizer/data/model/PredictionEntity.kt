package com.ubb.acousticrecognizer.data.model

import java.io.Serializable

data class PredictionEntity(
    public var Chord: String,
    public var Probability: String
):Serializable