# Recunoașterea automată a acordurilor muzicale <br> utilizând Inteligența Artificială(Machine Learning)
**Google Colab**: https://colab.research.google.com/drive/1CxuCb9kboNEOR6cVH30R52C8VRSKCttQ#scrollTo=CTatgj_fpKBD&uniqifier=1
- About Google Colab - https://www.geeksforgeeks.org/how-to-use-google-colab/
<hr>

- **Libraries**:
    - LibROSA - librărie Python pentru analiză audio. Furnizează pachetele necesare construirii unui sistem de obținere a informațiilor muzicale ("music information retrieval systems"); https://librosa.github.io/librosa/index.html
    - Numpy -
    - Matplotlib - 
    - TensorFlow - 
    - Keras - 
    - Pandas - 

- **Link-uri**
    - https://www.technics.com/us/high-res-audio/what-is-high-resolution-audio.html - imagine?
    - https://victorimpmooc.wordpress.com/ - imagine
    - https://www.wikiwand.com/ro/Transformata_Fourier - transformata Fourier
    - **Pentru ecuatii**: http://latex.codecogs.com/
    - https://ro.wikipedia.org/wiki/Intensitate_sonor%C4%83
    
- **Referințe**
    - Structura: https://libguides.lub.lu.se/c.php?g=297505&p=1984175 <br>
    - Articole/Carti - folder: *Documents*

- **Intrebari**
    - Romana sau engleza?
     - Romana
    - Latex sau Word? - Overleaf
    - Titlu licenta?
      - Recunoasterea automata a unei partituri muzicale 
    - Structura licentei - Cuprins
    - Putem lua poze/diagrama? Daca da, cum mentionam sursa?
    - Preluarea de definitii - adaptare; cum mentionam sursa?
    - Cum se scriu referintele?
    - ?Despre dateset - discografia Beatles, Queen etc. / dataset doar cu sunetele de chitara -> cate labeluri?(25?)
    - Despre modelele de clasificare - abordare prin comparatie
    - Despre aplicatia mobile/web
      - Gestiunea sunetului inregistrat -> trimitere catre BE (python) -> procesare -> onset detection -> predictie -> raspuns server cu acordurile pe intervale de timp -> procesare raspunse la nivel de FE
      REST Api -> library python pentru asta? - Flask?
      - SAU TensorFlow Lite => ? procesare sonora la nivel de FE
    - (5% sanse) **Idee: Impartirea track-urilor acustice in categorii de stiluri: Folk, Rock, Jazz etc. 
<hr>

        CURPINS
        -> 0.Abstract
        -> 1.Introducere
        -> //2.Teorie muzicală cu aplicabilitate matematică 
        -> 2. Notiuni introductive
            - Note, Acorduri, Frecvențe
        -> 3.Metode de procesare a semnalului sonor
            - Short-Time Fourier Transform
            - Q-Transform
        -> 4.Metode de clasificare - Machine learning algorithms - "Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow"
            - Regresie logistică
            - Rețea neuronală - "Multi Layer Perceptron Neural Network (MLPNN)"
            - Deep Belief Networks?
            - CNN
            - RNN?
            - Articol cu rezultate comparative intalnite folosind diverse metode (TRSI) - posibil in 5
            -> *Data augmentation asupra dataset-ului*
            -> *Data normalization* - ?
        -> 5.Rezultate experimentale
        -> //6.Implementarea algoritmului
        -> 6. Studiu de caz
            -> Arhitectura sistemului
            -> Proiect aplicativ - o parte la TRSI
            -> *Onset detection
        -> 7.Implementarea unei aplicatii **mobile**/web
        -> 8.Concluzii
        -> 9.Bibliografie

### ELL - Descrierea temei de licență
Recunoașterea automată a acordurilor muzicale utilizând Inteligenta Artificiala/algorimi de Machine Learning <br>
- Subiectul propus pentru tema de licență urmarește prezentarea și implementarea unui proces complex obținut prin îmbinarea a două domenii aparent diferite: muzica și inteligența artificială. 
- Prima parte (recunoașterea automată a acordurilor muzicale), reprezentând domeniul muzical, definește procesul automat capabil să analize o mostră muzicală, sa determine succesiunea continuă de acorduri diferite și să reprezinte automat această succesiune într-un format standard, numit tabulatură muzicală (format specific acordurilor acustice). Analiza unei mostre muzicale și extragerea unor trăsături specifice se realizează aplicând algoritmi de procesare pentru semnalul audio, algoritmi care vor fi analizați și discutați separat și prin comparație în următoarele capitole.
- Partea a doua (inteligența artificială), reprezintă unealta care stă la baza proceselor de învățare și deosebire a trăsăturilor unor acorduri din cadrul unei mostre muzicale. Se vor enunța și prezenta în detaliu câțiva algoritmi de machine learning cu aplicabilitate pentru problema noastra, cu scopul de a ajunge treptat la un algoritm complex capabil să analizeze automat semnalul audio, să clasifice cu o precizie cât mai mare fiecare acord, fără a fi necesară intervenția umană în corectarea rezultatului. 

