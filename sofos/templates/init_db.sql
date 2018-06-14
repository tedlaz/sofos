BEGIN TRANSACTION;
INSERT INTO "apasxolisitype" VALUES(1,'Πλήρης');
INSERT INTO "apasxolisitype" VALUES(2,'Μερική');
INSERT INTO "apasxolisitype" VALUES(3,'Εκ περιτροπής');
INSERT INTO "apodoxestype" VALUES(1,'Μισθός');
INSERT INTO "apodoxestype" VALUES(2,'Ημερομίσθιο');
INSERT INTO "apodoxestype" VALUES(3,'Ωρομίσθιο');
INSERT INTO "apoxorisitype" VALUES(1,'Απόλυση χωρίς προειδοποίηση');
INSERT INTO "apoxorisitype" VALUES(2,'Απόλυση με προειδοποίηση');
INSERT INTO "apoxorisitype" VALUES(3,'Οικιοθελής αποχώρηση');
INSERT INTO "apoxorisitype" VALUES(4,'Αποχώρηση λόγω λήξης σύμβασης ορισμένου χρόνου');
INSERT INTO "apoxorisitype" VALUES(5,'Αποχώρηση λόγω λήξης σύμβασης έργου');
INSERT INTO "apoxorisitype" VALUES(6,'Συνταξιοδότηση');
INSERT INTO "ergtype" VALUES(1,'Υπάλληλος');
INSERT INTO "ergtype" VALUES(2,'Εργάτης');
INSERT INTO "minas" VALUES(1,'Ιανουάριος');
INSERT INTO "minas" VALUES(2,'Φεβρουάριος');
INSERT INTO "minas" VALUES(3,'Μάρτιος');
INSERT INTO "minas" VALUES(4,'Απρίλιος');
INSERT INTO "minas" VALUES(5,'Μαϊος');
INSERT INTO "minas" VALUES(6,'Ιούνιος');
INSERT INTO "minas" VALUES(7,'Ιούλιος');
INSERT INTO "minas" VALUES(8,'Αύγουστος');
INSERT INTO "minas" VALUES(9,'Σεπτέμβριος');
INSERT INTO "minas" VALUES(10,'Οκτώβριος');
INSERT INTO "minas" VALUES(11,'Νοέμβριος');
INSERT INTO "minas" VALUES(12,'Δεκέμβριος');
INSERT INTO "misthodosiatype" VALUES(1,'Τακτικές αποδοχές','01');
INSERT INTO "misthodosiatype" VALUES(2,'Δώρο Χριστουγέννων','03');
INSERT INTO "misthodosiatype" VALUES(3,'Δώρο Πάσχα','04');
INSERT INTO "misthodosiatype" VALUES(4,'Επίδομα Αδείας','05');
INSERT INTO "misthodosiatype" VALUES(5,'Επίδομα Ισολογισμού','06');
INSERT INTO "misthodosiatype" VALUES(6,'Αποδοχές Ασθενείας','08');
INSERT INTO "misthodosiatype" VALUES(7,'Αναδρομικές αποδοχές','09');
INSERT INTO "misthodosiatype" VALUES(8,'Bonus','10');
INSERT INTO "misthodosiatype" VALUES(9,'Υπερωρίες','11');
INSERT INTO "misthodosiatype" VALUES(10,'Λοιπές αποδοχές','14');
INSERT INTO "misthodosiatype" VALUES(11,'Αποζημίωση Απόλυσης','99');
INSERT INTO "oikogkat" VALUES(1,'Άγαμος');
INSERT INTO "oikogkat" VALUES(2,'Έγγαμος');
INSERT INTO "parartima" VALUES(1,'Κεντρικό','4568');
INSERT INTO "paroysiatype" VALUES(1,'Τακτικές παρουσίες','01');
INSERT INTO "paroysiatype" VALUES(2,'Ασθένεια','08');
INSERT INTO "paroysiatype" VALUES(3,'Υπερωρίες','11');
INSERT INTO "sex" VALUES(1,'Άντρας');
INSERT INTO "sex" VALUES(2,'Γυναίκα');
INSERT INTO "symbasitype" VALUES(1,'Αορίστου χρόνου');
INSERT INTO "symbasitype" VALUES(2,'Ορισμένου χρόνου');
INSERT INTO "symbasitype" VALUES(3,'Έργου');
INSERT INTO "taftotitatype" VALUES(1,'Αστυνομική ταυτότητα');
INSERT INTO "taftotitatype" VALUES(2,'Διαβατήριο');
INSERT INTO "xora" VALUES(1,'Ελλάδα');
INSERT INTO "xrisi" VALUES(1,2017);
INSERT INTO "xrisi" VALUES(2,2018);
INSERT INTO "hmerologio" VALUES(1,'Ανοίγματος χρήσης');
INSERT INTO "hmerologio" VALUES(2,'Γενικό ημερολόγιο');
INSERT INTO "hmerologio" VALUES(3,'Κλεισίματος χρήσης');
INSERT INTO "metabolitype" VALUES(1,'ΣΥΜΒΑΣΗ');
INSERT INTO "metabolitype" VALUES(2,'ΠΡΟΓΡΑΜΜΑ ΕΡΓΑΣΙΑΣ');
COMMIT;