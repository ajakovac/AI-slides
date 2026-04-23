# Mesterséges inteligencia: hitek és tévhitek
## IX. Onko-Kardiológiai Napok

- **Bevezetés**
    - **AI sikerek**
    - **AI problémák (kihívások)**
    - időnként túl sokat, máskor túl keveset teszünk fel róla
    - jól használható eszköz, de tudni kell a korlátait
    - három kérdéskör:
        - lehet-e okosabb a gép, mint az alkotója
        - miért hazudik az AI?
        - tud-e gondolkodni az AI, van-e öntudata? (érzések vs gondolkodás)

- **Lehet-e okosabb a gép, mint az alkotója?**
    - **hagyományos problémakezelés**
        - megértjük a rendszert
        - algoritmizáljuk
        - kódoljuk
        - a gép olyan okos, mint az alkotója, csak gyorsabb
    - **problémakezelés MI-vel**
        - megértjük a megértést (tanulást)
        - tanulógépet készítünk
        - lekódoljuk $\to$ meta-program, általános célú
        - a gép megérti (megtanulja, training) a probléma kezelését $\to$ aktuális program a probléma megoldására
        - a gép lehet okosabb, mint az alkotója a problémamegoldás terén, de nem okosabb a megértés megértése terén

- **Miért hazudik az AI?**
    - **jelenség**
        - amikor kérdezünk valamit, olyan dolgokat generál, amely nem felel meg a valóságnak (kép és szöveg generálása közben)
        - teljesen egyszerű helyzetekben nem képes a mintafelismerésre (klasszifikációnál)
        - hallucináció, kreativitás vagy hazugság?
    - **az AI működése** (generálás, nyelvi modellek): azt tanulja meg az AI, mi következik egy adott szövegelőzményből
        - "figyelem" (attention) mechanizmus, csak az odavágó részekre figyel
        - AI függvény: szövegelőzmény $\to$ lehetséges következő szavak (valószínűség)
        - utána véletlenszerűen választ
        - nem használ adatbázist, a tudás kódolva van az AI függvényben
    - **AI és tudás**: az AI nem "tud" semmit (nincs valóságképe), csak vakon megy előre (l. majom és a Háború és béke)
        - nem tudja mit nem tud
        - nem tudja, ha valami hamisat állít
        - nem tudja, mit tud $\to$ egy jó promttal sokkal több információt lehet belőle kihozni
        - el van kódolva benne a valaha leírt összes szöveg (500 milliárd paraméter)
    - **fejlesztés**
        - a mai AI-ok próbálnak közelebb kerülni a valósághoz
        - használhatnak információt (internet, adatbázisok) $\to$ RAG rendszerek
        - többször feldolgozzák a választ
        - többször iterálnak, az eredményt megvizsgálják, vajon függetlenül ránézve igaznak tűnik-e (reasoning)
        - még messze vagyunk a hallucinációmentes AI-tól

- **tud-e gondolkodni az AI, van-e öntudata?**
    - néha úgy tűnik, az "AI öntudatra ébred", átveszi a hatalmat (AI doomsday)
    - generálás mentális modellje: System I $\to$ még akkor is, ha magának ad feladatot, csak generál
    - ha túl bonyolult a valóság, kell egy valóság reprezentáció, az új (szenzoros vagy belső) információk csak frissítik a valóságmodellt (System II)
    - döntési mechanizmus: mindkettőt figyelembe veszi
    - öntudat, én-kép: el kell helyeznünk magunkat a valóságban, az AI-nak ilyen képessége nincsen
    - gondolkodás: különböző scenariók kidolgozása anélkül, hogy a döntést meghoznánk $\to$ reasoning modellek kezdenek effelé menni, de AI-ban a valóság reprezentációja $\sim$ pár Mb, az általános tudás $sim$ 1000Gb
    - az AI nem gondolkodik, hanem a megérzéseire hallgat (mint amikor egy rossz diák vizsgázik)
    - eredmény: a generált szöveg kontrollja nagyon kezdetleges, céltalan, struktúrálatlan, a gondolkodást kezdetlegesen, az öntudatot egyáltalán nem tudja megvalósítani.

- **Összefoglalás**
    - mire használhatók a nyelvi modellek?
        - egy univerzális lexikon, amely szemantikusan tudja leválogatni az információt
        - az emberiség tudása benne van (kódolva)
    - mire használható az AI egyéb területen
        - mindenhol, ahol heurisztikára, ráérzésre van szükség
        - nem zavarja a monotonitás
    - mire nem használható az AI
        - tervezésre, absztrakcióra, fogalomalkotásra
        - megbízható döntésekre