## 0. Abstract
## 1. Introducere

## 2. Teorie muzicală cu aplicabilitate matematică
În acest capitol ne vom focusa asupra principalelor concepte din teoria muzicală, concepte necesare în înțelegerea modalităților de prelucrare și reprezentare ale sunetelor.


## 3. Metode de procesare a semnalului sonor
În acest capitol ne vom axa pe studiul diferitelor metode de procesare low-level a semnalului sonor, cu scopul obținerii unor caracteristici și a
unei reprezentări care va fi utilizată mai departe în antrenarea și clasificarea unui algoritm de machine learning.
### 3.1. Sunetul - un sistem dependent de timp
- **Sunetul**, prin definiție, este un semnal de tip mono-dimensional, dependent de timp, reprezentând presiunea aerului asupra canalului uman auditiv. Sistemul auditiv uman este capabil să perceapă orice semnal sonor care se află în intervalul de frecvență **20Hz - 20000Hz** (=20kHz).
- **Frecvența** se definește ca numărul de repetări ale unui fenomen sau eveniment periodic într-un interval de timp. Unitatea de măsură pentru frecvență este Hertz, simbolizat ca Hz, denumită astfel în cinstea fizicianului german Heinrich Hertz. Astfel, o frecvență f = 1 Hz este corespunzătoare unei perioade de timp de o secundă. Putem astfel afirma că dacă un anumit eveniment se repetă la un interval de timp T, putem calcula frecvența ca f = 1/T.
- In ceea ce privește sunetul, frecvența este legată de noțiunea de înălțime muzicală. Astfel, pentru nota La din gama centrală se definește frecvența de 440 Hz, ceea ce înseamnă că aerul pus în mișcare de unda sonoră corespunzătoare oscilează de 440 de ori pe secundă. 
- Sunetul capturat de către un **microfon** este o undă dependentă de timp, determinând variația presiunii aerului în câmpul sonor în care se află microfonul. Astfel, un semnal audio digital este obținut prin prelevarea și cuantificarea adecvată a ieșirii microfonului, reprezentat de unde electice. Deși orice frecvență peste 40kHz ar fi suficientă pentru a capta întreaga gamă de frecvențe perceptibile, rata de preluare utilizată pe o scară largă este de 44.100 Hz, stabilită în urma nevoii de a sincroniza sunetul cu datele de tip video. Calitatea de tip "CD" se referă la o mostră audio digitală cu frecvența de 44.1 kHz și 16-bit ("Bit depth" ~ adâncimea de biți, reprezintă numărul de biți de informație aflați în fiecare mostră/eșantion audio). <br>
- Pentru a înțelege mai bine calitatea sunetului în funcție de adâncimea de biți observăm Figura 1.1.
![](bits_ex.jpg "Figura 1.1...")
- Prin **intensitate sonoră** se înțelege senzația produsă de amplitudinea unei unde sonore(=volumul vibrației) asupra organului uman auditiv. Cu cât amplitudinea este mai mare, cu atât crește și intensitatea sunetului care rezultă. 
Intensitatea sonoră se măsoară în unități denumite în fizică decibeli(dB) sau foni (un decibel este echivalent cu un fon)
    - Auzul uman este limitat de un interval în ceea ce privește intensitatea sunetului, și anume:
       - marginea inferioară:
            - prag auditiv -> 0 dB
            - sunete foarte slabe ca intesitate(Exemple: sunete din natură, nivelul de zgomot dintr-o bibliotecă) -> 10-20 dB 
       - marginea superioară:
            - sunete extrem de puternice ca intensitate(Exemplu: decolarea unui avion cu reacție) -> 120-130 dB
            - prag dureros -> 140 dB


