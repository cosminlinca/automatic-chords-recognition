package com.ubb.acousticrecognizer.ui.recording

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProviders
import cafe.adriel.androidaudiorecorder.AndroidAudioRecorder
import cafe.adriel.androidaudiorecorder.model.AudioChannel
import cafe.adriel.androidaudiorecorder.model.AudioSampleRate
import cafe.adriel.androidaudiorecorder.model.AudioSource
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.utils.Constants
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter


class RecordingFragment : Fragment() {

    private lateinit var recordingViewModel: RecordingViewModel

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        recordingViewModel =
                ViewModelProviders.of(this).get(RecordingViewModel::class.java)
        val root = inflater.inflate(R.layout.fragment_recording, container, false)
        val primaryActivity = activity

        val startBtn: ImageButton = root.findViewById(R.id.recordBtn);
        startBtn.setOnClickListener { event ->
            val ldt: LocalDateTime = LocalDateTime.now()
            val formatter: DateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss")

            val formattedDateTime: String = ldt.format(formatter)

            val filePath: String =
                Constants.rootDirectoryPath + "/recorded_audio_" + formattedDateTime + ".wav"
                    .replace(":", "_")

            run {
                AndroidAudioRecorder.with(primaryActivity)
                    // Required
                    .setFilePath(filePath)
                    .setColor(R.color.waveform_unselected)
                    .setRequestCode(Constants.RECORDING_REQUEST_CODE)
                    // Optional
                    .setSource(AudioSource.MIC)
                    .setChannel(AudioChannel.STEREO)
                    .setSampleRate(AudioSampleRate.HZ_48000)
                    .setAutoStart(true)
                    .setKeepDisplayOn(true)

                    // Start recording
                    .record()
            }
        }

        return root
    }
}
