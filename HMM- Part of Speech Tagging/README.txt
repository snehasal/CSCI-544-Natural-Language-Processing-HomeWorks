README for the Catalan part-of-speech tagging corpus used in Homework 5, USC course CSCI-544 (Applied Natural Language Processing), Spring 2017.

The corpus has been adapted from the Catalan portion of WikiCorpus v. 1.0, as follows:

- The homework corpus contains only a selection (< 1.2M words) from the original.
- The corpus contains only tokens and parts of speech, not lemmas and word senses.
- The part-of-speech tags have been simplified from the original, resulting in 29 tags.
- The format has been changed to the word/TAG format, with each sentence on a separate line.

The homework corpus is licensed under the same terms as the original, that is, the GNU Free Documentation License (FDL; http://www.fsf.org/licensing/licenses/fdl.html). That means that you are allowed to use and redistribute the texts, provided the derived works keep the same license.


The original README file for the WikiCorpus is below.


README FOR WIKICORPUS, v. 1.0
=============================
modified gbt 2010/06/04

The WikiCorpus has been created from a 2006 dump of the Catalan, Spanish, and English Wikipedias.

CONTENTS:
- files raw.{ca,es,en}.tgz: documents in raw form, as extracted from the Mediawiki markup format by the Java Parser.
- files tagged.{ca,es,en}.tgz: tagged documents, that is, documents processed with (tokenized, lemmatized, POS-tagged, automatically word sense disambiguated) with FreeLing (v. 2.1, default options), which includes the UKB algorithm for WSD.

DOCUMENTATION:
Samuel Reese, Gemma Boleda, Montse Cuadros, Lluís Padró, German Rigau. 2010. Word-Sense Disambiguated Multilingual Wikipedia Corpus. In Proceedings of 7th Language Resources and Evaluation Conference (LREC'10), La Valleta, Malta. May, 2010.

LICENSE:
The WikiCorpus is licensed under the same license as Wikipedia, that is, the GNU Free Documentation License (FDL; http://www.fsf.org/licensing/licenses/fdl.html). That means that you are allowed to use and redistribute the texts, provided the derived works keep the same license.

KNOWN ISSUES:
- documents end with a marker 'ENDOFARTICLE', which should be removed. This marker was included by us to facilitate processing.
- some documents are truncated (i.e., </doc> marker at the end of the document), in cases where the parser broke down. These are generally long documents with many embedded elements.
- around 10-15% of the documents in the 2006 dump are not included in the Spanish and English corpora, due to problems derived from parser errors (these did not affect Catalan documents, which are generally shorter).
- the accuracy of the processing in the WikiCorpora has not been evaluated. This is particularly pressing for Word Sense Disambiguation. The accuracies of the tools are however reported in the documentation for FreeLing (http://www.lsi.upc.edu/~nlp/freeling) and UKB (http://ixa2.si.ehu.es/ukb).




