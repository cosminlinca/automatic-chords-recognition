package com.ubb.acousticrecognizer.ui.chords.adapters

import android.content.Context
import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.cardview.widget.CardView
import androidx.recyclerview.widget.RecyclerView
import com.ubb.acousticrecognizer.ui.items.Chord
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.ui.chords.PopActivity

class RecyclerViewAdapter(mContext: Context, mData: List<Chord>) :
    RecyclerView.Adapter<RecyclerViewAdapter.MyViewHolder>() {
    private val mContext: Context = mContext
    private val mData: List<Chord> = mData
    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): MyViewHolder {
        val view: View
        val mInflater = LayoutInflater.from(mContext)
        view = mInflater.inflate(R.layout.cardview_chord, parent, false)
        return MyViewHolder(view)
    }

    override fun onBindViewHolder(
        holder: MyViewHolder,
        position: Int
    ) {
        holder.imgChord.setImageDrawable(mData[position].drawable)
        holder.itemView.setOnClickListener {
            val intent = Intent(mContext, PopActivity::class.java)
            intent.putExtra("chordName", mData[position].name)
            mContext.startActivity(intent)
        }
    }

    override fun getItemCount(): Int {
        return mData.size
    }

    class MyViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        var imgChord: ImageView = itemView.findViewById(R.id.chordImageId) as ImageView
        var cardView: CardView = itemView.findViewById(R.id.cardViewForChordId)
    }

}