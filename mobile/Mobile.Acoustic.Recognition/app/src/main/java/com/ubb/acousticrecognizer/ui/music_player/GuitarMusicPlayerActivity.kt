package com.ubb.acousticrecognizer.ui.music_player

import android.annotation.SuppressLint
import android.app.AlertDialog
import android.content.res.Resources
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.media.MediaPlayer
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Message
import android.util.Log
import android.widget.ImageView
import android.widget.SeekBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.github.derlio.waveform.soundfile.SoundFile
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.data.db.AppDatabase
import com.ubb.acousticrecognizer.data.model.LocalDetectionEntity
import com.ubb.acousticrecognizer.data.model.PredictionOperation
import com.ubb.acousticrecognizer.external.chorddroid.helper.DrawHelper
import com.ubb.acousticrecognizer.ui.MyViewModelFactory
import kotlinx.android.synthetic.main.activity_guitar_music_player.*
import java.io.File
import java.lang.Thread.sleep


class GuitarMusicPlayerActivity : AppCompatActivity() {

    private var mediaPlayer: MediaPlayer = MediaPlayer()
    private lateinit var audioFile: File
    private lateinit var uriAudioFile: Uri
    private lateinit var guitarMusicPlayerViewModel: GuitarMusicPlayerViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_guitar_music_player)

        println("Init GuitarMusicPlayerActivity")
        guitarMusicPlayerViewModel =
            ViewModelProviders.of(this, MyViewModelFactory(this)).
                get(GuitarMusicPlayerViewModel::class.java)

        // Get extras
        val audioFileName: String = intent.getStringExtra("audioFileName")!!
        val audioFilePath: String = intent.getStringExtra("audioFilePath")!!
        guitarMusicPlayerViewModel.setAudioFileName(audioFileName)
        guitarMusicPlayerViewModel.setAudioFilePath(audioFilePath)

        // Set title for current recording
        titleTextView.text = audioFileName

        guitarMusicPlayerViewModel.getOnsets().observe(this, Observer { onsets ->
            println("ONSET SIZE " + onsets.size)
            // Define test uri file
            audioFile = File(guitarMusicPlayerViewModel.getAudioFilePath())
            uriAudioFile = Uri.fromFile(audioFile)

            defineMusicPlayer()
            definePlayMusicBtn()
            defineWaveform()
            defineHandlerForMusicPlayer()
        })

        guitarMusicPlayerViewModel.getPredictionOperation().observe(this, Observer { pred ->
            predictionImgBehavior(pred)
        })

        guitarMusicPlayerViewModel.initialize()
    }

    private fun savePredictionImgBehavior() {
        val predictionImg = findViewById<ImageView>(R.id.saveIcon)

        predictionImg.setImageDrawable(resources.getDrawable
            (R.drawable.ic_save_white_24px))

        predictionImg.setOnClickListener {
            // Save current onset prediction to local db
            val localDB = AppDatabase.getInstance(applicationContext)
            AlertDialog.Builder(this)
                .setTitle("Save")
                .setMessage("Do you want to save locally the result obtained after processing?")
                .setPositiveButton(
                    "Yes") { _, _ ->
                    localDB.detectionEntityDao().insert(LocalDetectionEntity(
                        guitarMusicPlayerViewModel.getAudioFilePath(),
                        guitarMusicPlayerViewModel.getAudioFileName(),
                        guitarMusicPlayerViewModel.getOnsets().value!!))

                    val localDetectionEntity = localDB.detectionEntityDao()
                        .getByAbsolutePath(guitarMusicPlayerViewModel.getAudioFilePath())
                    println("Saved onsets size " + localDetectionEntity!!.Onsets.size.toString())

                    Toast.makeText(applicationContext, "Successfully saved!",
                        Toast.LENGTH_SHORT).show()

                    deletePredictionImgBehavior()
                }
                .setNegativeButton("No", null)
                .show()
        }
    }

    private fun deletePredictionImgBehavior() {
        val predictionImg = findViewById<ImageView>(R.id.saveIcon)

        predictionImg.setImageDrawable(resources.getDrawable
            (R.drawable.ic_delete_forever_white_24px))

        predictionImg.setOnClickListener {
            // Delete
            val localDB = AppDatabase.getInstance(applicationContext)
            AlertDialog.Builder(this)
                .setTitle("Delete")
                .setMessage("Do you want to delete prediction locally stored?")
                .setPositiveButton(
                    "Yes"
                ) { _, _ ->

                    val localDB = AppDatabase.getInstance(applicationContext)
                    val localDetectionEntity = localDB.detectionEntityDao()
                        .getByAbsolutePath(guitarMusicPlayerViewModel.getAudioFilePath())

                    localDB.detectionEntityDao().delete(localDetectionEntity!!)

                    Toast.makeText(
                        applicationContext, "Successfully deleted!",
                        Toast.LENGTH_SHORT
                    ).show()

                    savePredictionImgBehavior()
                }
                .setNegativeButton("No", null)
                .show()
        }
    }

    private fun predictionImgBehavior(predictionOp: PredictionOperation) {
        if(predictionOp == PredictionOperation.ADD) {
            savePredictionImgBehavior()
        }
        else if(predictionOp == PredictionOperation.DELETE) {
            deletePredictionImgBehavior()
        }
    }

    private val handler = @SuppressLint("HandlerLeak") object : Handler() {
        override fun handleMessage(msg: Message?) {
            val currentPosition = msg!!.what

            // Update position bar
            positionBar.progress = currentPosition

            // Update waveform
            waveform.setPlaybackPosition(currentPosition)

            // Update label for elapsed time
            val elapsedTime: String = createTimeLabel(currentPosition)
            timerTextView.text = elapsedTime

            // Update chord image
            val onsets = guitarMusicPlayerViewModel.getOnsets().value;
            var auxPoz = 0
            for(i in guitarMusicPlayerViewModel.getOnsetsLastPoz() until onsets!!.size)  {
                val onsetEntity = onsets[i]
                val startMili = onsetEntity.Pitch_start.toInt() * 1000
                val stopMili = (onsetEntity.Pitch_start + onsetEntity.Duration).toInt() * 1000
                if(currentPosition in startMili..stopMili) {
                    var chordStringPrediction0 = onsetEntity.Predictions[0].Chord
                    var chordStringPrediction1 = onsetEntity.Predictions[1].Chord
                    var chordStringPrediction2 = onsetEntity.Predictions[2].Chord
                    var doubleProbability0 = ""
                    var doubleProbability1 = ""
                    var doubleProbability2 = ""
                    try {
                        doubleProbability0   = (onsetEntity.Predictions[0].Probability.toDouble() * 100)
                            .toString().subSequence(0, 5).toString() + "%"
                        doubleProbability1 = (onsetEntity.Predictions[1].Probability.toDouble() * 100)
                            .toString().subSequence(0, 5).toString() + "%"
                        doubleProbability2 = (onsetEntity.Predictions[2].Probability.toDouble() * 100)
                            .toString().subSequence(0, 5).toString() + "%"
                    }catch (ex: Exception) {
                        doubleProbability0   = (onsetEntity.Predictions[0].Probability.toDouble() * 100)
                            .toString().subSequence(0, 5).toString() + "%"
                        doubleProbability1 = (onsetEntity.Predictions[1].Probability.toDouble() * 100)
                            .toString().subSequence(0, 3).toString() + "%"
                        doubleProbability2 = (onsetEntity.Predictions[2].Probability.toDouble() * 100)
                            .toString().subSequence(0, 3).toString() + "%"
                    }


                    if(!chordStringPrediction0.contains("n")) {
                        chordStringPrediction0 = capitalize(chordStringPrediction0).toString()
                        auxPoz = i
                        // println("Chord recog: $chordString")

                        val chord = drawChordHelper(chordStringPrediction0)
                        chordImage.setImageDrawable(chord)
                        probabilityTextView.text = doubleProbability0
                    }
                    else {
                        chordImage.setImageDrawable(ContextCompat.getDrawable(applicationContext, R.drawable.ic_n))
                        probabilityTextView.text = doubleProbability0
                    }

                    if(!chordStringPrediction1.contains("n")) {
                        chordStringPrediction1 = capitalize(chordStringPrediction1).toString()
                        auxPoz = i
                        // println("Chord recog: $chordString")

                        val chord = drawChordHelper(chordStringPrediction1)
                        chordImageLeft.setImageDrawable(chord)
                        probabilityTextViewLeft.text = doubleProbability1
                    }
                    else {
                        chordImageLeft.setImageDrawable(ContextCompat.getDrawable(applicationContext, R.drawable.ic_n))
                        probabilityTextViewLeft.text = doubleProbability1
                    }

                    if(!chordStringPrediction2.contains("n")) {
                        chordStringPrediction2 = capitalize(chordStringPrediction2).toString()
                        auxPoz = i
                        // println("Chord recog: $chordString")

                        val chord = drawChordHelper(chordStringPrediction2)
                        chordImageRight.setImageDrawable(chord)
                        probabilityTextViewRigth.text = doubleProbability2
                    }
                    else {
                        chordImageRight.setImageDrawable(ContextCompat.getDrawable(applicationContext, R.drawable.ic_n))
                        probabilityTextViewRigth.text = doubleProbability2
                    }
                }
            }
            guitarMusicPlayerViewModel.setOnsetsLastPoz(auxPoz)
        }
    }

    private fun createTimeLabel(time: Int): String {
        var timeLabel = ""
        val min: Int  = time / 1000 / 60
        val sec: Int = time / 1000 % 60

        timeLabel = "$min:"
        if(sec < 10) timeLabel += "0"
        timeLabel += sec

        return timeLabel
    }

    private fun drawChordHelper(chordValue: String): BitmapDrawable {
        val resources: Resources = resources
        val width = 300
        val height = 300
        val chordName = chordValue
        val position = 0 // fret position index (0 to 8)
        val transpose = 0 // transpose distance (-12 to 12)

        // Draw chord
        val chord = DrawHelper.getBitmapDrawable(
            resources, width, height, chordName, position, transpose
        )

        return chord
    }

    private fun defineHandlerForMusicPlayer() {
        // Handler thread
        Thread(Runnable {
            while(true) {
                val msg = Message()
                msg.what = mediaPlayer.currentPosition
                handler.sendMessage(msg)
                sleep(10)
            }
        }).start()
    }

    private fun defineWaveform() {
        // Sound file for waveform
        val soundFile =
            SoundFile.create(audioFile.getPath(), object : SoundFile.ProgressListener {
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

        waveform.setAudioFile(soundFile)
        waveform.invalidate()
    }

    private fun definePlayMusicBtn() {
        // Start btn event
        startBtn.setOnClickListener {
            if(!mediaPlayer.isPlaying) {
                mediaPlayer.start()
                startBtn.text = "PAUSE"
                val pauseImage: Drawable = resources.getDrawable(R.drawable.ic_pause_24px)
                startBtn.setCompoundDrawablesWithIntrinsicBounds(pauseImage, null,
                    null, null)
            }
            else {
                mediaPlayer.pause()
                startBtn.text = "START"
                val pauseImage: Drawable = resources.getDrawable(R.drawable.ic_play_arrow_24px)
                startBtn.setCompoundDrawablesWithIntrinsicBounds(pauseImage, null,
                    null, null)
            }
        }
    }

    private fun defineMusicPlayer() {
        // Define Media Player
        mediaPlayer = MediaPlayer.create(applicationContext, uriAudioFile)
        mediaPlayer.isLooping = true
        mediaPlayer.seekTo(0)
        mediaPlayer.setVolume(1f, 1f)
        val totalTime = mediaPlayer.duration

        positionBar.max = totalTime
        positionBar.setOnSeekBarChangeListener(object :
            SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                if(fromUser) {
                    mediaPlayer.seekTo(progress)
                    positionBar.progress = progress
                }
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
            }
        })
    }

    fun capitalize(str: String?): String? {
        return if (str == null || str.isEmpty()) {
            str
        } else str.substring(0, 1).toUpperCase() + str.substring(1)
    }

    override fun onDestroy() {
        super.onDestroy()

        // Stop media player
        if(mediaPlayer.isPlaying)
            mediaPlayer.stop()
    }

    override fun onPause() {
        super.onPause()

        // Stop media player
        if(mediaPlayer.isPlaying)
            mediaPlayer.stop()
    }
}
