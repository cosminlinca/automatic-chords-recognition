package com.ubb.acousticrecognizer.config

import com.google.gson.GsonBuilder
import com.ubb.acousticrecognizer.utils.Constants
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit


class RetrofitFactory private constructor() {
    companion object {
        val wifi_retrofit_basic: Retrofit
            get() {
                val gsonBuilder = GsonBuilder()
                gsonBuilder.registerTypeAdapterFactory(ItemTypeAdapterFactory())

                val okHttpClient = OkHttpClient().newBuilder()
                    .connectTimeout(5, TimeUnit.MINUTES)
                    .readTimeout(5, TimeUnit.MINUTES)
                    .writeTimeout(5, TimeUnit.MINUTES)
                    .build()

                val builder: Retrofit.Builder = Retrofit.Builder()
                    .baseUrl(Constants.WIFI_API_BASE_URL)
                    .client(okHttpClient)
                    .addConverterFactory(GsonConverterFactory.create(gsonBuilder.create()))
                    .addCallAdapterFactory(RxJava2CallAdapterFactory.create())

                return builder.build()
            }

        val cable_retrofit_basic: Retrofit
            get() {
                val gsonBuilder = GsonBuilder()
                gsonBuilder.registerTypeAdapterFactory(ItemTypeAdapterFactory())

                val okHttpClient = OkHttpClient().newBuilder()
                    .connectTimeout(5, TimeUnit.MINUTES)
                    .readTimeout(5, TimeUnit.MINUTES)
                    .writeTimeout(5, TimeUnit.MINUTES)
                    .build()

                val builder: Retrofit.Builder = Retrofit.Builder()
                    .baseUrl(Constants.CABLE_API_BASE_URL)
                    .client(okHttpClient)
                    .addConverterFactory(GsonConverterFactory.create(gsonBuilder.create()))
                    .addCallAdapterFactory(RxJava2CallAdapterFactory.create())

                return builder.build()
            }

        val hotspot_retrofit_basic: Retrofit
            get() {
                val gsonBuilder = GsonBuilder()
                gsonBuilder.registerTypeAdapterFactory(ItemTypeAdapterFactory())

                val okHttpClient = OkHttpClient().newBuilder()
                    .connectTimeout(5, TimeUnit.MINUTES)
                    .readTimeout(5, TimeUnit.MINUTES)
                    .writeTimeout(5, TimeUnit.MINUTES)
                    .build()

                val builder: Retrofit.Builder = Retrofit.Builder()
                    .baseUrl(Constants.HOTSPOT_API_BASE_URL)
                    .client(okHttpClient)
                    .addConverterFactory(GsonConverterFactory.create(gsonBuilder.create()))
                    .addCallAdapterFactory(RxJava2CallAdapterFactory.create())

                return builder.build()
            }
    }
}