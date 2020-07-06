package com.ubb.acousticrecognizer.ui.home.adapters

import android.app.AlertDialog
import android.content.Context
import android.media.MediaPlayer
import android.net.Uri
import android.view.*
import android.widget.*
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.data.db.AppDatabase
import com.ubb.acousticrecognizer.ui.items.CardItem
import com.ubb.acousticrecognizer.utils.Constants
import java.io.File


class CardArrayAdapter(context: Context?, textViewResourceId: Int,
                       private val textViewCounter: TextView
) :
    ArrayAdapter<CardItem>(context!!, textViewResourceId) {
    private var cardList: ArrayList<CardItem> =
        ArrayList()

    fun getCardList(): List<CardItem> {
        return cardList
    }

    private var cardViewHolderList: ArrayList<CardViewHolder> = ArrayList()

    internal class CardViewHolder {
        var absolutePath: String = ""
        var line1: TextView? = null
        var line2: TextView? = null
        var popupThreeDotsImage: ImageView? = null
        var savedImage: ImageView? = null
        var previewTime: TextView? = null
    }

    override fun add(`object`: CardItem?) {
        cardList.add(`object`!!)
        super.add(`object`)
    }

    override fun getCount(): Int {
        return cardList.size
    }

    override fun getItem(index: Int): CardItem {
        return cardList[index]
    }

    override fun getView(
        position: Int,
        convertView: View?,
        parent: ViewGroup
    ): View {
        var row = convertView
        val inflater =
            this.context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        row = inflater.inflate(R.layout.list_item_card, parent, false)
        val viewHolder: CardViewHolder = CardViewHolder()
        viewHolder.line1 = row!!.findViewById<View>(R.id.line1) as TextView
        viewHolder.popupThreeDotsImage = row.findViewById(R.id.threeDotsMenuImageId)
                                                                as ImageView

        viewHolder.savedImage = row.findViewById(R.id.savedImageId) as ImageView
        viewHolder.previewTime = row.findViewById(R.id.previewTime) as TextView
        row.tag = viewHolder

        // Get card
        val card: CardItem = getItem(position)
        viewHolder.absolutePath = card.absolutePath
        viewHolder.line1!!.text = card.name
        viewHolder.popupThreeDotsImage!!.setOnClickListener {
            showPopup(viewHolder.popupThreeDotsImage!!, position)
        }

        // Find local detections
        val localDB = AppDatabase.getInstance(context!!)
        val currentCard = localDB.detectionEntityDao()
            .getByAbsolutePath(card.absolutePath)
        if(currentCard != null) {
            viewHolder.savedImage!!.visibility = View.VISIBLE
        }

        viewHolder.savedImage!!.setOnClickListener {
            //None
        }

        val mediaPlayer = MediaPlayer.create(context,
            Uri.fromFile(File(card.absolutePath)))
        if(mediaPlayer != null) {
            val totalTime = mediaPlayer.duration
            viewHolder.previewTime!!.text = createTimeLabel(totalTime)

            cardViewHolderList.add(viewHolder)
            mediaPlayer.release()
        }

        return row
    }

    private fun updatetTextViewCounter() {
        textViewCounter.text = cardList.size.toString()
    }

    private fun removeCardListItem(currentCard: CardItem) {
        cardList.remove(currentCard)
    }

    fun updateSavedImgStatus(absolutePath: String) {
        for (viewHolder: CardViewHolder in cardViewHolderList) {
            if(viewHolder.absolutePath == absolutePath) {
                viewHolder.savedImage!!.visibility = View.VISIBLE
            }
        }
    }

    private fun showPopup(v: View, position: Int) {
        val wrapper: Context = ContextThemeWrapper(context, R.style.main_popup_style)
        val popup = PopupMenu(wrapper, v)
        popup.gravity = Gravity.END
        popup.setForceShowIcon(true)
        popup.setOnMenuItemClickListener { item: MenuItem? ->
            when (item!!.itemId) {
                R.id.renameItem -> {
                    val currentCard = getItem(position)
                    val originalFile = File(currentCard.absolutePath)

                    // Create rename file dialog
                    val fileDialog = AlertDialog.Builder(context)
                    fileDialog.setTitle("Rename file")

                    val input = EditText(context)
                    input.setText(currentCard.name)
                    fileDialog.setView(input)

                    fileDialog.setPositiveButton(
                        "Ok") { _, _ ->
                        // New filename
                        val fileName = input.text.toString()

                        // Rename
                        val newFile = File(Constants.rootDirectoryPath, fileName)
                        originalFile.renameTo(newFile)

                        // Notify
                        currentCard.name = fileName
                        currentCard.absolutePath = newFile.absolutePath
                        this.notifyDataSetChanged()
                    }
                    fileDialog.setNegativeButton(
                        "Cancel") { dialog, _ ->
                        dialog.dismiss()
                    }

                    fileDialog.create()
                    fileDialog.show()
                }
                R.id.deleteItem -> {
                    val currentCard = getItem(position)
                    val file = File(currentCard.absolutePath)
                    if (file.exists()) {
                        // AlertBox
                        AlertDialog.Builder(context)
                            .setTitle("Delete recording")
                            .setMessage("Do you want to delete the selected record?")
                            .setPositiveButton(
                                "Yes") { dialog, _ ->
                                val deleted = file.delete()
                                if(deleted) {
                                    // Notify
                                    this.removeCardListItem(currentCard)
                                    this.notifyDataSetChanged()
                                    this.updatetTextViewCounter()
                                }
                            }
                            .setNegativeButton("No", null)
                            .show()
                    }
                }
            }
            true
        }

        popup.inflate(R.menu.popup_menu)
        popup.show()
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    override fun getItemViewType(position: Int): Int {
        return position
    }

    fun filterList(filteredList: ArrayList<CardItem>) {
        cardList = filteredList
        updatetTextViewCounter()
        notifyDataSetChanged()
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
}