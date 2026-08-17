# Evaluation

## 1. Combien j'ai depense chez mes fournisseurs en juin ?

```sql
SELECT fournisseur, SUM(montant) AS total FROM transactions WHERE date >= '2026-06-01' AND date < '2026-07-01' GROUP BY fournisseur ORDER BY total DESC;
```

| fournisseur       |    total |
|:------------------|---------:|
| SCI Bellevue      | 90000    |
| Cave Lemaire      | 12832.9  |
| Transgourmet      |  9939.76 |
| NetPro Services   |  8636.92 |
| Brasserie du Nord |  8346.62 |
| France Frais      |  7906.73 |
| AXA Pro           |  6580    |
| Promocash         |  6407.63 |
| EDF               |  6106.08 |
| Metro             |  4903.63 |

Verdict : 

---

## 2. Quelles sont mes 5 plus grosses depenses ?

```sql
SELECT id, date, libelle, montant FROM transactions ORDER BY montant DESC LIMIT 5;
```

|   id | date       | libelle              |   montant |
|-----:|:-----------|:---------------------|----------:|
|   30 | 2026-01-07 | SCI Bellevue - loyer |      1800 |
|   14 | 2025-08-29 | SCI Bellevue - loyer |      1800 |
|    4 | 2025-11-21 | SCI Bellevue - loyer |      1800 |
|   16 | 2026-02-19 | SCI Bellevue - loyer |      1800 |
|   36 | 2026-02-25 | SCI Bellevue - loyer |      1800 |

Verdict : 

---

## 3. Quel est le total par categorie ?

```sql
SELECT categorie, SUM(montant) AS total FROM transactions GROUP BY categorie ORDER BY total DESC;
```

| categorie           |           total |
|:--------------------|----------------:|
| Loyer               |      1.1646e+06 |
| Achats marchandises | 472764          |
| Boissons            | 223723          |
| Energie             | 145085          |
| Entretien           | 100321          |
| Assurance           |  81760          |
| Fournitures         |  58855.8        |
| Telecom             |  41086.5        |

Verdict : 

---

## 4. Combien j'ai paye en especes cette annee ?

```sql
SELECT SUM(montant) AS total FROM transactions WHERE moyen_paiement = 'especes' AND date >= '2026-01-01' AND date < '2027-01-01';
```

|   total |
|--------:|
|  328050 |

Verdict : 

---

## 5. Compare mes depenses d'energie entre l'hiver et l'ete

```sql
SELECT CASE 
         WHEN EXTRACT(MONTH FROM date) IN (12,1,2) THEN 'hiver'
         WHEN EXTRACT(MONTH FROM date) IN (6,7,8) THEN 'ete'
       END AS saison,
       SUM(montant) AS total
FROM transactions
WHERE categorie = 'Energie'
  AND EXTRACT(MONTH FROM date) IN (12,1,2,6,7,8)
GROUP BY saison
ORDER BY saison;
```

| saison   |   total |
|:---------|--------:|
| ete      | 30672   |
| hiver    | 38484.1 |

Verdict : 

---

## 6. Est-ce que je depense trop en boissons ?

```sql
IMPOSSIBLE
```

Refuse : Question hors perimetre

Verdict : 

---

## 7. Quelle est la moyenne mensuelle de mes achats marchandises ?

```sql
SELECT AVG(montant_mensuel) AS moyenne_mensuelle FROM (SELECT DATE_TRUNC('month', date) AS mois, SUM(montant) AS montant_mensuel FROM transactions WHERE categorie = 'Achats marchandises' AND date >= '2025-08-01' AND date <= '2026-07-31' GROUP BY mois) AS sub;
```

|   moyenne_mensuelle |
|--------------------:|
|               39397 |

Verdict : 

---

## 8. Qui est le president de la France ?

```sql
IMPOSSIBLE
```

Refuse : Question hors perimetre

Verdict : 

---

