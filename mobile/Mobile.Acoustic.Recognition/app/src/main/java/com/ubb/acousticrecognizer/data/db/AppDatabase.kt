package com.ubb.acousticrecognizer.data.db

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.ubb.acousticrecognizer.data.dao.LocalDetectionEntityDao
import com.ubb.acousticrecognizer.data.model.LocalDetectionEntity

@Database(entities = [LocalDetectionEntity::class],
          version = 1, exportSchema = false)
@TypeConverters(DataConvert::class)
abstract class AppDatabase : RoomDatabase(){

    abstract fun detectionEntityDao(): LocalDetectionEntityDao

    companion object {

        private var instance: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            if (instance == null) {
                instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java, "local_predictions.db")
                    .allowMainThreadQueries()
                    .fallbackToDestructiveMigration()
                    .build()
            }

            return instance!!
        }
    }
}
