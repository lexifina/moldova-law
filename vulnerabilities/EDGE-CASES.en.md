# Edge cases

[Română](EDGE-CASES.md) · **English**

None of the 42 flags the model reviewed survived. Here they are, each checked by hand and grouped by what it turned out to be, and what the other flags are. Back to [the vulnerabilities README](README.en.md).

## Spent (1)

| Provision | What the record says | Why it is harmless now |
| --- | --- | --- |
| [Constituția, Articolul IV](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/constitutia/tranz-04.md) (transitional provisions) | Article 25(4), on the length of arrest, does not apply "until 1 January 1995" to persons who committed serious offences under Article 7^1 of the Criminal Code | A transitional rule that ran out on 1 January 1995. Its only change here is the spelling of the 2024 edition ("răsfrâng, până" for "răsfrîng, pînă", and "7^1" for the register's "71"). |

## Lawful (1)

| Act | What the record says | Why it is lawful |
| --- | --- | --- |
| [Judgment HCC7/2016](https://github.com/lexifina/moldova-law/commit/009fddfa39d87241201b8f4e62297dca2438a1c9) of the Constitutional Court, changing Articles 78, 85 and 89 of the Constitution | in force 4 March 2016, published 18 March 2016 | Laws, or parts of them, become void "from the moment the corresponding judgment of the Constitutional Court is adopted" (Article 140(1) of the Constitution), and the Court's judgments state that they take effect on adoption, as [judgment No. 14 of 5 November 2026](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/caselaw/curtea-constitutionala/2026/hotariri-901/text.md), held here, does in its point 5. |

## Not law (40)

| Text | What the record says | Why it does not count |
| --- | --- | --- |
| 39 decisions of the Competition Council, among them [CN-36 of 21 July 2016](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2016/cn-36/text.md) and [DA-26 of 21 June 2017](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2017/da-26/text.md), the two the model first judged defects | a certificate of conformity of 29 April 2015 "valid until 28 April 2018"; SRL „Transenca-Tur” was to submit copies of documents "by 31.03.2017" under point 5 of decision DA-24 of 19 May 2016 | Facts of the case: licences, route permits and certificates with their terms, contract periods, a duty the Council set for a party, a village mayor's office to report on state aid "by 31.03.2017" ([ASR-39 of 27 July 2016](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2016/asr-39/text.md)). A decision in one case, not legislation; the second pass dismissed both candidates. |
| [Supreme Court of Justice, 2rac-132/13 of 29 May 2013](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/caselaw/curtea-suprema-de-justitie/2013/col-civil-842/text.md) | "from 16 July 2007 until 14 September 2007" | A period in the facts of a civil case. |

## Not flagged: traces of HCC7/2016 in the text

Read while checking the judgment's flag; no detector looks for these, and neither changes what a rule says.

- [Article 78](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/constitutia/art-078.md) goes from paragraph (4) to paragraph (6). Since HCC7/2016 ([the change](https://github.com/lexifina/moldova-law/commit/009fddfa39d87241201b8f4e62297dca2438a1c9)), the earlier paragraph (5), under which the President dissolved Parliament if repeated elections failed, is gone and the paragraphs were not renumbered. The Moldpres edition of 2024 prints the article the same way.
- [Article 85(4)](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/constitutia/art-085.md) reads "... mandatului Președintelui Republicii Moldova, și nici în timpul stării de urgență ...": the phrase HCC7/2016 struck, "cu excepția cazului prevăzut la articolul 78 alineatul (5)", went, and the comma before it stayed. The 2024 edition prints the comma too.

## The other flags

- **Lapsed time limits:** 84 of the 85 are in decisions, 78 of the Competition Council and 6 of the Supreme Court of Justice; 14 are in one decision, [APD-70 of 17 December 2015](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2015/apd-70/text.md), on bus carriers serving Chișinău–Prague and other routes: most are the terms of their licences and route permits. Of the 41 reviewed, 33 were judged artefacts, 6 lawful, and the 2 candidate defects fell to the second pass. The detector misses "pînă" and "până la data de" before a date; the 100 such phrases here are all in decisions.
- **Retroactive or pre-publication dates:** the one flag, above.
- **Duplicate numbering, dead currencies:** read by hand, not by a model. They are false positives. The 14 "duplicate numbers", 13 in Competition Council decisions and 1 in a Supreme Court decision, are the same article of a law cited at the start of two lines (for example "art. 19 alin. (1) lit. b) din Legea concurenţei nr. 183 din 11.07.2012" twice in [CN-62 of 8 October 2015](https://github.com/lexifina/moldova-law/blob/b9622766cdf1fa1863595ba9ccb48b928c59e9e3/decision/competition-council/2015/cn-62/text.md)). The 3 "dead currencies" are "inti", Peru's former currency, matched inside "intimatul" and "intimatului" (the respondent) in three Supreme Court decisions.
