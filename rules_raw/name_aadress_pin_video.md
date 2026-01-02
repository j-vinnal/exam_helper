Siin on struktureeritud Markdown-fail, mis võtab kokku **Pin Accuracy** (nõela täpsuse) määramise reeglid, tuginedes veebiseminarile "Pin_rating.mp4", "Guidelines.pdf" dokumentatsioonile ja muudele koolitusmaterjalidele.

---

# Nõela täpsuse (Pin Accuracy) määramise juhend

## 1. Üldpõhimõtted
*   **Sõltumatus:** Nõela täpsust hinnatakse teistest andmetest (nimi, aadress, relevantsus) **sõltumatult**. Pin võib olla *Perfect*, isegi kui aadressis on viga.
*   **Peegeldus:** Nõel peab olema tulemuse (POI) tegelik peegeldus reaalses maailmas.
*   **Asukoht:** Nõela asukohta tähistab selle **terav tipp**, mitte nõela pea.
*   **Tõenduspõhisus:** Mida rohkem on tõendeid (Street View, mall directory), seda täpsem peab nõel olema, et saada hinne *Perfect*.

---

## 2. Hindamisskaala

| Reiting | Kirjeldus ja kriteeriumid |
| :--- | :--- |
| **Perfect** | Nõel asub **otse huvipunkti katusel** (*rooftop*) või määratud objekti alal (nt admin-polügoon). |
| **Approximate** | Nõel asub **kinnistu piirides** (*property boundaries*), kuid väljaspool *Perfect* ala (nt parklas või abihoone katusel). |
| **Next Door** | Nõel asub **vahetult kõrvalasuval kinnistul**, mis jagab sama tänavat ja asub samas kvartalis. |
| **Wrong** | Nõel asub väljaspool *Approximate* või *Next Door* piire (nt teisel pool teed). |
| **Can't Verify** | Kasutatakse, kui asukohta ei saa kindlaks teha või kui **aadressi ei eksisteeri**. |

---

## 3. Detailne loogika ja näidistsenaariumid

### A. Üksik hoone ja elamukinnistud
*   **Perfect:** Pin on peahoone (elumaja) katusel.
*   **Approximate:** Pin on samal krundil, aga parklas, aias või **abihoonel** (kuur, garaaž, varjualune).
*   **Tennis Rule:** Kui nõela tipp puudutab piirjoont, loetakse see sissepoole jäävaks (*In*).

### B. Jagatud katus ja kaubanduskeskused (*Shared Rooftop / Strip Mall*)
Siin kehtib **"Parima tõendi reegel"** (GL 9.2.2):
1.  **Kui täpne asukoht on tuvastatav** (Street View või malli kaardi abil):
    *   *Perfect:* Ainult see katuseosa, kus äri tegelikult asub.
    *   *Approximate:* Sama hoone ülejäänud katuseosad (naaberpoed) või ühine parkla.
2.  **Kui täpset asukohta ei saa tuvastada:**
    *   *Perfect:* Kogu jagatud katus on *Perfect* ala.
    *   *Approximate:* Ühine parkla.

### C. Transiidi huvipunktid (Transit POIs)
*   **Perfect:** Pin on jaamahoone katusel, platvormil või ootealal.
*   **Approximate:** Pin on ootealast väljas, kuid **50 meetri raadiuses** või jaama parklas/territooriumil.
*   **NB!** Transiidi-POI-del **puudub *Next Door*** reiting.

### D. Haldusüksused (Linnad, linnaosad)
*   **Perfect:** Pin asub TryRatingu kaardil kuvatava **polügooni (piirjoone) sees**.
*   **Wrong:** Pin on polügoonist väljas.
*   **NB!** Haldusüksustel **puuduvad *Approximate* ja *Next Door*** reitingud.

---

## 4. Tehnilised erireeglid

*   **Satellite vs. Vector:** Kui kihid on nihkes, vali alati see kiht, mis on **nõela suhtes heldem** (annab parema hinde).
*   **Missing Pin / 0,0:** Kui nõela ei kuvata või see asub koordinaatidel 0,0 (ookeanis Aafrika rannikul), on hinne alati **Wrong**.
*   **Next Door piirangud:**
    *   Ei kehti, kui hoonete vahel on **ristuv tänav** (siis on *Wrong*).
    *   Ei kehti jagatud parklaga aladel (strip mall).

---

## 5. Uurimistöö (Research) kontroll-leht

1.  **Kontrolli TryRatingu kihte:** Kas nõel on katusel satelliidi- või vektorkihil?
2.  **Kasuta Street View'd:** Kas hoone fassaadil on õige nimi/logo? Kas nõel vastab sissepääsule?
3.  **Ametlikud allikad:** Kasuta kaubanduskeskuse kataloogi (*Mall Directory*) või äri kodulehte täpse asukoha leidmiseks.
4.  **USPS (USA puhul):** Kui aadressi ei eksisteeri (USPS ütleb "N"), märgi nõela reitinguks *Can't Verify*.
5.  **Kommenteerimine:** Kommentaar on kohustuslik, kui reiting ei ole *Perfect*. Lisa koordinaadid ja allika link.

---

**Analoogia (Tennis Rule):**
Pin Accuracy hindamine on nagu **tennisekohtuniku töö**. Kui pall (nõela tipp) puudutab joont, on see mängus (*In* ehk *Perfect/Approximate*). Kui pall on joonest väljas, on see *Out* (liigub järgmisele reitingutasemele).