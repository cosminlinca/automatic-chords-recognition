package com.ubb.acousticrecognizer.ui.home

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProviders
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.data.db.AppDatabase
import com.ubb.acousticrecognizer.ui.MyViewModelFactory
import com.ubb.acousticrecognizer.ui.home.adapters.CardArrayAdapter
import com.ubb.acousticrecognizer.ui.items.CardItem
import com.ubb.acousticrecognizer.ui.music_player.GuitarMusicPlayerActivity
import com.ubb.acousticrecognizer.utils.Constants
import java.io.File


class HomeFragment : Fragment() {

    private lateinit var homeViewModel: HomeViewModel
    private var cardArrayAdapter: CardArrayAdapter? = null
    private val cardList: ArrayList<CardItem> = ArrayList()
    private var listView: ListView? = null

    override fun onResume() {
        super.onResume()

        cardArrayAdapter!!.notifyDataSetChanged()
        // Find local detections and update array adapter
        val localDB = AppDatabase.getInstance(context!!)
        for (cardItem: CardItem in cardArrayAdapter!!.getCardList()) {
            val currentCard = localDB.detectionEntityDao()
                .getByAbsolutePath(cardItem.absolutePath)
            if(currentCard != null) {
                cardArrayAdapter!!.updateSavedImgStatus(currentCard.AbsolutePath)
            }
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        homeViewModel =
            ViewModelProviders.of(this, MyViewModelFactory(context)).get(HomeViewModel::class.java)
        val root = inflater.inflate(R.layout.fragment_home, container, false)
        initializeUIElements(root)
        initSearchEditTest(root)

        return root
    }

    private fun initSearchEditTest(root: View?) {
        val searchEditTest = root!!.findViewById<EditText>(R.id.searchEditText)
        searchEditTest.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable?) {
                filter(s.toString())
            }

            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {
            }

            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
            }

        })
    }

    private fun filter(text: String) {
        val filteredList = ArrayList<CardItem>()
        for (item in cardList) {
            if(item.name.toLowerCase().contains(text.toLowerCase())) {
                filteredList.add(item)
            }
        }
        cardArrayAdapter!!.filterList(filteredList)
    }

    private fun initializeUIElements(root: View) {
        listView = root.findViewById(R.id.card_listView) as ListView
        listView!!.addHeaderView(View(context))
        listView!!.addFooterView(View(context))

        val rootFile = File(Constants.rootDirectoryPath)
        // Set total value for audio files
        val textViewAudioTotalValue = root.findViewById(R.id.textViewAudioTotalValue)
                                                    as TextView
        textViewAudioTotalValue.text = rootFile.listFiles()!!.size.toString()

        // Create array adapter
        cardArrayAdapter = CardArrayAdapter(
            context,
            R.layout.list_item_card,
            textViewAudioTotalValue
        )
        for (audioFile in rootFile.listFiles()!!) {
            if(!audioFile.isDirectory) {
                val card = CardItem(audioFile.name, audioFile.absolutePath)
                cardList.add(card)
                cardArrayAdapter!!.add(card)
            }
        }

        // Set on item click event
        listView!!.onItemLongClickListener =
            AdapterView.OnItemLongClickListener { parent, view, position, id ->
                var selectedItem = cardArrayAdapter!!.getItem(position - 1)
                val intent = Intent(context!!, GuitarMusicPlayerActivity::class.java)
                intent.putExtra("audioFileName", selectedItem.name)
                intent.putExtra("audioFilePath", selectedItem.absolutePath)
                startActivity(intent)

                true
            }

        // Set list view adapter
        listView!!.adapter = cardArrayAdapter
    }
}
