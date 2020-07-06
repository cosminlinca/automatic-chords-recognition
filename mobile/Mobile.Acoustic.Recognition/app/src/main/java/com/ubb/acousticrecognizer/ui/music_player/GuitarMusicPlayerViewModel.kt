package com.ubb.acousticrecognizer.ui.music_player

import android.content.Context
import android.util.Log
import android.widget.Toast
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.ubb.acousticrecognizer.data.db.AppDatabase
import com.ubb.acousticrecognizer.data.model.OnsetEntity
import com.ubb.acousticrecognizer.data.model.PredictionOperation
import com.ubb.acousticrecognizer.data.repository.WebRepository
import com.ubb.acousticrecognizer.ui.intermediate.ProgressDialogUtil
import io.reactivex.SingleObserver
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.disposables.Disposable
import io.reactivex.schedulers.Schedulers
import retrofit2.Response
import java.io.File

class GuitarMusicPlayerViewModel(private var context: Context) : ViewModel() {
    private var webRepository: WebRepository = WebRepository()
    private var _audioFileName: String = ""
    private var _audioFilePath: String = ""
    private var _onsetsLastPoz: Int = 0

    private var _onsets: MutableLiveData<List<OnsetEntity>> = MutableLiveData()
    private var _predictionOperation: MutableLiveData<PredictionOperation> = MutableLiveData()

    fun initialize() {
         onsetLoading()
    }

    fun getOnsets(): LiveData<List<OnsetEntity>> {
        return _onsets
    }

    fun getPredictionOperation(): LiveData<PredictionOperation> {
        return _predictionOperation
    }

    fun getOnsetsLastPoz(): Int {
        return _onsetsLastPoz
    }

    fun setOnsetsLastPoz(lastPoz: Int) {
        _onsetsLastPoz = lastPoz
    }

    fun setAudioFileName(name: String) {
        _audioFileName = name
    }

    fun setAudioFilePath(name: String) {
        _audioFilePath = name
    }

    fun getAudioFilePath(): String {
        return _audioFilePath
    }

    fun getAudioFileName(): String {
        return _audioFileName
    }

    private fun onsetLoading() {
        val localDB = AppDatabase.getInstance(context)
        val localDetectionEntity = localDB.detectionEntityDao()
            .getByAbsolutePath(_audioFilePath)

        if(localDetectionEntity != null) {
            println("GET locally onsets size " + localDetectionEntity.Onsets.size.toString())
            _onsets.postValue(localDetectionEntity.Onsets as ArrayList)
            _predictionOperation.postValue(PredictionOperation.DELETE)
        }
        else {
            val audioFile = File(_audioFilePath)
            val dialog = ProgressDialogUtil.setProgressDialog(context, "Please wait...")

            // Response
            val onsetResponse = object : SingleObserver<Response<ArrayList<OnsetEntity>>> {
                override fun onSuccess(t: Response<ArrayList<OnsetEntity>>) {
                    dialog.dismiss()
                    if (t.isSuccessful) {
                        // Success
                        _onsets.postValue(t.body())
                        _predictionOperation.postValue(PredictionOperation.ADD)
                    } else {
                        Log.e("onsetError", "!isSuccessful")
                    }
                }

                override fun onSubscribe(d: Disposable) {
                    dialog.show()
                }

                override fun onError(e: Throwable) {
                    dialog.dismiss()
                    Log.e("onError", e.message!!)
                    Toast.makeText(context, "Application BE is not available!",
                        Toast.LENGTH_LONG).show()
                }
            }

            webRepository.computeChordsPrediction(audioFile)
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(onsetResponse)
        }
    }
}