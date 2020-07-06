package com.ubb.acousticrecognizer.ui

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider.NewInstanceFactory
import com.ubb.acousticrecognizer.ui.home.HomeViewModel
import com.ubb.acousticrecognizer.ui.music_player.GuitarMusicPlayerViewModel

class MyViewModelFactory(private val context: Context?, vararg params: Any) :
    NewInstanceFactory() {
    private val mParams: Array<Any> = arrayOf(params)
    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        return if (modelClass == HomeViewModel::class.java) {
            HomeViewModel(context!!) as T
        }
        else if (modelClass == GuitarMusicPlayerViewModel::class.java) {
            GuitarMusicPlayerViewModel(context!!) as T
        }
        else  { super.create(modelClass) }
    }
}