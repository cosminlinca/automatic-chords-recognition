package com.ubb.acousticrecognizer.ui.chords

import android.app.Activity
import android.content.res.Resources
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.media.MediaPlayer
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.DisplayMetrics
import android.view.Gravity
import android.widget.Button
import android.widget.ImageView
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.external.chorddroid.helper.DrawHelper
import com.ubb.acousticrecognizer.utils.Constants
import kotlinx.android.synthetic.main.activity_guitar_music_player.*
import java.io.File

class PopActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pop)

        // Get extras
        val chordName = intent.getStringExtra("chordName")

        // Display popup window
        val dispayMetrics = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(dispayMetrics)

        val width = dispayMetrics.widthPixels
        val height = dispayMetrics.heightPixels

        window.setLayout(((width*.8).toInt()), ((height*.5).toInt()))
        val params = window.attributes
        params.gravity = Gravity.CENTER
        params.x = 0
        params.y = -20

        window.attributes = params

        // Set drawable
        val drawable = drawChordHelper(chordName!!)
        val imageView = findViewById<ImageView>(R.id.chordImagePopId)
        imageView.setImageDrawable(drawable)

        // Set media player
        val chordAudioFile = File(Constants.rootDirectoryPath + "/chords/" + chordName + ".wav")
        val uriAudioFile = Uri.fromFile(chordAudioFile)
        val mediaPlayer = MediaPlayer.create(applicationContext, uriAudioFile)

        // Set start button
        val startBtn = findViewById<Button>(R.id.startBtnPop)
        startBtn.setOnClickListener {
            mediaPlayer.start()
        }
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
}