### 3.2 Metode de procesare
- În această secțiune voi prezenta în detaliu 2/3 metode de procesare a semnalului audio, metode care să contribuie la reprezentarea ulterioară a acestuia.
#### 3.2.1 Short-Time Fourier Transform
- Pentru a putea defini metoda este nevoie să definim bazele, pornind de la **Transformarea Fourier** (Fourier Transform ~ FT/TF). 
- Vom începe prin a considera drept exemplu un semnal pur cu frecvența de 3Hz, pe un interval de timp vizibil.
- Poză
- Vom încerca să transpunem această undă dependentă de timp în jurul unui cerc - coardă, în așa fel încât valorile extreme ale funcției din prima reprezentare să fie asociate cu distanțele maxime în raport cu originea din ceea de-a doua reprezentare. Astfel, o  parcurgere de la timpul t0 = 0 pană la timpul tn = 2sec va fi echivalentă cu o singură rotație de cerc. De aici observăm că trebuie să luăm în considerare o nouă frecvență, și anume frecvența de realizarea a unui rotații complete de cerc, fcerc. Această frecvență poate fi ajustată în orice fel de dorim, dar valoarea ei influențează modul în care se reprezintă coarda în reprezentarea a doua. 
- Să presupunem că această coardă are o masă și considerăm punctul din figură ca fiind centrul de masă al corzii. Se observă că odată cu modificare frecvenței cerc, se modifică și poziția centrului de masă, care se situează într-o vecinătate restrânsă a originii...TBC
- Poză

- În matematică, "Transformata Fourier" este o operație care se aplică unei funcții complexe și produce o altă funcție complexă care conține aceeași informație ca funcția originală, dar reorganizată dupa frecvențele componentelor. Pentru problema noastră, considerăm o funcție reprezentată de un semnal dependent de timp. Transformata Fourier a funcției descompune semnalul după frecvență și produce un *spectru* al acestuia.
- Studiul transformatei Fourier pornește de la studiul seriilor Fourier, folosite pentru a analiza funcții periodice complexe și pentru a le descompune ca sume ponderate de unde matematice reprezentate de funcțiile sinus și cosinus. Propietățile acestor funcții ne permit să revenim la valorea fiecarei unde prin intermediul unei integrale. 
- Una dintre cele mai utilizate formule de calcul a transformatei Fourier este: <br>
![](transformata_fourier.jpg)

- Observăm că proprietatea de bază a transformatei este reorganizarea informației după frecvențe (temporale, spațiale sau de alt fel), fiind extrem de utilă în prelucrarea semnalelor de diverse tipuri, în înțelegerea propriețăților unui număr mare de sisteme fizice sau în rezolvarea unor ecuații și sisteme de ecuații.
- O altă proprietate este dată de forma continuă a tranformatei, întrucât integrala este definită pe intervalul de timp(-infinit, infinit). În practică însă, colectarea de date audio se realizează într-un interval finit de timp (de la momentul de start t0 la momentul t(N-1)), ceea ce implică calcului unei tranformate de tip **discret**("Discret Fourier Tranform" ~ DFT). Tranformata de tip discret are aceeași definiție ca tranformata de tip continuu, diferența fiind doar în stabilirea unui interval finit cunoscut, calcul integralei fiind înlocuit de o sumă finită care are următoarea formă: <br>
![](dft_formula.jpg)
- Semnificația fiecărei variabile din formulă este următoarea:
    - x(tn) - semnalul de intrare, la momentul n
    - N  - totalul semnalelor de intrarea (mostre)
    - Xk - valoarea complexă a spectrului corespunzător lui x, la frecvența k
    - tn - nT, unde T reprezintă intervalul de eșantionare a semnalului, măsurat în secunde și n, o valoare de tip întreg, n>=0
    - fs = 1/T - reprezentând rata de eșantionare, măsurată în Hz; 1Hz = 10000 de eșantioane pe secundă ("samples per second")
#### 3.2.2 Transformarea Constant-Q

## 4. Machine learning
- Machine Learning("Învățare automată") este o ramură a Inteligenței Artificiale concentrată pe algoritmi specializați pe invățarea din date. Procesul de învățare constă în deducerea unor tipare, pe baza unor reguli bine stabilite. Mai precis, se urmărește crearea unui program complex capabil să generalizeze un comportament indiferent de datele de intrare. Problemele clasice de machine learning includ clasificare de imagini sau de înregistrări audio, recunoaștere vocală, evaluarea riscurilor financiare pentru diverse investiții sau dezvoltarea unor strategii în jocuri sau simulări. În mod general, abordările algorimilor sunt structurate după obiectivul lor de învățare: <br>
   - A) Învățare supervizată
        - i) Regresie
        - ii) Clasificare
    - B) Învățare nesupervizată
    - C) Reinforcement Learning/Învățare prin întărire
