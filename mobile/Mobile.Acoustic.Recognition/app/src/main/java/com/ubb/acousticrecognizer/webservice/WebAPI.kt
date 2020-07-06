package com.ubb.acousticrecognizer.webservice

import com.ubb.acousticrecognizer.data.model.OnsetEntity
import io.reactivex.Single
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.HeaderMap
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface WebAPI {

    @Multipart
    @POST("/ComputeChordsPrediction")
    fun computeChordsPrediction(@HeaderMap headers: Map<String, String> ,
                                @Part audio_file: MultipartBody.Part):
            Single<Response<ArrayList<OnsetEntity>>>

    @POST("/Ping")
    fun ping(): Single<String>
}