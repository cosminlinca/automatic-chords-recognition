package com.ubb.acousticrecognizer.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.squareup.moshi.JsonClass
import java.io.Serializable

@Entity(tableName = "onset_table")
@JsonClass(generateAdapter = true)
class LocalDetectionEntity {

    @PrimaryKey
    var AbsolutePath = ""
    var FileName: String = ""
    var Onsets: List<OnsetEntity> = ArrayList()

    constructor(AbsolutePath: String, FileName: String, Onsets: List<OnsetEntity>) {
        this.AbsolutePath = AbsolutePath
        this.FileName = FileName;
        this.Onsets = Onsets
    }
}