### Rețele convoluționale (CNN)

## 5.Implementarea algoritmului
- **Data normalization/Normalizarea datelor** - utilizand algoritmul "L-inf normalization" - pagina 59 Bonvini;
- Librosa oferă normalizarea de tip L-inf ca fiind prestabilită pentru obtinirea chromogramei atat cu STFT cat si cu Q-Constant. De asemenea, prestabilita este si valorea pentru  threshold = 0.0, astfel orice frame din chromograma cu valorea sub 0 va fi ignorat si setat cu valorea 0 ("Pre-normalizare");

## 7. Aplicatia mobile/web
- Pentru mobile: **TensorFlow Mobile/Lite** - https://code.tutsplus.com/tutorials/how-to-use-tensorflow-mobile-in-android-apps--cms-30957
- Server Python - REST Api

# Articles

# Rethinking Automatic Chord Recognition with Convolutional Neural Networks

- Introduction
Automatic chord recognition is one such task, receiving healthy attention for more than
a decade and is an established benchmark at the annual MIReX challenge (1).

One common definition of a chord is the “simultaneous sounding of two or more notes” [7], but music is seldom so simple. Though the explicit use of chords can
be straightforward – strumming a root-position C major on guitar, for instance – real music is typically characterized by complex tonal scenes that only imply a certain chord or
harmony, often in the presence of nonchord tones and with
no guarantee of simultaneity;

Historically speaking, automatic chord recognition research
is mostly summarized by a few seminal works. Arguably, the two most influential systems are those of Fujishima, who proposed the use of chroma features [3],
and Sheh and Ellis, who introduced the use of Hidden
Markov Models (HMMs) to stabilize chord classification [9].

# Chord Segmentation and Recognition using EM-Trained Hidden Markov Models

## Abstract
- Chords also have the attractive property that a piece of music can (mostly) be segmented into time intervals that consist of a single chord, much as recorded speech can (mostly) be segmented into time intervals that correspond to specific words.
 
- Sequence recognition is accomplished with hidden Markov models (HMMs) directly analogous to
subword models in a speech recognizer, and trained
by the same Expectation-Maximization (EM) algorithm. Crucially, this allows us to use as input only the chord sequences for our training examples, without requiring the precise timings of the chord changes
— which are determined automatically during training. Our results on a small set of 20 early Beatles
songs show frame-level accuracy of around 75% on a
forced-alignment task

## Introduction
Our specific approach uses the hidden Markov models (HMMs)
made popular in speech recognition (Gold and Morgan, 1999),
including the sophisticated Expectation-Maximization (EM) algorithm used to train them.

This is a statistical approach, in which the wide variety of feature frames falling under a single label is modeled as random variation that follows an estimated distribution.

We draw on the prior work of Fujishima (1999) who proposed a representation of audio termed “pitch class profiles” (PCPs), in
which the Fourier transform intensities are mapped to the twelve semitone pitch classes (chroma). This is very similar to the
“chroma spectrum” proposed by Bartsch and Wakefield (2001)
 
The assumption is that this representation captures harmonic information in a more meaningful way, thereby facilitating chord
recognition.

This hugestate space precludes direct training of models for each chord..

## System
- First the input signal is transformed to the frequency domain.
Then it is mapped to the PCP domain by summing and normalizing the pitch chroma intensities, for every time slice. These
features are then used to build chord models via EM. Finally,
chord alignment/recognition is performed with the Viterbi algorithm.

### Pitch Class Profile Features
- Monophonic music recordings x[n] sampled at 11025 Hz are
divided into overlapping frames of N = 4096 points and converted to a short-time Fourier transform (STFT) representation

- **The STFT is then mapped to the Pitch Class Profile (PCP) features, which traditionally consist of 12-dimensional
vectors, with each dimension corresponding to the intensity of a semitone class (chroma).**

### Hidden Markov Models
- PCP vectors are used as features to train a hidden Markov model (HMM) with one state for each chord distinguished by the system.
An HMM is a stochastic finite automaton in which each state generates an observation. The state transitions obey the
Markovian property, that given the present state, the future is
independent of the past.

- If we knew which state (i.e. chord) generated each observation in our training data, the model parameters could be directly
estimated.



