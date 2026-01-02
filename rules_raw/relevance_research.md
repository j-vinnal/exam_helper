Siin on üksikasjalik ülevaade sellest, milliseid konkreetseid **uurimissamme (Research)** pead iga `relevance.md` proovitöö küsimuse puhul ise tegema, et jõuda õige tulemuseni vastavalt juhistele.

### **I. Aadressipäringud ja asukohtade olemasolu**

*   **Q1 ([Alaska]):**
    *   **Research:** Kontrolli, kas päringul on reaalmaailmas rohkem kui üks tähendus (nt samanimeline linn teises riigis). Kuna Alaska on unikaalne osariik, on vastus navigatsioonilise tulemuse küsimusele "Yes".
*   **Q2 ja Q20 (Täisaadressi päringud):**
    *   **Research (USPS):** See on kriitiline. Ava **USPS ZIP Code Lookup** ja sisesta täisaadress.
    *   **Kontroll:** Kui USPS-i allanool näitab **"N" (not deliverable)**, siis aadressi ei eksisteeri. Sel juhul ei tohi sa anda reitingut "Navigational", isegi kui tulemus on identne – maksimaalne hinne on **Excellent**.
    *   **Imagery:** Vaata tänavavaadet (Street View). Kas seal on maja või tühi põld?.
*   **Q7 (Huvipunkti nimi vs puhas aadress):**
    *   **Research:** Kontrolli, kas antud aadress (1000 Fifth Avenue) kuulub tõesti otsitud huvipunktile (The Met Museum). Kui jah, aga tulemus näitab ainult aadressi ilma nimeta, on reiting **Bad** (Lack of Connection).

### **II. Kettäride päringud (Chain Businesses)**

Kettide puhul on **Store Locator** sinu kõige olulisem tööriist.

*   **Q11 ja Q12 ([Starbucks], kasutaja väljaspool Fresh Viewporti):**
    *   **Research:** Ava Starbucksi ametlik Store Locator.
    *   **Sammud:** Leia kõik filiaalid, mis asuvad lilla kasti (viewport) sees.
    *   **Võrdle:** Kui FVP-s on vähemalt 3 filiaali, mis on tulemusest lähemale, pead andma hinde **Good**, mitte Excellent.
*   **Q13 ja Q14 ([Wegmans Rockville MD], selge asukohaga päring):**
    *   **Research:** Kasuta ametlikku kodulehte, et teha kindlaks, kas **Rockville'i linnas** on Wegmansi pood.
    *   **Sammud:** Kui Rockville'is on pood olemas, on teises linnas asuv tulemus **Bad**. Kui tulemus on naaberlinnas ja see on reaalmaailmas "teine lähim", on hinne **Good**.
*   **Q15–Q18 ([Applebee's], kasutaja Fresh Viewporti sees):**
    *   **Research:** Mõõda Store Locatori abil distants **kasutaja asukohast (sinine täpp)** kõigi ümbritsevate filiaalideni.
    *   **Sammud:** Ainult reaalmaailma kõige lähem filiaal saab **Excellent**. Järgmised on **Good** ning väga kauged (kui lähedal on 3+ varianti) on **Acceptable**.
*   **Q19 ([Marshalls tavern Taylor Texas]):**
    *   **Research:** Kontrolli poe staatust konkreetselt Taylori linnas.
    *   **Sammud:** Kui uuring näitab, et Taylori pood on suletud, aga tulemus on lähim avatud filiaal väljaspool linna, on hinne **Excellent**.

### **III. Transiidi huvipunktid (Transit POIs)**

*   **Q9, Q10 ja Q21 (Jaamad):**
    *   **Research:** Ava ametlik transiidikaart (nt BART-i koduleht).
    *   **Sammud:**
        1.  Kontrolli nime täpsust: Kas "16th Street Mission" ja "24th Street Mission" on eri jaamad? (Jah, seega hinne **Bad**).
        2.  Kontrolli asukohta: Kas teine jaam asub samas linnas? (Kui jah, on reiting **Excellent**).

### **IV. Kategooria päringud ja teenustasemed**

*   **Q4 ja Q24 ([mall] või konkreetne malli nimi):**
    *   **Research:** Kasuta malli kataloogi (Mall Directory).
    *   **Sammud:** Veendu, et tulemus on pood malli sees, mitte mall ise. Juhiste järgi on malli otsingul pood **Bad**.
*   **Q23 ([Saks Fifth Avenue] vs [Saks OFF 5TH]):**
    *   **Research:** Uuri brändi kodulehelt, mis on nende erinevus.
    *   **Kontroll:** Kuna OFF 5TH on outlet/discount pood, on see teenustaseme ebakõla ( **Service-Level Mismatch** ) ja hinne algab **Good**'ist.

### **V. Eriolukordade kontrollimine**

*   **Q22 (Stale Viewport):**
    *   **Research:** Vaata TryRatingu päisest teksti värvi. Kui on punane (STALE), ignoreeri lilla kasti asukohta ja võta distantsi aluseks ainult **kasutaja asukoht**.
*   **Q26 (Suletud asutused):**
    *   **Research:** Otsi märke "Permanently Closed" Google'ist või sotsiaalmeediast.
    *   **Oluline:** Kui märgid checkboxi "Closed", pead ikkagi tegema Researchi nii, nagu pood oleks lahti, et määrata relevantsus.

**Analoogia uurimistööks:**
Research on nagu **prokuröri töö kohtus**. Sa ei saa süüdistust (reitingut) esitada ainult selle põhjal, mida kahtlusalune (TryRatingu kaart) ütleb. Sa pead küsitlema tunnistajaid (**USPS, Store Locator, Street View**), et saada teada, mis reaalses maailmas tegelikult toimub.