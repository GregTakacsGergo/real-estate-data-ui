/*
==========================================
MySQL cleanup + upsert protection script
==========================================

Motivation / miért kell ez?
- A real_estate_market_data táblába (MySQL) több sor is bekerülhet ugyanarra a dátumra.
- Ez később “duplikált” adatokhoz vezethet riportokban/grafikonokban, és az upsert (INSERT ... ON DUPLICATE KEY UPDATE)
  sem fog működni, amíg nincs olyan UNIQUE/PRIMARY kulcs, amihez ütközni tud.
- A cél: dátumonként pontosan 1 sor maradjon, majd adatbázis-szinten megakadályozzuk, hogy valaha újra duplikálódjon.

Mit csinál a script?
1) Opcionálisan megmutatja, milyen sorokat tekintünk duplikáltnak (ellenőrző SELECT-ek).
2) Törli a duplikált sorokat úgy, hogy dátumonként a LEGKISEBB id maradjon meg (a legkorábban beszúrt rekord).
3) Ellenőrzi, hogy maradt-e duplikáció.
4) Feltesz egy UNIQUE indexet a date oszlopra, hogy az upsert tényleg update-eljen, és ne INSERT-eljen új sort.

Fontos:
- Ha MySQL Workbench “Safe Update Mode” be van kapcsolva, a DELETE-t blokkolhatja (Error 1175).
  Ilyenkor ideiglenesen kikapcsoljuk a session-ben: SET SQL_SAFE_UPDATES = 0; (majd vissza 1-re).
- Éles adatbázison előtte erősen ajánlott backupot készíteni.
*/

/* -----------------------------------------------------------
(0) OPTIONAL: gyors backup (erősen ajánlott éles DB-n)
----------------------------------------------------------- */
-- CREATE TABLE real_estate_market_data_backup AS
-- SELECT * FROM real_estate_market_data;


/* -----------------------------------------------------------
(1) OPTIONAL: régi megközelítés (max(id) marad) – itt csak példa
NE futtasd, ha a MIN(id) megtartása a cél!
----------------------------------------------------------- */
-- Ez a minta törölné a kisebb id-ket (megtartaná a legnagyobb id-t dátumonként)
-- DELETE t1
-- FROM real_estate_market_data t1
-- JOIN real_estate_market_data t2
--   ON t1.date = t2.date
--  AND t1.id < t2.id;

-- Ugyanez SELECT-ben, hogy lásd, mit törölne (max(id) megtartás logika)
-- SELECT t1.*
-- FROM real_estate_market_data t1
-- JOIN real_estate_market_data t2
--   ON t1.date = t2.date
--  AND t1.id < t2.id
-- ORDER BY t1.date, t1.id;


/* -----------------------------------------------------------
(2) OPTIONAL: ellenőrzés egy konkrét dátumra
- Megmutatja, hogy egy adott date-hez hány sor tartozik,
  és id-k szerint hogyan néz ki.
----------------------------------------------------------- */
SELECT id, date, COUNT(*) AS c
FROM real_estate_market_data
WHERE date = '2024-07-02'
GROUP BY id, date
ORDER BY id;


/* -----------------------------------------------------------
(3) Előnézet: mit fogunk törölni, ha MIN(id) marad meg?
- keep_id = dátumonként a legkisebb id
- minden más id az adott dátumhoz “felesleges”, ezeket töröljük
----------------------------------------------------------- */
SELECT t.*
FROM real_estate_market_data t
JOIN (
  SELECT date, MIN(id) AS keep_id
  FROM real_estate_market_data
  GROUP BY date
  HAVING COUNT(*) > 1
) k ON k.date = t.date
WHERE t.id <> k.keep_id
ORDER BY t.date, t.id;


/* -----------------------------------------------------------
(4) Safe update mode kikapcsolása (ha szükséges)
- MySQL Workbench safe mode gyakran blokkolja a JOIN-os DELETE-et (Error 1175)
----------------------------------------------------------- */
SET SQL_SAFE_UPDATES = 0;


/* -----------------------------------------------------------
(5) Törlés: dátumonként csak a MIN(id) maradjon meg
- keep_id = MIN(id) dátumonként
- minden olyan sor törlődik, ahol id != keep_id
----------------------------------------------------------- */
DELETE t
FROM real_estate_market_data t
JOIN (
  SELECT date, MIN(id) AS keep_id
  FROM real_estate_market_data
  GROUP BY date
) k ON k.date = t.date
WHERE t.id <> k.keep_id;


/* -----------------------------------------------------------
(6) Safe update mode visszakapcsolása (jó szokás)
----------------------------------------------------------- */
SET SQL_SAFE_UPDATES = 1;


/* -----------------------------------------------------------
(7) Ellenőrzés: maradt-e duplikált dátum?
- Ha ez a query üres eredményt ad, akkor dátumonként már csak 1 sor van.
----------------------------------------------------------- */
SELECT date, COUNT(*) AS c
FROM real_estate_market_data
GROUP BY date
HAVING c > 1;


/* -----------------------------------------------------------
(8) Védelem a jövőre: UNIQUE(date)
- Ettől kezdve egy dátum csak egyszer szerepelhet.
- Az INSERT ... ON DUPLICATE KEY UPDATE innentől tényleg UPDATE-re vált,
  ha ugyanarra a date-re jön új adat.
Megjegyzés:
- Ha már létezik ilyen index, ez hibát adhat.
----------------------------------------------------------- */
ALTER TABLE real_estate_market_data
ADD UNIQUE KEY uk_real_estate_date (date);
