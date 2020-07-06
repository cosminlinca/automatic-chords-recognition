package com.ubb.acousticrecognizer.ui

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.ViewTreeObserver
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import com.github.derlio.waveform.SimpleWaveformView
import com.github.derlio.waveform.soundfile.SoundFile
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.utils.Constants
import kotlinx.android.synthetic.main.activity_recorder.*
import java.io.File


// POC
class TestRecorderActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_recorder)

//        requirePermissions()
//
//        val filePath: String =
//            Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM).toString() + "/recorded_audio.wav"
//
//        var testFolder = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM),
//            "TESTAUDIO.txt")
//
//        if(!testFolder.exists()) {
//            var created= testFolder.createNewFile()
//            println("Folder created: " + created)
//        }
//
//        var startBtn: ImageButton = findViewById(R.id.record);
//        startBtn.setOnClickListener { event ->
//            run {
//                AndroidAudioRecorder.with(this)
//                    // Required
//                    .setFilePath(filePath)
//                    .setRequestCode(Constants.RECORDING_REQUEST_CODE)
//
//                    // Optional
//                    .setSource(AudioSource.MIC)
//                    .setChannel(AudioChannel.STEREO)
//                    .setSampleRate(AudioSampleRate.HZ_48000)
//                    .setAutoStart(true)
//                    .setKeepDisplayOn(true)
//
//                    // Start recording
//                    .record();
//            }
//        }

        var rootFile: File = File(Constants.rootDirectoryPath)
        var testAudioFile = rootFile.listFiles()!![0]

        val soundFile =
            SoundFile.create(testAudioFile.getPath(), object : SoundFile.ProgressListener {
                var lastProgress = 0
                override fun reportProgress(fractionComplete: Double): Boolean {
                    val progress = (fractionComplete * 100).toInt()
                    if (lastProgress == progress) {
                        return true
                    }

                    lastProgress = progress
                    Log.i("RECORD ACTIVITY", "LOAD FILE PROGRESS:$progress")
                    return true
                }
            })

        var vto = window.decorView.viewTreeObserver
        if (vto.isAlive) {
            vto.addOnGlobalLayoutListener {
                waveform.setAudioFile(soundFile)
                waveform.invalidate()
                waveform.setPlaybackPosition(600)
            }
        }
    }


    private fun requirePermissions(): Boolean { // Setup
        val requestCode = 101
        val permissionsArray = arrayOf(
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.RECORD_AUDIO
        )
        // Get permissions status
        val writePermission = ContextCompat.checkSelfPermission(
            applicationContext,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )
        val readPermission = ActivityCompat.checkSelfPermission(
            applicationContext,
            Manifest.permission.READ_EXTERNAL_STORAGE
        )
        val recordAudioPermission = ActivityCompat.checkSelfPermission(
            applicationContext,
            Manifest.permission.RECORD_AUDIO
        )

        return if (writePermission != PackageManager.PERMISSION_GRANTED ||
            readPermission != PackageManager.PERMISSION_GRANTED ||
            recordAudioPermission != PackageManager.PERMISSION_GRANTED
        ) { // Grant user permissions (read & write)
            ActivityCompat.requestPermissions(this, permissionsArray, requestCode)
            false
        } else true
    }
}
