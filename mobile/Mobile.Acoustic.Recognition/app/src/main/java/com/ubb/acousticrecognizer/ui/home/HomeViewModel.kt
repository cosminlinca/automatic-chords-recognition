package com.ubb.acousticrecognizer.ui.home

import android.content.Context
import android.util.Log
import android.widget.Toast
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.ubb.acousticrecognizer.data.model.OnsetEntity
import com.ubb.acousticrecognizer.data.repository.WebRepository
import com.ubb.acousticrecognizer.utils.Constants
import io.reactivex.SingleObserver
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.disposables.Disposable
import io.reactivex.schedulers.Schedulers
import retrofit2.Response
import java.io.File

class HomeViewModel(context: Context) : ViewModel() {
    private var context: Context = context
    private var webRepository: WebRepository = WebRepository()
}