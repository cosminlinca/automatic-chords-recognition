package com.ubb.acousticrecognizer

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.MenuItem
import android.view.View
import android.widget.ImageView
import android.widget.PopupMenu
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.android.material.snackbar.Snackbar
import com.ubb.acousticrecognizer.ui.home.HomeFragment
import com.ubb.acousticrecognizer.utils.Constants
import java.io.File

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val navView: BottomNavigationView = findViewById(R.id.nav_view)

        val navController = findNavController(R.id.nav_host_fragment)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        val appBarConfiguration = AppBarConfiguration(setOf(
                R.id.navigation_home, R.id.navigation_recording, R.id.navigation_chords))
        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)

        requirePermissions()
        createFolderStructure()
        ping()
    }

    private fun ping() {

    }

    private fun createFolderStructure() {
        val rootDirectory = File(
            Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM),
            "AcousticRecognizer")

        if(!rootDirectory.exists()) {
            rootDirectory.mkdir()
        }
    }

    private fun requirePermissions(): Boolean {
        // Setup
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

    override fun onActivityResult(
        requestCode: Int,
        resultCode: Int,
        data: Intent?
    ) {
        super.onActivityResult(requestCode, resultCode, data)
        Log.i("ActivityResult", resultCode.toString())
        if (requestCode == Constants.RECORDING_REQUEST_CODE) {
            val parentLayout: View = findViewById(android.R.id.content)
            if (resultCode == Activity.RESULT_OK) {
                // Great! User has recorded and saved the audio file
                //Snackbar.make(parentLayout, "Recording file saved!", Snackbar.LENGTH_SHORT).show()
                Toast.makeText(applicationContext, "Recording file saved!",
                    Toast.LENGTH_SHORT).show()
            } else if (resultCode == Activity.RESULT_CANCELED) {
                // Oops! User has canceled the recording
                //Snackbar.make(parentLayout, "Recording canceled.", Snackbar.LENGTH_SHORT).show()
                Toast.makeText(applicationContext, "Recording canceled.",
                    Toast.LENGTH_SHORT).show()
            }
        }
    }

}
