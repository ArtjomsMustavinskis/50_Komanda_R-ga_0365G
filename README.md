# 50_Komanda_R-ga_0365G
Projekta struktūrai jābūt šādai (kopā 4 faili):

1. Interfeiss – lietotāja saskarne spēlei.
  Lietotāja saskarne (UI) ar iespēju:
  Apskatīt spēles skaitļu virkni
  Veikt gājienus
  Sākt jaunu spēli
  Redzēt punktus un uzvarētāju
2. Minimax algoritms – loģika ar Minimax stratēģiju.

3. Alfa-beta algoritms – loģika ar Alpha-Beta griešanu.

4. Apvienojums – fails, kas apvieno interfeisu ar izvēlēto algoritmu un veido pilnībā funkcionējošu spēli.

Lūdzu, visus failus un izmaiņas pievienojiet mapē “Shared”.

________________________________________
Īss spēles apraksts
1.	Spēles sākumā tiek piedāvāta ģenerētā skaitļu virkne. Katram spēlētājam sākotnēji ir 0 punkti.
2.	Spēlētāji gājienus veic secīgi. Gājiena laikā spēlētājs var: 
-	Paņemt jebkuru skaitli no virknes un pieskaitīt to savam punktu skaitam.
-	Sadalīt skaitli “2” divos skaitļos “1” un “1” un pieskaitīt vienu punktu pretiniekam.
-	Sadalīt skaitli “4” divos skaitļos “2” un “2” un atņemt vienu punktu no pretinieka punktu skaita.
3.	Spēle beidzas, kad virkne ir tukša. Uzvar tas spēlētājs, kuram ir vairāk punktu.
________________________________________
