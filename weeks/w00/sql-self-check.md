---
module: m00
title: "SQL self-check (10 minutes, self-paced)"
tag: m00
grading: not graded, blocks nothing
source: modules/m00-onboarding/content.md Topic 11 (merged PR #39 at 1ab1676)
---

# SQL self-check

SQL is a prerequisite for this course. It is not taught. Weeks 4, 11 and 12 use simple SQL queries. This check tells you if you are ready.

- 8 questions on `SELECT`, `WHERE`, `GROUP BY` and `JOIN`.
- For each question, write a query, run it, then pick the option closest to your result.
- It is not graded and blocks nothing. If more than 2 answers are wrong, work through [SQLBolt](https://sqlbolt.com/) lessons 1 to 6 (interactive, in the browser, no sign-up) before Week 4.

## Set up (2 minutes)

Do this after Practical 0, Step 7. Install the SQLite command-line tool and load the diamonds file into a small database:

On macOS, skip the `apt` line: macOS ships `sqlite3` already (not yet tested on a Mac).

```
sudo apt install -y sqlite3
cd ~/<your-course-repo>/diamond-mlops
sqlite3 ~/diamonds.db
```

At the `sqlite>` prompt, type these 4 lines:

```
CREATE TABLE diamonds (carat REAL, cut TEXT, color TEXT, clarity TEXT, depth REAL, "table" REAL, price INTEGER, x REAL, y REAL, z REAL);
.import --csv --skip 1 data/raw/diamonds.csv diamonds
.mode column
.headers on
```

- `CREATE TABLE` gives each column a type, so numbers compare as numbers.
- `.import --csv --skip 1` loads the file and skips its header line.
- `table` is both a column name and a SQL keyword. Write it in double quotes: `"table"`.
- Stay at the `sqlite>` prompt for all 8 questions. Every query ends with `;`.

Check: `SELECT COUNT(*) FROM diamonds;` prints `53940`.

The data is the raw file, before the notebook removes duplicates and zero sizes. Your answers use the raw file.

---

## Questions

**1. How many diamonds weigh more than 2 carats?**

- A. 189
- B. 1,889
- C. 5,222
- D. 18,890

**2. How many diamonds cost more than 10,000?**

- A. 1,889
- B. 2,834
- C. 5,222
- D. 10,000

**3. What are the highest and the lowest prices?**

- A. 18,823 and 326
- B. 18,823 and 0
- C. 10,000 and 326
- D. 3,933 and 326

**4. How many diamonds have cut `Ideal` and color `D`?**

- A. 6,775
- B. 21,551
- C. 2,834
- D. 280

**5. Which cut has the highest average price?** (Use `GROUP BY cut`.)

- A. Ideal
- B. Premium
- C. Very Good
- D. Fair

**6. Which cut has the lowest average price?**

- A. Fair
- B. Good
- C. Ideal
- D. Premium

**7. Ideal is the best cut. Why can its average price be the lowest?** Run `SELECT cut, AVG(carat) FROM diamonds GROUP BY cut;` first.

- A. The file has a bug in the Ideal rows.
- B. Ideal diamonds are smaller on average (lowest average carat), and a plain average does not hold carat constant.
- C. Ideal diamonds have the worst color.
- D. SQLite rounds the Ideal prices down.

**8. A JOIN.** Create 2 small tables. They are invented for this question: model predictions, and the real prices that came in later.

```
CREATE TABLE predictions (id INTEGER, predicted_price INTEGER);
INSERT INTO predictions VALUES (1, 520), (2, 4100), (3, 9800);
CREATE TABLE actuals (id INTEGER, price INTEGER);
INSERT INTO actuals VALUES (1, 500), (2, 4400), (4, 7000);
```

Join them on `id` with an (inner) `JOIN`. Then compute the average absolute error, `AVG(ABS(predicted_price - price))`, over the joined rows. What do you get?

- A. 3 rows, average error 160
- B. 2 rows, average error 160
- C. 2 rows, average error 140
- D. 4 rows, average error 700

---

## Answers

Measured with SQLite 3.45.1 on the raw `diamonds.csv` at tag `m00` (October 2026).

| # | Answer | A query that works | Why |
|---|---|---|---|
| 1 | B, 1,889 | `SELECT COUNT(*) FROM diamonds WHERE carat > 2;` | `WHERE` keeps only matching rows; `COUNT(*)` counts them |
| 2 | C, 5,222 | `SELECT COUNT(*) FROM diamonds WHERE price > 10000;` | Same pattern. Do not write the number with a comma |
| 3 | A, 18,823 and 326 | `SELECT MAX(price), MIN(price) FROM diamonds;` | No price is 0. The zeros in the file are in `x`, `y` and `z` (20 rows) |
| 4 | C, 2,834 | `SELECT COUNT(*) FROM diamonds WHERE cut = 'Ideal' AND color = 'D';` | `AND` needs both. Text values go in single quotes. 6,775 is all color D; 21,551 is all Ideal |
| 5 | B, Premium | `SELECT cut, AVG(price) FROM diamonds GROUP BY cut ORDER BY AVG(price) DESC;` | Premium 4,584.26, Fair 4,358.76, Very Good 3,981.76, Good 3,928.86, Ideal 3,457.54 |
| 6 | C, Ideal | Same query | Ideal is last: 3,457.54 |
| 7 | B | `SELECT cut, AVG(carat) FROM diamonds GROUP BY cut;` | Average carat: Fair 1.046, Premium 0.892, Good 0.849, Very Good 0.806, Ideal 0.703. Carat drives price most. Comparing averages across groups can mislead when another column differs between the groups |
| 8 | B | `SELECT AVG(ABS(p.predicted_price - a.price)) FROM predictions p JOIN actuals a ON p.id = a.id;` | An inner join keeps only ids in both tables: 1 and 2. Id 3 has no actual price yet; id 4 has no prediction. Errors 20 and 300, average 160. In Week 12 you join predictions with real prices exactly like this |

When you are done: type `.quit` to leave SQLite, then `rm ~/diamonds.db`.
