package com.ubb.acousticrecognizer.utils

import android.os.Environment

class Constants {
    companion object {
        const val RECORDING_REQUEST_CODE = 0
        var rootDirectoryPath = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM)
            .toString() + "/AcousticRecognizer"
        const val WIFI_API_BASE_URL = "http://192.168.100.5:5000"
        const val CABLE_API_BASE_URL = "http://192.168.100.10:5000"
        const val HOTSPOT_API_BASE_URL = "http://192.168.100.5:5000"
    }
}