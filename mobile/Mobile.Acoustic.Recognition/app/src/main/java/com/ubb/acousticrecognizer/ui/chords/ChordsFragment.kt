package com.ubb.acousticrecognizer.ui.chords

import android.content.res.Resources
import android.graphics.drawable.BitmapDrawable
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProviders
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.ubb.acousticrecognizer.R
import com.ubb.acousticrecognizer.external.chorddroid.helper.DrawHelper
import com.ubb.acousticrecognizer.ui.chords.adapters.RecyclerViewAdapter
import com.ubb.acousticrecognizer.ui.items.Chord


class ChordsFragment : Fragment() {

    private lateinit var chordsViewModel: ChordsViewModel

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        chordsViewModel =
                ViewModelProviders.of(this).get(ChordsViewModel::class.java)
        val root = inflater.inflate(R.layout.fragment_chords, container, false)
        drawChords(root)

        return root
    }

    private fun drawChords(root: View?) {
        val chordsList = arrayListOf<Chord>()

        var chord = drawChordHelper("A")
        chordsList.add(Chord("A", chord))

        chord = drawChordHelper("A#")
        chordsList.add(Chord("A#", chord))

        chord = drawChordHelper("A#m")
        chordsList.add(Chord("A#m", chord))

        chord = drawChordHelper("Am")
        chordsList.add(Chord("Am", chord))

        chord = drawChordHelper("B")
        chordsList.add(Chord("B", chord))

        chord = drawChordHelper("Bm")
        chordsList.add(Chord("Bm", chord))

        chord = drawChordHelper("C")
        chordsList.add(Chord("C", chord))

        chord = drawChordHelper("C#")
        chordsList.add(Chord("C#", chord))

        chord = drawChordHelper("C#m")
        chordsList.add(Chord("C#m", chord))

        chord = drawChordHelper("Cm")
        chordsList.add(Chord("Cm", chord))

        chord = drawChordHelper("D")
        chordsList.add(Chord("D", chord))

        chord = drawChordHelper("D#")
        chordsList.add(Chord("D#", chord))

        chord = drawChordHelper("D#m")
        chordsList.add(Chord("D#m", chord))

        chord = drawChordHelper("Dm")
        chordsList.add(Chord("Dm", chord))

        chord = drawChordHelper("E")
        chordsList.add(Chord("E", chord))

        chord = drawChordHelper("Em")
        chordsList.add(Chord("Em", chord))

        chord = drawChordHelper("F")
        chordsList.add(Chord("F", chord))

        chord = drawChordHelper("F#")
        chordsList.add(Chord("F#", chord))

        chord = drawChordHelper("F#m")
        chordsList.add(Chord("F#m", chord))

        chord = drawChordHelper("Fm")
        chordsList.add(Chord("Fm", chord))

        chord = drawChordHelper("G")
        chordsList.add(Chord("G", chord))

        chord = drawChordHelper("G#")
        chordsList.add(Chord("G#", chord))

        chord = drawChordHelper("G#m")
        chordsList.add(Chord("G#m", chord))

        chord = drawChordHelper("Gm")
        chordsList.add(Chord("Gm", chord))

        val recyView = root!!.findViewById(R.id.recyclerViewId) as RecyclerView
        val myAdapter = RecyclerViewAdapter(context!!, chordsList)
        recyView.layoutManager = GridLayoutManager(context!!, 3)
        recyView.adapter = myAdapter
    }

    private fun drawChordHelper(chordValue: String): BitmapDrawable {
        val resources: Resources = resources
        val width = 300
        val height = 300
        val chordName = chordValue
        val position = 0 // fret position index (0 to 8)
        val transpose = 0 // transpose distance (-12 to 12)

        // Draw chord
        val chord = DrawHelper.getBitmapDrawable(
            resources, width, height, chordName, position, transpose
        )

        return chord
    }
}