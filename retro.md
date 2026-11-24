# Retrospektiivit

## 1. Sprintin retro

### Glad
- Saatiin kaikki vaaditut asiat tehtyä.
- Jokainen ryhmän jäsen osallistui työskentelyyn.
- Saatiin asiat toimimaan sekavan alun jälkeen
- Tekniset asiat saatiin toimimaan.

### Sad
- Taskit oli sekavia ja riippuivat toisistaan liikaa.
- Kaikilla taskeilla ei ollut nimettyä tekijää heti suunnitteluvaiheen jälkeen-
- Ei saatu kaikkia ominaisuuksia tehtyä.
- Taskit olivat epäselviä, joka aiheuttaa päällekkäisiä asioita ja koodissa konflikteja.
- Pitäisi jakaa työt loogisiksi kokonaisuuksiksi.
- Pylintistä olisi hyötyä tyylin littyviin "typoihin" (jotka eivät kuitenkaan vaikuta ohjelman toimintaan).
- Paremmat käytännöt koodin katselmointiin.

### Mad
- Pyörästä puhkesi kumi.
- Miniprojektin ohjeet ovat hieman pirstaleisesti laitettu useaan paikkan.

### Valitut taskeiksi

- pyörän kumin paikkaus
- pep8 lint setup
- taskien sopiva jakaantuminen päällekkäisyyksien välttämiseksi


## 2. Sprintin retro

! Käykää läpi, miten edellisen retrospektiivin parannuskohteet toteutuivat.

### Edellisten parannuskohteiden toteutuminen
- pyörän kumi korjattu.
- pylint otettiin käyttöön ja saatiin CI:hin.
- Taskit jakautuivat sopivammin ja riippuvuutta/odottelua oli vähemmän.

! Jokainen miettii hiljaa minuutin ajan yhden asian, joka sujui sprintissä hyvin. Sen jälkeen kukin kertoo omansa lyhyesti, ja asiasta keskustellaan. Miettimisaikaa voi tarvittaessa pidentää kahteen minuuttiin.

### Mietittiin hiljaa minuutin verran asioita jotka sujui:
- kehitys nopeampi/vähemmän odottelua hyvän kommunikaation takia.
- enemmän velocityy. Taskit jakautuivat mukavasti ja päästiin jaettua töitä reilusti.
- päästy vauhtiin. Taskeja ei kasaudu ja kaikki pääsevät tekemään hyviin.
- vähemmän aikaa ohjeisiin perehtymiseen ja projektista kiinni saamiseen


### Mitä voitaisiin parantaa
- merget aikaisimmin, esim. asiakastapaamista edeltävänä päivänä.
- enemmän kommunikaatiota kun +1 henkilö työskentelee saman systeemin osan parissa. Esim. saman storyn eri taskeja tehdessä.
- hyvin samaan asiaan liittyvät/peräkkäiset taskit ehkä samalle henkilölle. Esim. uuden lähdetyypin lisääminen hoituu vähemmällä vaivalla kun yks henkilö tekee molemmat peräkkäin/kerralla. 


## Mitä voitaisiin lopettaa
- koitetaan välttää mergejen kasaantumista.
- vältetään sitä että asiakastapaamisen päivänä tulee merge konflikteja.
- Ei enää rikota klusterilla tietokantaa.


## Kolme parannuskohdetta.
1. ei puoli tunta ennen asiakastapaamiseta mergekonflikteja/juttuja.
2. Linkit/webhookit discord kommunikaatiossa.
3. Ei rikota tietokantaa; muistetaan sen resetointi/ylläpito klusterilla, esim. erillisenä taskina.
