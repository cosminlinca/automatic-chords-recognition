package com.ubb.acousticrecognizer.data.repository

import com.ubb.acousticrecognizer.config.RetrofitFactory
import com.ubb.acousticrecognizer.data.model.OnsetEntity
import com.ubb.acousticrecognizer.webservice.WebAPI
import io.reactivex.Single
import okhttp3.MediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import java.io.File

class WebRepository {
    private val webApi: WebAPI = RetrofitFactory.cable_retrofit_basic.create(WebAPI::class.java)

    fun computeChordsPrediction(audioFile: File): Single<Response<ArrayList<OnsetEntity>>> {
        val headers = HashMap<String, String>()

        var requestFile: RequestBody = RequestBody
            .create(MediaType.parse("multipart/form-data"), audioFile)
        var bodyType = MultipartBody.Part
            .createFormData("audio_file", audioFile.name, requestFile)

        return webApi.computeChordsPrediction(headers, bodyType)
    }
}