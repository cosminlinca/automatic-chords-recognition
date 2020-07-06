package com.ubb.acousticrecognizer.data.dao

import androidx.room.*
import com.ubb.acousticrecognizer.data.model.LocalDetectionEntity
import com.ubb.acousticrecognizer.data.model.OnsetEntity

@Dao
interface LocalDetectionEntityDao {

    @get:Query("SELECT * FROM onset_table")
    val getAll: List<LocalDetectionEntity>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    fun insert(localDetectionEntity: LocalDetectionEntity)

    @Delete
    fun delete(localDetectionEntity: LocalDetectionEntity)

    @Query("DELETE FROM onset_table")
    fun deleteAll()

    @Transaction
    @Query("SELECT * FROM onset_table where AbsolutePath=:absolutePath")
    fun getByAbsolutePath(absolutePath: String): LocalDetectionEntity?
}