# 50_Komanda_R-ga_0365G
________________________________________
Projekta struktūrai jābūt šādai (kopā 4 faili):
1. Interface.py – Lietotāja saskarne (UI) ar iespēju:
- Apskatīt spēles skaitļu virkni
- Veikt gājienus
- Sākt jaunu spēli
- Redzēt punktus un uzvarētāju
2. Minimax.py:
- AI loģika ar klasisko Minimax algoritmu, kur dators izvēlas labāko iespējamo gājienu, apsverot visus iespējamos iznākumus līdz spēles beigām.
3. AlfaBeta.py:
- AI loģika ar uzlabotu Alpha-Beta griešanas algoritmu, kas ir efektīvāka versija Minimax algoritmam ar to pašu mērķi — izvēlēties optimālo gājienu.
4. Main.py:
- Galvenais fails, kas apvieno interfeisu ar izvēlēto algoritmu. Šeit tiek inicializēta spēle, piesaistīta loģika un palaista programma.

Lūdzu, visus failus un izmaiņas pievienojiet mapē “Shared”.
________________________________________
Īss spēles apraksts:
1. Spēles sākumā tiek ģenerēta nejauša skaitļu virkne (piemēram, [1, 2, 4, 2, 1]).
2. Katram spēlētājam sākotnēji ir 0 punkti.
3. Gājiena laikā spēlētājs var:
-	Paņemt jebkuru skaitli no virknes un pieskaitīt to savam punktu skaitam.
-	Sadalīt skaitli “2” divos skaitļos “1” un “1” un pieskaitīt vienu punktu pretiniekam.
-	Sadalīt skaitli “4” divos skaitļos “2” un “2” un atņemt vienu punktu no pretinieka punktu skaita.
4.	Spēle beidzas, kad virkne ir tukša. Uzvar tas spēlētājs, kuram ir vairāk punktu.
5. Vadība
- "Shift + 2" → sadala 2 uz (1 un 1), dod +1 punktu pretiniekam
- "Shift + 4" → sadala 4 uz (2 un 2), atņem -1 punktu pretiniekam
- Pele un tastatūra → lai veiktu izvēli spēles interfeisā
________________________________________
Nepieciešamās bibliotēkas:
- Pygame – interfeisam un spēles logam
- random – sākotnējās virknes ģenerēšanai
________________________________________
